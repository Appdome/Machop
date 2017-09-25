import struct

from constants import *
from structures import *
from cputype import get_arch_name


class LoadCommand(object):
    CMD = load_command

    def __init__(self, macho, offset):
        self.macho = macho
        self.lcmd = macho.unpack(offset, self.CMD)

    def __getattr__(self, attr):
        return self.lcmd.get(attr, None)

    def __str__(self):
        return 'LoadCommand(cmd={}, cmdsize={})'.format(self.cmd, self.cmdsize)


class SegmentCommand(LoadCommand):
    def __str__(self):
        return 'Segment:{}'.format(self.segname.strip('\x00'))


class SegmentCommand32(SegmentCommand):
    CMD = segment_command_32


class SegmentCommand64(SegmentCommand):
    CMD = segment_command_64


class SymtabCommand(LoadCommand):
    CMD = symtab_command

    def __str__(self):
        return 'Symtab(nsyms={})'.format(self.nsyms)


class _MachO(object):
    mach_header = None
    segment_command = None
    section = None
    LC_SEGMENT_cmd = None
    nlist = None
    LOAD_COMMAND_CLASSES = {}

    def __init__(self, filename, little_endian=True, arch=None):
        self.little_endian = little_endian
        with open(filename, 'rb') as macho_file:
            if arch is None:
                # Read all the file
                self.raw = macho_file.read()
            else:
                # Read just the part specified by the `arch` parameter
                macho_file.seek(arch['offset'])
                self.raw = macho_file.read(arch['size'])
        self.header = self.unpack(0, self.mach_header)
        for xxx in self.load_commands():
            print xxx

    def load_commands(self):
        offset = sizeof(self.mach_header)
        for i in range(self.header['ncmds']):
            cmd = self.unpack(offset, load_command)
            cmd_class = self.LOAD_COMMAND_CLASSES.get(cmd['cmd'], LoadCommand)
            yield cmd_class(self, offset)
            offset += cmd['cmdsize']

    def unpack(self, offset, spec):
        endianesse = '<' if self.little_endian else '>'
        names, types = zip(*spec)
        fmt = endianesse + ''.join(types)
        values = struct.unpack_from(fmt, self.raw, offset)
        return dict(zip(names, values))


class _MachO64(_MachO):
    mach_header = mach_header_64
    segment_command = segment_command_64
    section = section_64
    LC_SEGMENT_cmd = LC_SEGMENT_64
    nlist = nlist_64
    LOAD_COMMAND_CLASSES = {
            LC_SEGMENT_64: SegmentCommand64,
            LC_SYMTAB: SymtabCommand,
        }


class _MachO32(_MachO):
    mach_header = mach_header_32
    segment_command = segment_command_32
    section = section_32
    LC_SEGMENT_cmd = LC_SEGMENT
    nlist = nlist_32
    LOAD_COMMAND_CLASSES = {
            LC_SEGMENT: SegmentCommand32,
            LC_SYMTAB: SymtabCommand,
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
        for i in range(header['nfat_arch']):
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
            if magic == MH_MAGIC_64:
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
