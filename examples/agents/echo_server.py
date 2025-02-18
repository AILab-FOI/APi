#!/usr/bin/env python3

from flask import Flask
import sys

app = Flask(__name__)


@app.route("/<msg>")
def echo(msg):
    return msg


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2709)
