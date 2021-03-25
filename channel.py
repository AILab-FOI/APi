#!/usr/bin/env python3

from APi import APiChannel
import json
import argparse

def main( name, address, password, holon, token, portrange, input, output, transformer ):
    portrange = json.loads( portrange )
    input = json.loads( input )
    output = json.loads( output )
    transformer = json.loads( transformer )
    a = APiChannel( name, address, password, holon, token, portrange, channel_input=input, channel_output=output, transformer=transformer )
    a.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='APi agent.')
    parser.add_argument( 'name', metavar='NAME', type=str, help="Channel's local APi name" )
    parser.add_argument( 'address', metavar='ADDRESS', type=str, help="Channel's XMPP/JID address" )
    parser.add_argument( 'password', metavar='PWD', type=str, help="Channel's XMPP/JID password" )
    parser.add_argument( 'holon', metavar='HOLON', type=str, help="Channel's instantiating holon's XMPP/JID address" )
    parser.add_argument( 'token', metavar='TOKEN', type=str, help="Channel's security token" )
    parser.add_argument( 'portrange', metavar='PORTRANGE', type=str, help="Channel's port range" )
    parser.add_argument( 'input', metavar='INPUT', type=str, help="Channel's input specification" )
    parser.add_argument( 'output', metavar='OUTPUT', type=str, help="Channel's output specification" )
    parser.add_argument( 'transformer', metavar='TRANSFORMER', type=str, help="Channel's transformer specification" )

    args = parser.parse_args()
    main( args.name, args.address, args.password, args.holon, args.token, args.portrange, args.input, args.output, args.transformer )
