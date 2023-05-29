#!/usr/bin/env python3
from namespace import *
from APiLexer import APiLexer
from APiListener import APiListener
from APiParser import APiParser
from antlr4 import *

class APi( APiListener ):
    '''
    APi main listener.
    '''
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.ns = APiNamespace()
        self.STACK = []
        self.PARSING_XML = False

    def get_ns( self ):
        return self.ns


    # Enter a parse tree produced by APiParser#api_program.
    def enterApi_program(self, ctx:APiParser.Api_programContext):
        pass

    # Exit a parse tree produced by APiParser#api_program.
    def exitApi_program(self, ctx:APiParser.Api_programContext):
        pass


    # Enter a parse tree produced by APiParser#s_environment.
    def enterS_environment(self, ctx:APiParser.S_environmentContext):
        pass

    # Exit a parse tree produced by APiParser#s_environment.
    def exitS_environment(self, ctx:APiParser.S_environmentContext):
        output = self.STACK.pop()
        input = self.STACK.pop()
        environment = { "input": input, "output": output }
        self.ns.add_environment(environment)

    # Enter a parse tree produced by APiParser#s_environment_forward.
    def enterS_environment_forward(self, ctx:APiParser.S_environment_forwardContext):
        pass

    # Exit a parse tree produced by APiParser#s_environment_forward.
    def exitS_environment_forward(self, ctx:APiParser.S_environment_forwardContext):
        environment = { "input": None, "output": None }
        self.ns.add_environment(environment)



    # Enter a parse tree produced by APiParser#iflow.
    def enterIflow(self, ctx:APiParser.IflowContext):
        input = ctx.children[5].getText()
        self.STACK.append( input )

    # Exit a parse tree produced by APiParser#iflow.
    def exitIflow(self, ctx:APiParser.IflowContext):
        pass


    # Enter a parse tree produced by APiParser#oflow.
    def enterOflow(self, ctx:APiParser.OflowContext):
        output = ctx.children[5].getText()
        self.STACK.append( output )

    # Exit a parse tree produced by APiParser#oflow.
    def exitOflow(self, ctx:APiParser.OflowContext):
        pass


    # Enter a parse tree produced by APiParser#s_start.
    def enterS_start(self, ctx:APiParser.S_startContext):
        plans = "".join([child.getText() for child in ctx.children[2:]]).strip()
        self.ns.add_execution_plan( plans )

    # Exit a parse tree produced by APiParser#s_start.
    def exitS_start(self, ctx:APiParser.S_startContext):
        pass


    # Enter a parse tree produced by APiParser#pi_expr.
    def enterPi_expr(self, ctx:APiParser.Pi_exprContext):
        pass

    # Exit a parse tree produced by APiParser#pi_expr.
    def exitPi_expr(self, ctx:APiParser.Pi_exprContext):
        pass


    # Enter a parse tree produced by APiParser#s_agent.
    def enterS_agent(self, ctx:APiParser.S_agentContext):
        pass

    # Exit a parse tree produced by APiParser#s_agent.
    def exitS_agent(self, ctx:APiParser.S_agentContext):
        a_name = ctx.children[2].getText()

        flows = []
        args = None

        while (len(self.STACK)):
            exp = self.STACK.pop()
            type = exp['type']
            value = exp['value']

            if type == "flow":
                flows.append(value)
            else:
                args = value

        agent = {"name": a_name, "args": args, "flows": flows}
        self.ns.add_agent(agent)


    # Enter a parse tree produced by APiParser#arglist.
    def enterArglist(self, ctx:APiParser.ArglistContext):
        args_str = "".join([child.getText() for child in ctx.children[1:-1]]).strip()
        args = args_str.split(" ")
        self.STACK.append({"type": "args", "value": args})

    # Exit a parse tree produced by APiParser#arglist.
    def exitArglist(self, ctx:APiParser.ArglistContext):
        pass


    # Enter a parse tree produced by APiParser#aflow.
    def enterAflow(self, ctx:APiParser.AflowContext):
        from_a = ctx.children[1].getText()
        to_a = ctx.children[5].getText()
        self.STACK.append({"type": "flow", "value": (from_a, to_a)})

    # Exit a parse tree produced by APiParser#aflow.
    def exitAflow(self, ctx:APiParser.AflowContext):
        pass


    # Enter a parse tree produced by APiParser#valid_channel.
    def enterValid_channel(self, ctx:APiParser.Valid_channelContext):
        pass

    # Exit a parse tree produced by APiParser#valid_channel.
    def exitValid_channel(self, ctx:APiParser.Valid_channelContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel.
    def enterS_channel(self, ctx:APiParser.S_channelContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel.
    def exitS_channel(self, ctx:APiParser.S_channelContext):
        channel_name = ctx.children[ 2 ].getText()
        input, protocol_symbol, output = self.STACK.pop()
        protocol = "tcp" if protocol_symbol == '-->' else "udp"
        channel = { 'name': channel_name, 'input': input, 'output': output, 'protocol': protocol }
        self.ns.add_channel(channel)


    # Enter a parse tree produced by APiParser#s_channel_forward.
    def enterS_channel_forward(self, ctx:APiParser.S_channel_forwardContext):
        channel_name = ctx.children[ 2 ].getText()
        channel = { 'name': channel_name, 'input': None, 'output': None, 'protocol': 'tcp' } # TODO: default to TCP
        self.ns.add_channel(channel)

    # Exit a parse tree produced by APiParser#s_channel_forward.
    def exitS_channel_forward(self, ctx:APiParser.S_channel_forwardContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel_spec.
    def enterS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        input = ctx.children[1].getText()
        protocol = ctx.children[3].getText()
        output = ctx.children[5].getText()
        self.STACK.append((input, protocol, output))

    # Exit a parse tree produced by APiParser#s_channel_spec.
    def exitS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        pass


    # Enter a parse tree produced by APiParser#s_import.
    def enterS_import(self, ctx:APiParser.S_importContext):
        pass

    # Exit a parse tree produced by APiParser#s_import.
    def exitS_import(self, ctx:APiParser.S_importContext):
        holon = ctx.children[2].getText()
        self.ns.add_holon(holon)


    # Enter a parse tree produced by APiParser#s_input.
    def enterS_input(self, ctx:APiParser.S_inputContext):
        pass

    # Exit a parse tree produced by APiParser#s_input.
    def exitS_input(self, ctx:APiParser.S_inputContext):
        pass


    # Enter a parse tree produced by APiParser#s_output.
    def enterS_output(self, ctx:APiParser.S_outputContext):
        pass

    # Exit a parse tree produced by APiParser#s_output.
    def exitS_output(self, ctx:APiParser.S_outputContext):
        pass


    # Enter a parse tree produced by APiParser#s_xml.
    def enterS_xml(self, ctx:APiParser.S_xmlContext):
        pass

    # Exit a parse tree produced by APiParser#s_xml.
    def exitS_xml(self, ctx:APiParser.S_xmlContext):
        pass


    # Enter a parse tree produced by APiParser#s_json.
    def enterS_json(self, ctx:APiParser.S_jsonContext):
        pass

    # Exit a parse tree produced by APiParser#s_json.
    def exitS_json(self, ctx:APiParser.S_jsonContext):
        pass


    # Enter a parse tree produced by APiParser#s_regex.
    def enterS_regex(self, ctx:APiParser.S_regexContext):
        pass

    # Exit a parse tree produced by APiParser#s_regex.
    def exitS_regex(self, ctx:APiParser.S_regexContext):
        pass


    # Enter a parse tree produced by APiParser#json.
    def enterJson(self, ctx:APiParser.JsonContext):
        pass

    # Exit a parse tree produced by APiParser#json.
    def exitJson(self, ctx:APiParser.JsonContext):
        pass


    # Enter a parse tree produced by APiParser#obj.
    def enterObj(self, ctx:APiParser.ObjContext):
        pass

    # Exit a parse tree produced by APiParser#obj.
    def exitObj(self, ctx:APiParser.ObjContext):
        pass


    # Enter a parse tree produced by APiParser#pair.
    def enterPair(self, ctx:APiParser.PairContext):
        pass

    # Exit a parse tree produced by APiParser#pair.
    def exitPair(self, ctx:APiParser.PairContext):
        pass


    # Enter a parse tree produced by APiParser#arr.
    def enterArr(self, ctx:APiParser.ArrContext):
        pass

    # Exit a parse tree produced by APiParser#arr.
    def exitArr(self, ctx:APiParser.ArrContext):
        pass


    # Enter a parse tree produced by APiParser#value.
    def enterValue(self, ctx:APiParser.ValueContext):
        pass

    # Exit a parse tree produced by APiParser#value.
    def exitValue(self, ctx:APiParser.ValueContext):
        pass


    # Enter a parse tree produced by APiParser#xml.
    def enterXml(self, ctx:APiParser.XmlContext):
        pass

    # Exit a parse tree produced by APiParser#xml.
    def exitXml(self, ctx:APiParser.XmlContext):
        pass


    # Enter a parse tree produced by APiParser#prolog.
    def enterProlog(self, ctx:APiParser.PrologContext):
        pass

    # Exit a parse tree produced by APiParser#prolog.
    def exitProlog(self, ctx:APiParser.PrologContext):
        pass


    # Enter a parse tree produced by APiParser#content.
    def enterContent(self, ctx:APiParser.ContentContext):
        pass

    # Exit a parse tree produced by APiParser#content.
    def exitContent(self, ctx:APiParser.ContentContext):
        pass


    # Enter a parse tree produced by APiParser#element.
    def enterElement(self, ctx:APiParser.ElementContext):
        pass

    # Exit a parse tree produced by APiParser#element.
    def exitElement(self, ctx:APiParser.ElementContext):
        pass


    # Enter a parse tree produced by APiParser#var_or_ident.
    def enterVar_or_ident(self, ctx:APiParser.Var_or_identContext):
        pass

    # Exit a parse tree produced by APiParser#var_or_ident.
    def exitVar_or_ident(self, ctx:APiParser.Var_or_identContext):
        pass


    # Enter a parse tree produced by APiParser#reference.
    def enterReference(self, ctx:APiParser.ReferenceContext):
        pass

    # Exit a parse tree produced by APiParser#reference.
    def exitReference(self, ctx:APiParser.ReferenceContext):
        pass


    # Enter a parse tree produced by APiParser#attribute.
    def enterAttribute(self, ctx:APiParser.AttributeContext):
        pass

    # Exit a parse tree produced by APiParser#attribute.
    def exitAttribute(self, ctx:APiParser.AttributeContext):
        pass


    # Enter a parse tree produced by APiParser#chardata.
    def enterChardata(self, ctx:APiParser.ChardataContext):
        pass

    # Exit a parse tree produced by APiParser#chardata.
    def exitChardata(self, ctx:APiParser.ChardataContext):
        pass


    # Enter a parse tree produced by APiParser#misc.
    def enterMisc(self, ctx:APiParser.MiscContext):
        pass

    # Exit a parse tree produced by APiParser#misc.
    def exitMisc(self, ctx:APiParser.MiscContext):
        pass




