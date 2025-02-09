import sys
from antlr4 import CommonTokenStream, ParseTreeWalker, StdinStream, FileStream
from src.grammar.APiLexer import APiLexer
from src.grammar.APiParser import APiParser
from src.grammar.listener import APi
import os


def process(lexer):
    lexer.recover = lambda x: sys.exit()
    stream = CommonTokenStream(lexer)
    parser = APiParser(stream)
    tree = parser.api_program()
    printer = APi()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    try:
        print(printer.get_ns())
    except Exception as e:
        print(str(e))


def main(dir: str):
    os.chdir(dir)
    if len(sys.argv) != 2:
        lexer = APiLexer(StdinStream())
        process(lexer)
    else:
        if len(sys.argv) == 2:
            fl = sys.argv[1]
            stream = FileStream(fl, encoding="utf-8")
            lexer = APiLexer(stream)
            process(lexer)


if __name__ == "__main__":
    examples_dir = "examples"
    main(examples_dir)
