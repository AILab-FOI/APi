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
    

BYE = 'Bye!'
def generate_namespace():
    if len( sys.argv ) > 2:
        print( 'Usage: APi [filename.api]' )
    else:
        ns = None

        if len( sys.argv ) == 2:
            fl = sys.argv[ 1 ]
            stream = FileStream( fl, encoding='utf-8' )
            lexer = APiLexer( stream )
            ns = process( lexer )
        else:
            print( splash )
            lexer = APiLexer( StdinStream() )
            ns = process( lexer )

        return ns
            
            

def initialize():
    global BYE
    BYE = random.choice( [ i.strip().title() for i in open( 'bye.txt' ).readlines() ][ 1: ] )
    if not os.path.exists( TMP_FOLDER ):
        os.makedirs( TMP_FOLDER )
                    
if __name__ == '__main__':
    initialize()

    # TESTING
    os.chdir('test')
    
    # ns = generate_namespace()
    # agents = ns.get("agents", [])
    # channels = ns.get("channels", [])
    # holons = ns.get("holons", [])
    # environment = ns.get("environment", [])
    # execution_plan = None

    # print(ns)

    rs = APiRegistrationService( 'APi-test' )
    h1name, h1password = rs.register( 'holonko1' )

    
    agents = [ 
        { 
            'name':'bla_stdin_stdout', 
            # 'flows':[ ( 'c', 'self' ), ( 'self', 'd' ), ( 'self', 'holonko1', 'io-1' ) ], 
            'flows':[ ( 'c', 'self' ) ], 
            # 'flows':[ ( 'self', 'c' ) ], 
            # 'args':{'protocol': 'tcp'} 
            'args': {},
        }, 
        # { 
        #     'name':'bla_stdin_http', 
        #     'flows':[ ( 'd', 'self' ) ], 
        #     'args':{'protocol': 'tcp'} 
        # }, 
        {
            'name':'bla_file_stdout', 
            'flows':[ ( 'self', 'c' ) ], 
            'args': {},
            # 'args':{'protocol': 'tcp'} 
        } 
    ]
    channels = [ 
        { 
            'name':'c', 
            # 'input':'regex( (?P<act>.*) )', 
            # 'output':"?act", 
            'input': None,
            'output': None,
            'transformer': "'test' + x"
        }, 
        # { 
        #     'name':'d', 
        #     # 'input':'regex( (?P<act>.*) )', 
        #     # 'output':"{ 'action':'?act', 'history':'?act' }", 
        #     'input':'regex( (?P<act>.*) )', 
        #     'output':"?act", 
        #     'transformer':None 
        # } 
    ]
    environment = [ 
        { 
            'name': 'io-1', 
            'input': "{ 'val1': ?x }", 
            'output': "{ 'val2': ?y }" 
            } 
        ]
    
    holons = []
    execution_plan = ['bla_file_stdout bla_stdin_stdout']

    h1 = APiHolon( 'holonko1', h1name, h1password, agents, channels, environment, holons, execution_plan )
    h1.start()
    
    input("Press enter to interrupt")

    spade.quit_spade()

