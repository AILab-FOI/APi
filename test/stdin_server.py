#!/usr/bin/env python3

from flask import Flask
import sys
import fileinput

app = Flask( __name__ )
acc = []

@app.route('/')
def echo_stdin():
    global acc
    print( acc )
    return '<br />'.join( acc )

if __name__ == '__main__':
    
    
    for line in fileinput.input():
        acc.append( line )
        
    app.run( host="0.0.0.0", port=2709 )
