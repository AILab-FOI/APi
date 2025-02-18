import xmltodict
import re
from pyxf.pyxf import swipl


def main(input_xml: str, data: str):
    var_re = re.compile(r"[\?][a-zA-Z][a-zA-Z0-9-_]*")
    REPL_STR = '"$$$API_THIS_IS_VARIABLE_%s$$$"'
    kb = swipl()

    cp = input_xml
    replaces = {}
    for var in var_re.findall(input_xml):
        rpl = REPL_STR % var
        replaces[rpl[1:-1]] = var
        cp = cp.replace(var, rpl)

    for k, v in replaces.items():
        input_json = cp.replace(k, "X" + v[1:])

    input_json = xmltodict.parse(input_json)
    input_json = str(input_json).replace(" ", "").replace("'", "").replace("@", "")

    data = xmltodict.parse(data)
    data = str(data).replace(" ", "").replace("'", "").replace("@", "")

    query = " APIRES = ok, X = %s, Y = %s, X = Y. " % (data, input_json)
    res = kb.query(query)

    del res[0]["X"]
    del res[0]["Y"]

    output = "abc abc ?var"

    for var, val in res[0].items():
        output = output.replace("?" + var[1:], val)

    print(output)


if __name__ == "__main__":
    input_xml = "<Abc test=?var />"
    data = '<Abc test="123" />'

    main(input_xml, data)
