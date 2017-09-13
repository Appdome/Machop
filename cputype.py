def get_arch_name(cputype, cpusubtype):
    output = ''
#------------------------------------------------------------
# $File: mach,v 1.22 2015/10/15 16:54:01 christos Exp $
# Mach has two magic numbers, 0xcafebabe and 0xfeedface.
# Unfortunately the first, cafebabe, is shared with
# Java ByteCode, so they are both handled in the file "cafebabe".
# The "feedface" ones are handled herein.
#------------------------------------------------------------
# if set, it's for the 64-bit version of the architecture
# yes, this is separate from the low-order magic number bit
# it's also separate from the "64-bit libraries" bit in the
# upper 8 bits of the CPU subtype
    if cputype & 0x1000000 == 0:
        output += ''
#
# 32-bit ABIs.
#
#				1	vax
        if cputype & 0xffffff == 1:
            output += ''
            if cpusubtype & 0xffffff == 0:
                output += 'vax'
            if cpusubtype & 0xffffff == 1:
                output += 'vax11/780'
            if cpusubtype & 0xffffff == 2:
                output += 'vax11/785'
            if cpusubtype & 0xffffff == 3:
                output += 'vax11/750'
            if cpusubtype & 0xffffff == 4:
                output += 'vax11/730'
            if cpusubtype & 0xffffff == 5:
                output += 'uvaxI'
            if cpusubtype & 0xffffff == 6:
                output += 'uvaxII'
            if cpusubtype & 0xffffff == 7:
                output += 'vax8200'
            if cpusubtype & 0xffffff == 8:
                output += 'vax8500'
            if cpusubtype & 0xffffff == 9:
                output += 'vax8600'
            if cpusubtype & 0xffffff == 10:
                output += 'vax8650'
            if cpusubtype & 0xffffff == 11:
                output += 'vax8800'
            if cpusubtype & 0xffffff == 12:
                output += 'uvaxIII'
            if cpusubtype & 0xffffff > 12:
                output += 'vax subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff == 2:
            output += 'romp'
        if cputype & 0xffffff == 3:
            output += 'architecture=3'
        if cputype & 0xffffff == 4:
            output += 'ns32032'
        if cputype & 0xffffff == 5:
            output += 'ns32332'
        if cputype & 0xffffff == 6:
            output += 'm68k'
#				7	x86
        if cputype & 0xffffff == 7:
            output += ''
            if cpusubtype & 0xf == 3:
                output += 'i386'
            if cpusubtype & 0xf == 4:
                output += 'i486'
                if cpusubtype & 0xfffff0 == 0:
                    output += ''
                if cpusubtype & 0xfffff0 == 0x80:
                    output += 'sx'
            if cpusubtype & 0xf == 5:
                output += 'i586'
            if cpusubtype & 0xf == 6:
                output += ''
                if cpusubtype & 0xfffff0 == 0:
                    output += 'p6'
                if cpusubtype & 0xfffff0 == 0x10:
                    output += 'pentium_pro'
                if cpusubtype & 0xfffff0 == 0x20:
                    output += 'pentium_2_m0x20'
                if cpusubtype & 0xfffff0 == 0x30:
                    output += 'pentium_2_m3'
                if cpusubtype & 0xfffff0 == 0x40:
                    output += 'pentium_2_m0x40'
                if cpusubtype & 0xfffff0 == 0x50:
                    output += 'pentium_2_m5'
                if cpusubtype & 0xfffff0 > 0x50:
                    output += 'pentium_2_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf == 7:
                output += 'celeron'
                if cpusubtype & 0xfffff0 == 0x00:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
                if cpusubtype & 0xfffff0 == 0x10:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
                if cpusubtype & 0xfffff0 == 0x20:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
                if cpusubtype & 0xfffff0 == 0x30:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
                if cpusubtype & 0xfffff0 == 0x40:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
                if cpusubtype & 0xfffff0 == 0x50:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
                if cpusubtype & 0xfffff0 == 0x60:
                    output += ''
                if cpusubtype & 0xfffff0 == 0x70:
                    output += '_mobile'
                if cpusubtype & 0xfffff0 > 0x70:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf == 8:
                output += 'pentium_3'
                if cpusubtype & 0xfffff0 == 0x00:
                    output += ''
                if cpusubtype & 0xfffff0 == 0x10:
                    output += '_m'
                if cpusubtype & 0xfffff0 == 0x20:
                    output += '_xeon'
                if cpusubtype & 0xfffff0 > 0x20:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf == 9:
                output += 'pentiumM'
                if cpusubtype & 0xfffff0 == 0x00:
                    output += ''
                if cpusubtype & 0xfffff0 > 0x00:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf == 10:
                output += 'pentium_4'
                if cpusubtype & 0xfffff0 == 0x00:
                    output += ''
                if cpusubtype & 0xfffff0 == 0x10:
                    output += '_m'
                if cpusubtype & 0xfffff0 > 0x10:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf == 11:
                output += 'itanium'
                if cpusubtype & 0xfffff0 == 0x00:
                    output += ''
                if cpusubtype & 0xfffff0 == 0x10:
                    output += '_2'
                if cpusubtype & 0xfffff0 > 0x10:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf == 12:
                output += 'xeon'
                if cpusubtype & 0xfffff0 == 0x00:
                    output += ''
                if cpusubtype & 0xfffff0 == 0x10:
                    output += '_mp'
                if cpusubtype & 0xfffff0 > 0x10:
                    output += '_m0x%x' % (cpusubtype & 0xfffff0)
            if cpusubtype & 0xf > 12:
                output += 'ia32 family=%d' % (cpusubtype & 0xf)
                if cpusubtype & 0xfffff0 == 0x00:
                    output += ''
                if cpusubtype & 0xfffff0 > 0x00:
                    output += 'model=%x' % (cpusubtype & 0xfffff0)
        if cputype & 0xffffff == 8:
            output += 'mips'
            if cpusubtype & 0xffffff == 1:
                output += 'R2300'
            if cpusubtype & 0xffffff == 2:
                output += 'R2600'
            if cpusubtype & 0xffffff == 3:
                output += 'R2800'
            if cpusubtype & 0xffffff == 4:
                output += 'R2000a'
            if cpusubtype & 0xffffff == 5:
                output += 'R2000'
            if cpusubtype & 0xffffff == 6:
                output += 'R3000a'
            if cpusubtype & 0xffffff == 7:
                output += 'R3000'
            if cpusubtype & 0xffffff > 7:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff == 9:
            output += 'ns32532'
        if cputype & 0xffffff == 10:
            output += 'mc98000'
        if cputype & 0xffffff == 11:
            output += 'hppa'
            if cpusubtype & 0xffffff == 0:
                output += '7100'
            if cpusubtype & 0xffffff == 1:
                output += '7100LC'
            if cpusubtype & 0xffffff > 1:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff == 12:
            output += 'arm'
            if cpusubtype & 0xffffff == 0:
                output += ''
            if cpusubtype & 0xffffff == 1:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 2:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 3:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 4:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 5:
                output += 'v4t'
            if cpusubtype & 0xffffff == 6:
                output += 'v6'
            if cpusubtype & 0xffffff == 7:
                output += 'v5tej'
            if cpusubtype & 0xffffff == 8:
                output += 'xscale'
            if cpusubtype & 0xffffff == 9:
                output += 'v7'
            if cpusubtype & 0xffffff == 10:
                output += 'v7f'
            if cpusubtype & 0xffffff == 11:
                output += 'v7s'
            if cpusubtype & 0xffffff == 12:
                output += 'v7k'
            if cpusubtype & 0xffffff == 13:
                output += 'v8'
            if cpusubtype & 0xffffff == 14:
                output += 'v6m'
            if cpusubtype & 0xffffff == 15:
                output += 'v7m'
            if cpusubtype & 0xffffff == 16:
                output += 'v7em'
            if cpusubtype & 0xffffff > 16:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
#				13	m88k
        if cputype & 0xffffff == 13:
            output += ''
            if cpusubtype & 0xffffff == 0:
                output += 'mc88000'
            if cpusubtype & 0xffffff == 1:
                output += 'mc88100'
            if cpusubtype & 0xffffff == 2:
                output += 'mc88110'
            if cpusubtype & 0xffffff > 2:
                output += 'mc88000 subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff == 14:
            output += 'SPARC'
        if cputype & 0xffffff == 15:
            output += 'i860g'
        if cputype & 0xffffff == 16:
            output += 'alpha'
        if cputype & 0xffffff == 17:
            output += 'rs6000'
        if cputype & 0xffffff == 18:
            output += 'ppc'
            if cpusubtype & 0xffffff == 0:
                output += ''
            if cpusubtype & 0xffffff == 1:
                output += '_601'
            if cpusubtype & 0xffffff == 2:
                output += '_602'
            if cpusubtype & 0xffffff == 3:
                output += '_603'
            if cpusubtype & 0xffffff == 4:
                output += '_603e'
            if cpusubtype & 0xffffff == 5:
                output += '_603ev'
            if cpusubtype & 0xffffff == 6:
                output += '_604'
            if cpusubtype & 0xffffff == 7:
                output += '_604e'
            if cpusubtype & 0xffffff == 8:
                output += '_620'
            if cpusubtype & 0xffffff == 9:
                output += '_650'
            if cpusubtype & 0xffffff == 10:
                output += '_7400'
            if cpusubtype & 0xffffff == 11:
                output += '_7450'
            if cpusubtype & 0xffffff == 100:
                output += '_970'
            if cpusubtype & 0xffffff > 100:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff > 18:
            output += 'architecture=%d' % (cputype & 0xffffff)
    if cputype & 0x1000000 == 0x01000000:
        output += ''
#
# 64-bit ABIs.
#
        if cputype & 0xffffff == 0:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 1:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 2:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 3:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 4:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 5:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 6:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 7:
            output += 'x86_64'
            if cpusubtype & 0xffffff == 0:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 1:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 2:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
            if cpusubtype & 0xffffff == 3:
                output += ''
            if cpusubtype & 0xffffff == 4:
                output += '_arch1'
            if cpusubtype & 0xffffff == 8:
                output += '_haswell'
            if cpusubtype & 0xffffff > 4:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff == 8:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 9:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 10:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 11:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 12:
            output += 'arm64'
            if cpusubtype & 0xffffff == 0:
                output += ''
            if cpusubtype & 0xffffff == 1:
                output += 'v8'
        if cputype & 0xffffff == 13:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 14:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 15:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 16:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 17:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
        if cputype & 0xffffff == 18:
            output += 'ppc64'
            if cpusubtype & 0xffffff == 0:
                output += ''
            if cpusubtype & 0xffffff == 1:
                output += '_601'
            if cpusubtype & 0xffffff == 2:
                output += '_602'
            if cpusubtype & 0xffffff == 3:
                output += '_603'
            if cpusubtype & 0xffffff == 4:
                output += '_603e'
            if cpusubtype & 0xffffff == 5:
                output += '_603ev'
            if cpusubtype & 0xffffff == 6:
                output += '_604'
            if cpusubtype & 0xffffff == 7:
                output += '_604e'
            if cpusubtype & 0xffffff == 8:
                output += '_620'
            if cpusubtype & 0xffffff == 9:
                output += '_650'
            if cpusubtype & 0xffffff == 10:
                output += '_7400'
            if cpusubtype & 0xffffff == 11:
                output += '_7450'
            if cpusubtype & 0xffffff == 100:
                output += '_970'
            if cpusubtype & 0xffffff > 100:
                output += 'subarchitecture=%d' % (cpusubtype & 0xffffff)
        if cputype & 0xffffff > 18:
            output += '64-bit architecture=%d' % (cputype & 0xffffff)
    return output
