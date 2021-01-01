#!/usr/bin/env python3

import re
vre = re.compile( '([0-9][.][0-9][.][0-9])' )

vstr = '__version__ = %d.%d.%d\n'

def main():
    vf = open( 'version.py' )
    v = vf.readlines()
    vf.close()
    ver = [ i for i in v if '__version__' in i ][ 0 ]
    vn = vre.findall( ver )[ 0 ]
    v1, v2, v3 = [ int( i ) for i in vn.split( '.' ) ]
    if v3 == 9:
        v3 = 0
        if v2 == 9:
            v2 = 0
            v1 += 1
        else:
            v2 +=1
    else:
        v3 += 1

    vf = open( 'version.py', 'w' )
    vf.write( vstr % ( v1, v2, v3 ) )
    vf.close()
    

if __name__ == '__main__':
    main()
