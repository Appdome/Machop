if __name__ == '__main__':
    with open('mach', 'rU') as magic:
        print 'def get_arch_name(cputype, cpusubtype):'
        print '    output = \'\''
        for line in magic:
            if line.startswith('#'):
                print line.strip()
            elif line.startswith('>'):
                tokens = line.strip().split(None, 3)
                if len(tokens) == 4:
                    input_selector, mask, value_selector, fmt = tokens
                    if fmt.startswith('\\b'):
                        fmt = fmt[2:]
                else:
                    fmt = ''
                    input_selector, mask, value_selector = tokens
                depth = len(input_selector[:-1])
                prefix = depth * '    '
                if input_selector[-1] == '0':
                    var = 'cputype'
                elif input_selector[-1] == '4':
                    var = 'cpusubtype'
                mask = int(mask.split('&')[1], 16)
                if value_selector.startswith('>'):
                    print '{}if {} & {} > {}:'.format(
                            prefix, var, hex(mask), value_selector[1:])
                else:
                    print '{}if {} & {} == {}:'.format(
                            prefix, var, hex(mask), value_selector)
                if len(fmt) != 0:
                    if '%' in fmt:
                        print '{}    output += \'{}\' % ({} & {})'.format(
                                prefix, fmt, var, hex(mask))
                    else:
                        print '{}    output += \'{}\''.format(
                                prefix, fmt)
                else:
                        print '{}    output += \'\''.format(prefix)
        print '    return output'
