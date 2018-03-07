import struct

from constants import *
from structures import *
from cputype import get_arch_name
from collections import OrderedDict


def check_flag(flag, mask):
    return (flag & mask) == mask


class LoadCommand(object):
    CMD = load_command

    def __init__(self, macho, offset=None, lcmd=None):
        self.macho = macho
        self.offset = offset

        if offset is None:  # used in a self generated LoadCommand
            self.lcmd = lcmd
        else:
            self.lcmd = macho.unpack(offset, self.CMD)

    def __getattr__(self, attr):
        return self.lcmd.get(attr, None)

    def __str__(self):
        return 'LoadCommand(cmd={}, cmdsize={})'.format(self.cmd, self.cmdsize)


class Section(object):
    def __init__(self, segment, section):
        self.segment = segment
        self.section = section

    def __getattr__(self, attr):
        return self.section.get(attr, None)

    @property
    def name(self):
        return self.sectname.strip('\x00')


class DylibCommand(LoadCommand):
    CMD = dylib_command

    def __init__(self, macho=None, offset=None, lcmd=None):
        if macho is None:
            pass
        else:
            return super(DylibCommand, self).__init__(macho, offset, lcmd)


    @property
    def name(self):
        name_string = self.macho.raw[self.offset + self.name_offset:]
        end = name_string.find("\x00")
        return name_string[:end]

def createDylibCommand(macho, timestamp, version, comp_version, name):
    # CR: Are you aligning the name length to the platform's word size?
    # If so, use "word_size", not "gran", and the "name_len"
    # calculation should be with an "align" function
    gran = 8 if macho.is_64() else 4
    name_len = len(name) + gran - (len(name) % gran)
    tempDylib = DylibCommand()
    tempDylib.CMD = dylib_command[:]
    name_offset = sizeof(tempDylib.CMD)
    cmdsize = name_offset + name_len
    tempDylib.CMD += [('name', str(name_len) + 's')]
    names, types = zip(*tempDylib.CMD)
    generated_lcmd = OrderedDict(zip(names, [LC_LOAD_DYLIB,
                                             cmdsize, name_offset,
                                             timestamp, version,
                                             comp_version, name]))
    tempDylib.__init__(macho, None, generated_lcmd)
    return tempDylib


class SegmentCommand(LoadCommand):
    SECTION_COMMAND = None

    def __iter__(self):
        offset = self.offset + sizeof(self.CMD)
        for _ in range(self.nsects):
            section = self.macho.unpack(offset, self.SECTION_COMMAND)
            yield Section(self, section)
            offset += sizeof(self.SECTION_COMMAND)

    def __str__(self):
        return 'Segment:{}'.format(self.segname.strip('\x00'))

    @property
    def name(self):
        return self.segname.strip('\x00')


class SegmentCommand32(SegmentCommand):
    CMD = segment_command_32
    SECTION_COMMAND = section_32


class SegmentCommand64(SegmentCommand):
    CMD = segment_command_64
    SECTION_COMMAND = section_64


class Symbol(object):
    def __init__(self, symtab, nlist, idx):
        self.symtab = symtab
        self.nlist = nlist
        self.idx = idx

    def __str__(self):
        return self.symtab.extract_name(self.n_strx)

    def __getattr__(self, attr):
        return self.nlist.get(attr, None)


class SpecialSymbol(Symbol):
    def __init__(self, name):
        self.n_value = 0
        self.idx = 0
        self.name = name

    def __str__(self):
        return self.name


class SymtabCommand(LoadCommand):
    CMD = symtab_command
    NLIST = None

    def __iter__(self):
        offset = self.symoff
        for idx in range(self.nsyms):
            nlist = self.macho.unpack(offset, self.NLIST)
            yield Symbol(self, nlist, idx)
            offset += sizeof(self.NLIST)

    def extract_name(self, name_offset):
        chars = []
        offset = self.stroff + name_offset
        while self.macho.raw[offset] != '\0':
            chars.append(self.macho.raw[offset])
            offset += 1
        return ''.join(chars)

    def __str__(self):
        return 'Symtab(nsyms={})'.format(self.nsyms)


class SymtabCommand32(SymtabCommand):
    NLIST = nlist_32


class SymtabCommand64(SymtabCommand):
    NLIST = nlist_64


class DySymtabCommand(LoadCommand):
    CMD = dysymtab_command

    def __init__(self, macho, offset):
        super(DySymtabCommand, self).__init__(macho, offset)
        for cmd in macho.load_commands():
            if cmd.cmd == LC_SYMTAB:
                self.symbols_table = [sym for sym in cmd]
                break

    def __iter__(self):
        offset = self.indirectsymoff
        for idx in range(self.nindirectsyms):
            index = self.macho.unpack(offset, table_index)['index']
            if check_flag(index, INDIRECT_SYMBOL_ABS):
                yield SpecialSymbol("ABSOLUTE")
            elif check_flag(index, INDIRECT_SYMBOL_LOCAL):
                yield SpecialSymbol("LOCAL")
            else:
                yield self.symbols_table[index]
            offset += sizeof(table_index)


class _MachO(object):
    mach_header = None
    segment_command = None
    section = None
    LC_SEGMENT_cmd = None
    nlist = None
    LOAD_COMMAND_CLASSES = {}

    def __init__(self, filename, little_endian=True, arch=None):
        self.little_endian = little_endian
        self.filename = filename
        with open(filename, 'rb') as macho_file:
            if arch is None:
                # Read all the file
                self.mach_offset = 0
                self.raw = macho_file.read()
                self.mach_offset = 0
            else:
                # Read just the part specified by the `arch` parameter
                macho_file.seek(arch['offset'])
                self.mach_offset = arch['offset']
                self.raw = macho_file.read(arch['size'])
        self.header = self.unpack(0, self.mach_header)
        self.file_changed = False

    def load_commands(self):
        offset = sizeof(self.mach_header)
        for _ in range(self.header['ncmds']):
            cmd = self.unpack(offset, load_command)
            cmd_class = self.LOAD_COMMAND_CLASSES.get(cmd['cmd'], LoadCommand)
            yield cmd_class(self, offset)
            offset += cmd['cmdsize']

    def unpack(self, offset, spec):
        endianesse = '<' if self.little_endian else '>'
        names, types = zip(*spec)
        fmt = endianesse + ''.join(types)
        values = struct.unpack_from(fmt, self.raw, offset)
        return OrderedDict(zip(names, values))

    def pack(self, values, spec):
        endianesse = '<' if self.little_endian else '>'
        names, types = zip(*spec)
        fmt = endianesse + ''.join(types)
        return struct.pack(fmt, *values.values())

    # CR: Could it be better to define a static field for each MachO class:
    # "word" and maybe even a "word_size" and then you don't need the dirty
    # "isinstance" hack.
    def is_64(self):
        return isinstance(self, _MachO64)

    def flush_changes_to_file(self):
        if self.file_changed:
            with open(self.filename, "r+b") as macho_file:
                macho_file.seek(self.mach_offset)
                macho_file.write(self.raw)

    def update_file_part(self, value, spec, offset):
        # CR: The docstring does not fit the function's parameter names
        """
        updates file in memory ONLY
        :param data: data to write
        :param offset: offset in current MachO part
        :return:
        """
        packed = self.pack(value, spec)
        self.raw = self.raw[:offset] + packed + self.raw[offset + len(packed):]
        self.file_changed = True
        return len(packed)

    def iter_sections(self):
        for cmd in self.load_commands():
            if cmd.cmd not in [LC_SEGMENT, LC_SEGMENT_64]:
                continue
            for section in cmd:
                yield section

    def iter_symbols(self):
        for cmd in self.load_commands():
            if cmd.cmd not in [LC_SYMTAB]:
                continue
            for symbol in cmd:
                yield symbol

    def add_load_command_load_dylib(self, load_coammnd_to_insert):
        load_commands = list(self.load_commands())
        offset = load_commands[-1].offset + load_commands[-1].cmdsize
        if not self.can_add_command(load_coammnd_to_insert.cmdsize, offset):
            raise Exception("Can't add command. Padding is too small")
        added_data_len = self.update_file_part(load_coammnd_to_insert.lcmd,
                                               load_coammnd_to_insert.CMD,
                                               offset)
        self.header['ncmds'] += 1
        self.header['sizeofcmds'] += added_data_len
        self.update_file_part(self.header, self.mach_header, 0)

    def remove_load_command(self, command_index):
        load_commands = list(self.load_commands())
        target_command_size = load_commands[command_index].lcmd["cmdsize"]

        #Delete the load command
        delete_range_start = load_commands[command_index].offset
        delete_range_end = delete_range_start + target_command_size

        self.raw = "".join((self.raw[0:delete_range_start], self.raw[delete_range_end:-1]))

        #Add zeroes at the end of load commands section
        filler_start = load_commands[-1].offset + load_commands[-1].lcmd["cmdsize"] - target_command_size
        self.raw = "".join((self.raw[0:filler_start], "\x00" * target_command_size, self.raw[filler_start:-1]))

        #Update number of commands and load section size
        self.header["ncmds"] = self.header["ncmds"] - 1
        self.header["sizeofcmds"] = self.header["sizeofcmds"] - target_command_size
        new_macho_header = pack_dict(self.header, self.mach_header)
        # TODO - use update_file_part func
        self.raw = "".join((new_macho_header, self.raw[len(new_macho_header):]))
        self.file_changed = True

    def can_add_command(self, command_size, command_start):
        min_offset = min([sec.offset for sec in self.iter_sections() if not sec.flags == S_ZEROFILL])
        return (self.mach_offset + command_start + command_size) <= \
               (min_offset + self.mach_offset)


class _MachO64(_MachO):
    mach_header = mach_header_64
    segment_command = segment_command_64
    section = section_64
    LC_SEGMENT_cmd = LC_SEGMENT_64
    nlist = nlist_64
    LOAD_COMMAND_CLASSES = {
        LC_SEGMENT_64: SegmentCommand64,
        LC_SYMTAB: SymtabCommand64,
        LC_DYSYMTAB: DySymtabCommand,
        LC_LOAD_DYLIB: DylibCommand,
    }


class _MachO32(_MachO):
    mach_header = mach_header_32
    segment_command = segment_command_32
    section = section_32
    LC_SEGMENT_cmd = LC_SEGMENT
    nlist = nlist_32
    LOAD_COMMAND_CLASSES = {
        LC_SEGMENT: SegmentCommand32,
        LC_SYMTAB: SymtabCommand32,
        LC_DYSYMTAB: DySymtabCommand,
        LC_LOAD_DYLIB: DylibCommand,
    }


def load_thin_32(filename, little_endian=True):
    return _MachO32(filename, little_endian)


def load_thin_64(filename, little_endian=True):
    return _MachO64(filename, little_endian)


def load_fat(filename, little_endian=True):
    with open(filename, 'rb') as f:
        header_bytes = f.read(sizeof(fat_header))
        header = unpack_from(header_bytes, 0, fat_header, little_endian)
        thins = {}
        for _ in range(header['nfat_arch']):
            arch_bytes = f.read(sizeof(fat_arch))
            arch = unpack_from(arch_bytes, 0, fat_arch, little_endian)
            arch_name = get_arch_name(arch['cputype'], arch['cpusubtype'])

            offset = f.tell()
            f.seek(arch['offset'])
            magic = struct.unpack('<I', f.read(4))[0]
            f.seek(offset)

            if magic == MH_MAGIC:
                thins[arch_name] = _MachO32(filename, True, arch)
            elif magic == MH_CIGAM:
                thins[arch_name] = _MachO32(filename, False, arch)
            elif magic == MH_MAGIC_64:
                thins[arch_name] = _MachO64(filename, True, arch)
            elif magic == MH_CIGAM_64:
                thins[arch_name] = _MachO64(filename, False, arch)
            else:
                thins[arch_name] = None
        return thins


def load_non_mach(filename):
    return None


def read_magic(filename):
    with open(filename, 'rb') as f:
        magic = f.read(4)
        if len(magic) == 4:
            return struct.unpack('<I', magic)[0]
    return None


def is_fat(filename):
    return read_magic(filename) in [FAT_CIGAM, FAT_MAGIC]


def MachO(filename):
    MACH_PARSERS = {
        FAT_MAGIC: lambda filename: load_fat(filename, True),
        FAT_CIGAM: lambda filename: load_fat(filename, False),
        MH_MAGIC: lambda filename: load_thin_32(filename, True),
        MH_CIGAM: lambda filename: load_thin_32(filename, False),
        MH_MAGIC_64: lambda filename: load_thin_64(filename, True),
        MH_CIGAM_64: lambda filename: load_thin_64(filename, False),
    }
    return MACH_PARSERS.get(read_magic(filename), load_non_mach)(filename)


if __name__ == '__main__':
    from sys import argv
    print MachO(argv[1])
