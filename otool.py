from argparse import ArgumentParser

import macho
import constants

LC_NAMES = {lc for lc in dir(constants) if lc.startswith('LC_')}
LC_NAMES_DICT = {getattr(constants, lc): lc for lc in LC_NAMES}


def print_load_commands_thin(mach):
    for i, cmd in enumerate(mach.load_commands()):
        print 'Load commnad {}'.format(i)
        print '      cmd {}'.format(LC_NAMES_DICT[cmd.cmd])
        print '  cmdsize {}'.format(cmd.cmdsize)
        if cmd.cmd in [constants.LC_SEGMENT, constants.LC_SEGMENT_64]:
            print '  segname {}'.format(cmd.segname.strip('\x00'))
            for section in cmd:
                print 'Section'
                print '  sectname {}'.format(section.sectname.strip('\x00'))
                print '   segname {}'.format(cmd.segname.strip('\x00'))


def print_load_commands(filename):
    if macho.is_fat(filename):
        for _, mach in macho.MachO(filename).iteritems():
            print_load_commands_thin(mach)
    else:
        print_load_commands_thin(macho.MachO(filename))

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
    parser.add_argument('file')
    args = parser.parse_args()
    if args.l:
        print_load_commands(args.file)
