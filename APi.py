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

def process( stream ):
    lexer = APiLexer( stream )
    lexer.recover = lambda x: sys.exit()
    stream = CommonTokenStream( lexer )
    parser = APiParser( stream )
    tree = parser.api_program()
    printer = APi()
    walker = ParseTreeWalker()
    walker.walk( printer, tree )
    try:
        return parser.STACK[ -1 ]
    except:
        pass # TODO: remove exception handling when all parts of parser are implemented
    

BYE = 'Bye!'
def main():
    if len( sys.argv ) > 2:
        print( 'Usage: APi [filename.api]' )
    else:
        if len( sys.argv ) == 2:
            fl = sys.argv[ 1 ]
            stream = FileStream( fl, encoding='utf-8' )
            process( stream )            
        else:
            print( splash )
            while True:
                try:
                    command = input( "Aπ :- " )
                except:
                    print( '\n%s!' % BYE )
                    quit_spade()
                    sys.exit()
                
                if command == "exit":
                    print( '%s!' % BYE )
                    quit_spade()
                    break
                elif command == '':
                    continue
                elif command.strip()[ -1 ] == ':':
                    line = input( '|' )
                    command += '\n' + line
                    while line[ 0 ] == '\t':
                        line = input( '|' )
                        command += '\n' + line
                        if not line:
                            break
                    
                if command:
                    stream = InputStream( command + '\n' )
                    process( stream )

def initialize():
    global BYE
    BYE = random.choice( [ i.strip().title() for i in open( 'bye.txt' ).readlines() ][ 1: ] )
    if not os.path.exists( TMP_FOLDER ):
        os.makedirs( TMP_FOLDER )
                    
if __name__ == '__main__':
    initialize()
    ns = APiNamespace()

    # TESTING
    os.chdir('test')
    rs = APiRegistrationService( 'APi-test' )
    #a1, a1pass = rs.register( 'ivek' )
    #a2, a2pass = rs.register( 'joza' )
    #c1, c1pass = rs.register( 'stefica' )

    #a = APiAgent( 'bla_stdin_stdout', a1 + '@rec.foi.hr', a1pass, flows=[ ( 'self', 'c' ) ] )
    #b = APiAgent( 'bla_stdin_ws', a2 + '@rec.foi.hr', a2pass, flows=[ ( 'c', 'self' ) ] )
    #c = APiChannel( 'c', c1 + '@rec.foi.hr', c1pass, channel_input='regex( x is (?P<act>[0-9]+) )', channel_output="{ 'action':?act, 'history':?act }" )

    #ns[ 'agents' ][ 'a' ] = a
    #ns[ 'agents' ][ 'b' ] = b
    #ns[ 'channels' ][ 'c' ] = c

    #c.start()

    h1name, h1password = rs.register( 'holonko1' )
    agents = [ { 'name':'bla_stdin_stdout', 'flows':[ ( 'c', 'self' ), ( 'self', 'd' ), ( 'self', 'holonko1', 'io-1' ) ], 'args':{'protocol': 'tcp'} }, { 'name':'bla_stdin_http', 'flows':[ ( 'd', 'self' ) ], 'args':{'protocol': 'tcp'} }, { 'name':'bla_file_stdout', 'flows':[ ( 'self', 'c' ) ], 'args':{'protocol': 'tcp'} } ]
    channels = [ { 'name':'c', 'input':'regex( (?P<act>.*) )', 'output':"?act", 'transformer':None }, { 'name':'d', 'input':'regex( (?P<act>.*) )', 'output':"{ 'action':'?act', 'history':'?act' }", 'transformer':None } ]
    environment = [ { 'name': 'io-1', 'input': "{ 'val1': ?x }", 'output': "{ 'val2': ?y }" } ]
    holons = []
    execution_plan = None
    print( h1name )
    h1 = APiHolon( 'holonko1', h1name, h1password, agents, channels, environment, holons, execution_plan )
    h1.start()
    

    
    #a = APiAgent( 'bla_ws_ws', 'bla0agent@dragon.foi.hr', 'tajna', flows=[ ('a', 'self'), ('self', 'c'), ('d', 'e', 'NIL'), ('b','VOID') ] ) # ('STDIN', 'self'),  ('self', 'STDOUT'),

    
    '''
    sleep( 1 )
    a.input( 'avauhu\nguhu\nbuhu\nwuhu\ncuhu\n' )
    sleep( 1 )
    a.input( 'juhu\n' )
    sleep( 1 )
    a.input( 'muhu\n' )
    a.input( 'ahu\n' )
    sleep( 1 )
    a.input( 'puhu\nluhu\n' )
    sleep( 1 )
    a.input( '<!eof!>' )'''
    
    #a.start_shell_client( await_stdin=True, print_stdout=True, print_stderr=True )
    

    #c = APiChannel( 'test', 'bla0agent@dragon.foi.hr', 'tajna', channel_input='regex( x is (?P<act>[0-9]+) )', channel_output="{ 'action':?act, 'history':?act }" )

    #print( c.map( 'x is 247 blakaka x is 222121' ) )

    #c = APiChannel( 'test', 'bla0agent@dragon.foi.hr', 'tajna', channel_input='json( { "gugu":?y, "bla":?x } )', channel_output='<bla><nana x="?x" /><y>?y</y></bla>' )

    #c.start()
    
    #print( c.map( '{ "bla":234, "gugu":1 }' ) )

    
    #c = APiChannel( 'test', 'bla0agent@dragon.foi.hr', 'tajna' ) # TRANSPARENT CHANNEL

    #print( c.map( '{ "bla":234, "gugu":1 }' ) ) 
    
    
    print( ns )

    
    main()
    
    spade.quit_spade()

