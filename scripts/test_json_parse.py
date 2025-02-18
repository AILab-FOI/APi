import re
from pyxf.pyxf import swipl


def main(input_json: str, data: str):
    var_re = re.compile(r"[\?][a-zA-Z][a-zA-Z0-9-_]*")
    REPL_STR = '"$$$API_THIS_IS_VARIABLE_%s$$$"'
    kb = swipl()

    # setup input
    kb.query("use_module(library(http/json))")
    cp = input_json
    replaces = {}
    for var in var_re.findall(input_json):
        rpl = REPL_STR % var
        replaces[rpl[1:-1]] = var
        cp = cp.replace(var, rpl)
    query = " APIRES = ok, open_string( '%s', S ), json_read_dict( S, X ). " % cp
    res = kb.query(query)
    prolog_json = res[0]["X"]
    for k, v in replaces.items():
        prolog_json = prolog_json.replace(k, "X" + v[1:])

    input_json = prolog_json

    # process
    query = " APIRES = ok, open_string( '%s', S ), json_read_dict( S, X ). " % data
    res = kb.query(query)
    prolog_json = res[0]["X"]
    query = " APIRES = ok, X = %s, Y = %s, X = Y. " % (prolog_json, input_json)
    res = kb.query(query)
    del res[0]["X"]
    del res[0]["Y"]

    output = "abc abc ?var"

    for var, val in res[0].items():
        output = output.replace("?" + var[1:], val)

    print(output)


if __name__ == "__main__":
    input_json = '{"some": ?var}'
    data = '{"some": 123}'

    main(input_json, data)
