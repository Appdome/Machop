import struct

from constants import *
from cputype import get_arch_name


def unpack_from(raw, offset, spec, little_endian=True):
    endianesse = '<' if little_endian else '>'
    names, types = zip(*spec)
    fmt = endianesse + ''.join(types)
    values = struct.unpack_from(fmt, raw, offset)
    return dict(zip(names, values))


def sizeof(spec):
    names, types = zip(*spec)
    fmt = ''.join(types)
    return struct.calcsize(fmt)

uint8_t = 'B'
int16_t = 'h'
int32_t = 'i'
uint32_t = 'I'
uint64_t = 'Q'
cpu_type_t = int32_t
cpu_subtype_t = int32_t
vm_prot_t = int32_t

fat_header = [
        ('magic', uint32_t),
        ('nfat_arch', uint32_t),
        ]

fat_arch = [
        ('cputype', uint32_t),
        ('cpusubtype', uint32_t),
        ('offset', uint32_t),
        ('size', uint32_t),
        ('align', uint32_t),
        ]


class _MachO(object):
    def __init__(self, filename, little_endian=True, arch=None):
        with open(filename, 'rb') as macho_file:
            if arch is None:
                # Read all the file
                self.raw = macho_file.read()
            else:
                # Read just the part specified by the `arch` parameter
                macho_file.seek(arch['offset'])
                self.raw = macho_file.read(arch['size'])


def load_thin(filename, little_endian=True):
    return _MachO(filename, little_endian)


def load_fat(filename, little_endian=True):
    with open(filename, 'rb') as f:
        header_bytes = f.read(sizeof(fat_header))
        header = unpack_from(header_bytes, 0, fat_header, little_endian)
        thins = {}
        for i in range(header['nfat_arch']):
            arch_bytes = f.read(sizeof(fat_arch))
            arch = unpack_from(arch_bytes, 0, fat_arch, little_endian)
            arch_name = get_arch_name(arch['cputype'], arch['cpusubtype'])
            thins[arch_name] = _MachO(filename, little_endian, arch)
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
            MH_MAGIC: lambda filename: load_thin(filename, True),
            MH_CIGAM: lambda filename: load_thin(filename, False),
            MH_MAGIC_64: lambda filename: load_thin(filename, True),
            MH_CIGAM_64: lambda filename: load_thin(filename, False),
            }
    return MACH_PARSERS.get(read_magic(filename), load_non_mach)(filename)

if __name__ == '__main__':
    from sys import argv
    print MachO(argv[1])
