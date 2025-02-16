#!/usr/bin/env python3

from flask import Flask, request
import sys
import logging
import click

app = Flask(__name__)

# Disable console logging
log = logging.getLogger("werkzeug")
log.disabled = True


def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass


def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass


click.echo = echo
click.secho = secho


@app.route("/<msg>")
def echo(msg):
    if msg == "<!eof!>":
        try:
            func = request.environ.get("werkzeug.server.shutdown")
            func()
        except Exception as e:
            print("err", e)
    else:
        print(msg, file=sys.stdout)
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2709)
