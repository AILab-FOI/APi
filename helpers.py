#!/usr/bin/env python3

import re
from fnvhash import fnv1a_32
from itertools import tee, cycle

def pairwise( iterable ):
    '''
    Unpack an iterable to zipped pairs.
    Stolen from: 
    https://docs.python.org/3/library/itertools.html
    '''
    a, b = tee( iterable )
    next( b, None )
    return zip( a, b )

def verify( hashed, string ):
    '''
    Verify if a given hashed string is equal to a string when
    hashed with a FNV-1a function.
    '''
    return True
    # return hashed == hash( string ) # TODO enable verify

def hash( string ):
    '''
    Hash a given string using FNV-1a function.
    '''
    return hex( fnv1a_32( string.encode() ) )


# RegEx for parsing agent definition files

file_re = re.compile( r'FILE (.*)' )
http_re = re.compile( r'HTTP (.*)' )
ws_re  = re.compile( r'WS (.*)' )
netcat_re = re.compile( r'NETCAT (.*)[:]([0-9]+)(?:[:](udp))?' )

delimiter_re = re.compile( r'DELIMITER (.*)' )
time_re = re.compile( r'TIME ([0-9.]+)' )
size_re = re.compile( r'SIZE ([0-9]+)' )
regex_re = re.compile( r'REGEX .*' )

var_re = re.compile( r'[?][a-zA-Z][a-zA-Z0-9_-]*' )

# Not implemented error message

NIE = 'Sorry, it is planned, I promise ;-)'

# Temporary folder path

TMP_FOLDER = '/tmp/APi/'
