import re
import xmltodict
from src.agents.base.base_talking_agent import APiTalkingAgent
from spade.behaviour import OneShotBehaviour
from copy import deepcopy
from pyxf.pyxf import swipl
import socket
import nclib
from src.utils.logger import setup_logger

logger = setup_logger("base_channel_agent")


class APiBaseChannel(APiTalkingAgent):
    REPL_STR = '"$$$API_THIS_IS_VARIABLE_%s$$$"'

    def __init__(
        self,
        channelname,
        name,
        password,
        holon,
        token,
        portrange,
        channel_input=None,
        channel_output=None,
    ):
        global logger
        logger = setup_logger("channel " + channelname)

        self.channelname = channelname
        self.holon = holon
        super().__init__(name, password, token)

        self.kb = swipl()
        self.var_re = re.compile(r"[\?][a-zA-Z][a-zA-Z0-9-_]*")

        self.min_port, self.max_port = portrange

        self.input = channel_input
        self.output = channel_output

        self.socket_clients = {}

        # TODO: return map function based on channel_input/output
        # descriptor (can be JSON, XML, REGEX, TRANSFORMER, TRANSPARENT)
        # * JSON -> JSON input or output
        # XML -> XML input or output
        # * REGEX -> Python style regex (with named groups) input
        # TRANSFORMER -> read definition from channel description (.cd) file
        # * TRANSPARENT -> no mapping needed, just forward
        #
        # * -> Done!

        if self.input is None or self.output is None:
            self.map = lambda x: x
        else:
            if self.input.startswith("regex("):
                reg = self.input[6:-1]
                self.input_re = re.compile(reg)
                self.map = self.map_re
            elif self.input.startswith("json("):
                self.input_json = self.input[5:-1]
                self.kb.query("use_module(library(http/json))")
                cp = self.input_json
                replaces = {}
                for var in self.var_re.findall(self.input_json):
                    rpl = self.REPL_STR % var
                    replaces[rpl[1:-1]] = var
                    cp = cp.replace(var, rpl)
                query = (
                    " APIRES = ok, open_string( '%s', S ), json_read_dict( S, X ). "
                    % cp
                )
                res = self.kb.query(query)
                prolog_json = res[0]["X"]
                for k, v in replaces.items():
                    prolog_json = prolog_json.replace(k, "X" + v[1:])

                self.input_json = prolog_json

                self.map = self.map_json
            elif self.input.startswith("xml("):
                self.input_xml = self.input[4:-1]
                cp = self.input_xml
                replaces = {}
                for var in self.var_re.findall(self.input_xml):
                    rpl = self.REPL_STR % var
                    replaces[rpl[1:-1]] = var
                    cp = cp.replace(var, rpl)

                for k, v in replaces.items():
                    input_xml = cp.replace(k, "X" + v[1:])

                input_xml = xmltodict.parse(input_xml)
                self.input_xml = (
                    str(input_xml).replace(" ", "").replace("'", "").replace("@", "")
                )

                self.map = self.map_xml

    def map(self, data):
        pass

    def map_re(self, data):
        match = self.input_re.match(data)
        vars = self.input_re.groupindex.keys()
        results = {}
        if not match:
            return ""
        for i in vars:
            results[i] = match.group(i)
        query = ""
        for var, val in results.items():
            query += "X" + var + " = '" + val + "', "
        query = "APIRES = ok, " + query[:-2]
        res = self.kb.query(query)

        return self.format_output(res)

    def format_output(self, res):
        output = self.output

        if self.output.startswith("json("):
            output = self.output[5:-1]
        elif self.output.startswith("xml("):
            output = self.output[4:-1]

        for var, val in res[0].items():
            output = output.replace("?" + var[1:], val)

        return output

    def map_json(self, data):
        try:
            query = (
                " APIRES = ok, open_string( '%s', S ), json_read_dict( S, X ). " % data
            )
            res = self.kb.query(query)
            prolog_json = res[0]["X"]
            query = " APIRES = ok, X = %s, Y = %s, X = Y. " % (
                prolog_json,
                self.input_json,
            )
            res = self.kb.query(query)
            del res[0]["X"]
            del res[0]["Y"]
            return self.format_output(res)
        except:
            return ""

    def map_xml(self, data):
        try:
            data = xmltodict.parse(data)
            data = str(data).replace(" ", "").replace("'", "").replace("@", "")

            query = " APIRES = ok, X = %s, Y = %s, X = Y. " % (data, self.input_xml)
            res = self.kb.query(query)

            del res[0]["X"]
            del res[0]["Y"]
            return self.format_output(res)
        except:
            return ""

    def get_server_clients(self, server, ref_var_name, protocol):
        if protocol == "udp":
            for _, client in server:
                self.socket_clients[ref_var_name].append(client)
        else:
            for client in server:
                self.socket_clients[ref_var_name].append(client)

    def get_free_port(self, protocol):
        """Get a free port on the host"""
        if protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(type=socket.SOCK_DGRAM)
        port = self.min_port
        while port <= self.max_port:
            try:
                sock.bind(("", port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError("No free ports in range %d - %d" % (self.min_port, self.max_port))

    def get_ip(self):
        """Get the current IP address of the agent"""
        # TODO: Verify this works with outside network
        #       addresses!
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(("10.255.255.255", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def create_server(self, port, protocol):
        if protocol == "udp":
            srv = nclib.UDPServer(("0.0.0.0", port))
            srv.sock.bind(("0.0.0.0", port))
            return srv

        return nclib.TCPServer(("0.0.0.0", port))

    def get_server(self, protocol):
        """Get a NetCat server for sending or receiving"""
        port = self.get_free_port(protocol)
        host = self.get_ip()

        self.say(host, port)

        srv_created = False
        while not srv_created:
            try:
                srv = self.create_server(port, protocol)
                srv_created = True
                logger.info(f"{protocol.upper()} server created at port {port}")
            except OSError as e:
                logger.error(f"Error starting socket server: {e} at port {port}")
                port = self.get_free_port(protocol)

        return srv, host, str(port), protocol

    class StatusListening(OneShotBehaviour):
        async def run(self):
            metadata = deepcopy(self.agent.inform_msg_template)
            metadata["status"] = "listening"
            await self.agent.schedule_message(self.agent.holon, metadata=metadata)
