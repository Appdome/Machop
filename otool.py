from itertools import groupby
from argparse import ArgumentParser

import macho
import constants


def fat_thin_functor(filename, function):
    if macho.is_fat(filename):
        for _, mach in macho.MachO(filename).iteritems():
            function(mach)
    else:
        function(macho.MachO(filename))


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
    for cmd in mach.load_commands():
        if cmd.cmd not in [constants.LC_SEGMENT, constants.LC_SEGMENT_64]:
            continue
        for section in cmd:
            yield section


def iter_symbols(mach):
    for cmd in mach.load_commands():
        if cmd.cmd not in [constants.LC_SYMTAB]:
            continue
        for symbol in cmd:
            yield symbol


def print_indirect_symbols(mach):
    symbol_dict = {section_index: list(symbol_list)
                   for section_index, symbol_list
                   in groupby(iter_symbols(mach), lambda sym: sym.n_sect)}
    for section_index, section in enumerate(iter_sections(mach)):
        print 'Indirect symbols for ({},{}) {} entries'.format(
            section.segment.name,
            section.name,
            len(symbol_dict.get(section_index, [])))
        print 'address            index name'
        for symbol in symbol_dict.get(section_index, []):
            print '0x{:016x} {:>5} {}'.format(
                symbol.n_value, symbol.idx, symbol)

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
    parser.add_argument('-I', action='store_true',
                        help='print the indirect symbol table')
    parser.add_argument('file')
    args = parser.parse_args()
    if args.l:
        fat_thin_functor(args.file, print_load_commands)
    elif args.I:
        fat_thin_functor(args.file, print_indirect_symbols)
