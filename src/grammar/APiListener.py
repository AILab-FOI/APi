# Generated from APi.g4 by ANTLR 4.13.0
from antlr4 import *

if "." in __name__:
    from .APiParser import APiParser
else:
    from APiParser import APiParser

# This class defines a complete listener for a parse tree produced by APiParser.
class APiListener(ParseTreeListener):

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
        pass


    # Enter a parse tree produced by APiParser#s_environment_forward.
    def enterS_environment_forward(self, ctx:APiParser.S_environment_forwardContext):
        pass

    # Exit a parse tree produced by APiParser#s_environment_forward.
    def exitS_environment_forward(self, ctx:APiParser.S_environment_forwardContext):
        pass


    # Enter a parse tree produced by APiParser#iflow.
    def enterIflow(self, ctx:APiParser.IflowContext):
        pass

    # Exit a parse tree produced by APiParser#iflow.
    def exitIflow(self, ctx:APiParser.IflowContext):
        pass


    # Enter a parse tree produced by APiParser#oflow.
    def enterOflow(self, ctx:APiParser.OflowContext):
        pass

    # Exit a parse tree produced by APiParser#oflow.
    def exitOflow(self, ctx:APiParser.OflowContext):
        pass


    # Enter a parse tree produced by APiParser#s_start.
    def enterS_start(self, ctx:APiParser.S_startContext):
        pass

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
        pass


    # Enter a parse tree produced by APiParser#arglist.
    def enterArglist(self, ctx:APiParser.ArglistContext):
        pass

    # Exit a parse tree produced by APiParser#arglist.
    def exitArglist(self, ctx:APiParser.ArglistContext):
        pass


    # Enter a parse tree produced by APiParser#aflow.
    def enterAflow(self, ctx:APiParser.AflowContext):
        pass

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
        pass


    # Enter a parse tree produced by APiParser#s_channel_forward.
    def enterS_channel_forward(self, ctx:APiParser.S_channel_forwardContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel_forward.
    def exitS_channel_forward(self, ctx:APiParser.S_channel_forwardContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel_spec.
    def enterS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel_spec.
    def exitS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        pass


    # Enter a parse tree produced by APiParser#s_import.
    def enterS_import(self, ctx:APiParser.S_importContext):
        pass

    # Exit a parse tree produced by APiParser#s_import.
    def exitS_import(self, ctx:APiParser.S_importContext):
        pass


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



del APiParser