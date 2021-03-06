#!/usr/bin/env python

from itertools import groupby
from argparse import ArgumentParser

import macho
import constants


def fat_thin_functor(filename, func):
    if macho.is_fat(filename):
        for _, mach in macho.MachO(filename).iteritems():
            func(mach)
    else:
        func(macho.MachO(filename))


LC_NAMES = {lc for lc in dir(constants) if lc.startswith('LC_')}
LC_NAMES_DICT = {getattr(constants, lc): lc for lc in LC_NAMES}


def print_load_commands(mach):
    for i, cmd in enumerate(mach.load_commands()):
        print 'Load commnad {}'.format(i)
        print '      cmd {}'.format(LC_NAMES_DICT[cmd.cmd])
        print '  cmdsize {}'.format(cmd.cmdsize)
        if cmd.cmd in [constants.LC_SEGMENT, constants.LC_SEGMENT_64]:
            print '  segname {}'.format(cmd.name)
            for section in cmd:
                print 'Section'
                print '  sectname {}'.format(section.name)
                print '   segname {}'.format(cmd.name)


def iter_sections(mach):
    for cmd in mach.load_commands([constants.LC_SEGMENT, constants.LC_SEGMENT_64]):
        for section in cmd:
            yield section


def iter_symbols(mach):
    for symbol in mach.load_command(constants.LC_SYMTAB):         
        yield symbol


def print_all_symbols(mach):
    symbol_dict = {section_index: list(symbol_list)
                   for section_index, symbol_list
                   in groupby(iter_symbols(mach), lambda sym: sym.n_sect)}
    for section_index, section in enumerate(iter_sections(mach)):
        print 'Symbols for ({},{}) {} entries'.format(
            section.segment.name,
            section.name,
            len(symbol_dict.get(section_index, [])))
        print 'address            index name'
        for symbol in symbol_dict.get(section_index, []):
            print '0x{:016x} {:>5} {}'.format(
                symbol.n_value, symbol.idx, symbol)


def get_dy_symbols(mach):
    cmd = mach.load_command(constants.LC_DYSYMTAB)
    return list(cmd)


def print_indirect_symbols(mach):
    symbol_list = get_dy_symbols(mach)
    is_64 = isinstance(mach, macho._MachO64)
    symbol_address_size = 8 if is_64 else 4
    for section_index, section in enumerate(iter_sections(mach)):
        sec_flags = section.flags
        if (sec_flags == constants.S_NON_LAZY_SYMBOL_POINTERS) \
                or (sec_flags == constants.S_LAZY_SYMBOL_POINTERS):
            number_of_symbols = section.size / symbol_address_size
        elif sec_flags == constants.S_SYMBOL_STUBS:
            number_of_symbols = section.size / section.reserved2
        else:
            continue
        print 'Indirect symbols for ({},{}) {} entries'.format(
            section.segment.name,
            section.name,
            number_of_symbols)
        address = section.addr
        print 'address            index name'
        first_symbol = section.reserved1
        for index in xrange(number_of_symbols):
            symbol = symbol_list[first_symbol + index]
            print '0x{:08x} {:>5} {}'.format(
                address, symbol.idx, symbol)
            address += symbol_address_size


if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)
    parser.add_argument('--help', action='help',
                        help='show this help message and exit')
    parser.add_argument('-f', action='store_true',
                        help='print the fat headers')
    parser.add_argument('-a', action='store_true',
                        help='print the archive header')
    parser.add_argument('-h', action='store_true',
                        help='print the mach header')
    parser.add_argument('-l', action='store_true',
                        help='print the load commands')
    parser.add_argument('--all-symbols', action='store_true',
                        help='print the entire symbol table')
    parser.add_argument('-I', action='store_true',
                        help='print the indirect symbol table')
    parser.add_argument('file')
    args = parser.parse_args()
    if args.l:
        fat_thin_functor(args.file, print_load_commands)
    elif args.all_symbols:
        fat_thin_functor(args.file, print_all_symbols)
    elif args.I:
        fat_thin_functor(args.file, print_indirect_symbols)
