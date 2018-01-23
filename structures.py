import struct

# Common

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

load_command = [
        ('cmd', uint32_t),
        ('cmdsize', uint32_t),
    ]

symtab_command = [
        ('cmd', uint32_t),
        ('cmdsize', uint32_t),
        ('symoff', uint32_t),
        ('nsyms', uint32_t),
        ('stroff', uint32_t),
        ('strsize', uint32_t),
    ]

relocation_info = [
        ('r_address', int32_t),
        ('r_info', uint32_t),
    ]

dysymtab_command = [
        ('cmd', uint32_t),
        ('cmdsize', uint32_t),
        ('ilocalsym', uint32_t),
        ('nlocalsym', uint32_t),
        ('iextdefsym', uint32_t),
        ('nextdefsym', uint32_t),
        ('iundefsym', uint32_t),
        ('nundefsym', uint32_t),
        ('tocoff', uint32_t),
        ('ntoc', uint32_t),
        ('modtaboff', uint32_t),
        ('nmodtab', uint32_t),
        ('extrefsymoff', uint32_t),
        ('nextrefsyms', uint32_t),
        ('indirectsymoff', uint32_t),
        ('nindirectsyms', uint32_t),
        ('extreloff', uint32_t),
        ('nextrel', uint32_t),
        ('locreloff', uint32_t),
        ('nlocrel', uint32_t),
    ]

table_index = [
        ('index', uint32_t),
    ]

# 32bit

mach_header_32 = [
        ('magic', uint32_t),
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('filetype', uint32_t),
        ('ncmds', uint32_t),
        ('sizeofcmds', uint32_t),
        ('flags', uint32_t),
    ]

segment_command_32 = [
        ('cmd', uint32_t),
        ('cmdsize', uint32_t),
        ('segname', '16s'),
        ('vmaddr', uint32_t),
        ('vmsize', uint32_t),
        ('fileoff', uint32_t),
        ('filesize', uint32_t),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', uint32_t),
        ('flags', uint32_t),
    ]

section_32 = [
        ('sectname', '16s'),
        ('segname', '16s'),
        ('addr', uint32_t),
        ('size', uint32_t),
        ('offset', uint32_t),
        ('align', uint32_t),
        ('reloff', uint32_t),
        ('nreloc', uint32_t),
        ('flags', uint32_t),
        ('reserved1', uint32_t),
        ('reserved2', uint32_t),
    ]

nlist_32 = [
        ('n_strx', int32_t),
        ('n_type', uint8_t),
        ('n_sect', uint8_t),
        ('n_desc', int16_t),
        ('n_value', uint32_t),
    ]

# 64bit

mach_header_64 = [
        ('magic', uint32_t),
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('filetype', uint32_t),
        ('ncmds', uint32_t),
        ('sizeofcmds', uint32_t),
        ('flags', uint32_t),
        ('reserved', uint32_t),
    ]

segment_command_64 = [
        ('cmd', uint32_t),
        ('cmdsize', uint32_t),
        ('segname', '16s'),
        ('vmaddr', uint64_t),
        ('vmsize', uint64_t),
        ('fileoff', uint64_t),
        ('filesize', uint64_t),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', uint32_t),
        ('flags', uint32_t),
    ]

section_64 = [
        ('sectname', '16s'),
        ('segname', '16s'),
        ('addr', uint64_t),
        ('size', uint64_t),
        ('offset', uint32_t),
        ('align', uint32_t),
        ('reloff', uint32_t),
        ('nreloc', uint32_t),
        ('flags', uint32_t),
        ('reserved1', uint32_t),
        ('reserved2', uint32_t),
        ('reserved3', uint32_t),
    ]

nlist_64 = [
        ('n_strx', int32_t),
        ('n_type', uint8_t),
        ('n_sect', uint8_t),
        ('n_desc', int16_t),
        ('n_value', uint64_t),
    ]


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
