#!/usr/bin/env python3
import sys
    
from version import __version__
from helpers import *
from errors import *
from baseagent import *
from debug import *
from holon import *
from listener import *



'''
Penguin ASCII art by apx stolen from:
http://www.ascii-art.de/ascii/pqr/penguins.txt
'''

splash = '''
                             ;
                         ('>-'
                        //-\\
                        (\_/)
                         ~ ~  
------------------------------------------------------------
Awkward π-nguin %s : Microservice orchestration language
------------------------------------------------------------
''' % __version__

def process( lexer ):
    lexer.recover = lambda x: sys.exit()
    stream = CommonTokenStream( lexer )
    parser = APiParser( stream )
    tree = parser.api_program()
    printer = APi()
    walker = ParseTreeWalker()
    walker.walk( printer, tree )
    
    return printer.get_ns()

def read_from_stdin():
    print( splash )
    lexer = APiLexer( StdinStream() )
    return process( lexer )

def read_specification_from_file(fl):
    stream = FileStream( fl, encoding='utf-8' )
    lexer = APiLexer( stream )
    return process( lexer )


def read_specification_files_recursively(fl, spec_by_holon = {}):
    hn = fl.replace('.api', '')
    ns = read_specification_from_file(fl)
    holons = ns['holons']
    spec_by_holon[hn] = ns

    for holon in holons:
        spec_by_holon = read_specification_files_recursively(f'{holon}.api', spec_by_holon)

    return spec_by_holon

def generate_namespaces():
    if len( sys.argv ) > 2:
        print( 'Usage: APi [filename.api]' )
    else:
        if len( sys.argv ) == 2:
            return read_specification_files_recursively(sys.argv[ 1 ])
        else:
            # the problem is that by specifying specification on stdin, we don't know the name of the holon
            print("Not supported at this itme")
            # return read_from_stdin()    
            
BYE = 'Bye!'
def initialize():
    global BYE
    BYE = random.choice( [ i.strip().title() for i in open( 'bye.txt' ).readlines() ][ 1: ] )
    if not os.path.exists( TMP_FOLDER ):
        os.makedirs( TMP_FOLDER )
                    
if __name__ == '__main__':
    initialize()

    # TESTING
    os.chdir('test')
    
    ns = generate_namespaces()
    holon_names = list(ns.keys())
    rs = APiRegistrationService( 'api-test' ) # should make sure that the name is lowercase
    holons_addressbook = {}
    for holon in holon_names:
        h1name, h1password = rs.register( holon )
        holons_addressbook[holon] = {"address": h1name, "password":h1password}

    for holon, namespace in ns.items():
        agents = namespace.get("agents", [])
        channels = namespace.get("channels", [])
        environment = namespace.get("environment", [])
        execution_plans = namespace.get("execution_plans")        
        holons = namespace.get("holons", [])
        holon_addresses = {ch: holons_addressbook[ch]['address'] for ch in holons}
        
        creds = holons_addressbook[holon]    
        h = APiHolon( holon, creds['address'], creds['password'], agents, channels, environment, holon_addresses, execution_plans )
        h.start()

    input("Press enter to interrupt")

    spade.quit_spade()

