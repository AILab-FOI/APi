#!/usr/bin/env python3

from APi import APiAgent
import json
import argparse

def main( name, address, password, holon, token, args, flows ):
    args = json.loads( args )
    flows = json.loads( flows )
    flows = [ ( i[ 0 ], i[ 1 ] ) for i in flows ]
    a = APiAgent( name, address, password, holon, token, args, flows )
    a.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='APi agent.')
    parser.add_argument( 'name', metavar='NAME', type=str, help="Agent's local APi name" )
    parser.add_argument( 'address', metavar='ADDRESS', type=str, help="Agent's XMPP/JID address" )
    parser.add_argument( 'password', metavar='PWD', type=str, help="Agent's XMPP/JID password" )
    parser.add_argument( 'holon', metavar='HOLON', type=str, help="Agent's instantiating holon's XMPP/JID address" )
    parser.add_argument( 'token', metavar='TOKEN', type=str, help="Agent's security token" )
    parser.add_argument( 'args', metavar='ARGS', type=str, help="Agent's instantiation arguments" )
    parser.add_argument( 'flows', metavar='FLOWS', type=str, help="Agent's communication flows" )

    args = parser.parse_args()
    main( args.name, args.address, args.password, args.holon, args.token, args.args, args.flows )
