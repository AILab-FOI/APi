import sys
import os

from src.agents.holon import APiHolon
from src.grammar.listener import APi
from src.grammar.APiLexer import APiLexer
from src.grammar.APiParser import APiParser
from src.orchestration.registrar import APiRegistrationService
from src.config.settings import settings
from antlr4 import CommonTokenStream, ParseTreeWalker, StdinStream, FileStream
import spade

_ORCHESTRATION_FILE_NAME_TEMPLATE = "{file_name}.api"

SPLASH = """
                             ;
                         ('>-'
                        //-\\
                        (\_/)
                         ~ ~  
------------------------------------------------------------
Awkward π-nguin : Microservice orchestration language
------------------------------------------------------------
"""


def process(lexer):
    lexer.recover = lambda x: sys.exit()
    stream = CommonTokenStream(lexer)
    parser = APiParser(stream)
    tree = parser.api_program()
    printer = APi()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    return printer.get_ns()


def read_from_stdin():
    print(SPLASH)
    lexer = APiLexer(StdinStream())
    return process(lexer)


def read_specification_from_file(fl):
    stream = FileStream(fl, encoding="utf-8")
    lexer = APiLexer(stream)
    return process(lexer)


def read_specification_files_recursively(fl, spec_by_holon={}):
    hn = fl.replace(".api", "")
    ns = read_specification_from_file(fl)
    hn = hn.replace("orchestration_specifications/", "")
    holons = ns.holons
    spec_by_holon[hn] = ns

    for holon in holons:
        spec_by_holon = read_specification_files_recursively(
            "orchestration_specifications/"
            + _ORCHESTRATION_FILE_NAME_TEMPLATE.format(file_name=holon),
            spec_by_holon,
        )

    return spec_by_holon


def generate_namespaces(configuration_name: str):
    file_name = _ORCHESTRATION_FILE_NAME_TEMPLATE.format(file_name=configuration_name)
    file_name = "orchestration_specifications/" + file_name
    return read_specification_files_recursively(file_name)


def extract_orchestration_specification_name():
    if len(sys.argv) > 2:
        print("Usage: APi [filename.api]")
    else:
        if len(sys.argv) == 2:
            file_name = sys.argv[1]
            splits = file_name.split(".")
            return splits[0]
        else:
            print("Not supported at this time")


if __name__ == "__main__":
    # set working directory to test folder
    os.chdir(settings.examples_dir)

    orchestration_specification_name = extract_orchestration_specification_name()
    if not orchestration_specification_name:
        exit()

    ns = generate_namespaces(orchestration_specification_name)
    holon_names = list(ns.keys())

    rs = APiRegistrationService(orchestration_specification_name)

    holons_addressbook = {}
    for holon in holon_names:
        h1name, h1password = rs.register(holon)
        holons_addressbook[holon] = {"address": h1name, "password": h1password}

    for holon, namespace in ns.items():
        agents = namespace.agents
        channels = namespace.channels
        environment = namespace.environment
        execution_plans = namespace.execution_plans
        holons = namespace.holons
        holon_addresses = {ch: holons_addressbook[ch]["address"] for ch in holons}

        creds = holons_addressbook[holon]
        h = APiHolon(
            holon,
            creds["address"],
            creds["password"],
            agents,
            channels,
            environment,
            holon_addresses,
            execution_plans,
        )
        h.start()

    input("Press enter to interrupt")

    spade.quit_spade()
