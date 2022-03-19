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
        environment = { 'inputs': [], 'outputs': [] }
        self.STACK.append( environment )


    # Exit a parse tree produced by APiParser#s_environment.
    def exitS_environment(self, ctx:APiParser.S_environmentContext):
        environment = self.STACK[ -1 ]
        self.ns.add_environment( environment )


    # Enter a parse tree produced by APiParser#iflow.
    def enterIflow(self, ctx:APiParser.IflowContext):
        pass

    # Exit a parse tree produced by APiParser#iflow.
    def exitIflow(self, ctx:APiParser.IflowContext):
        input_name = ctx.children[ 1 ].getText()
        input_payload = self.STACK.pop()
        input_flow = ( input_name, input_payload )

        environment = self.STACK[ -1 ]
        environment[ 'inputs' ].append( input_flow )


    # Enter a parse tree produced by APiParser#oflow.
    def enterOflow(self, ctx:APiParser.OflowContext):
        pass


    # Exit a parse tree produced by APiParser#oflow.
    def exitOflow(self, ctx:APiParser.OflowContext):
        output_name = ctx.children[ 1 ].getText()
        output_payload = self.STACK.pop()
        output_flow = ( output_name, output_payload )

        environment = self.STACK[ -1 ]
        environment[ 'outputs' ].append( output_flow )


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
        agent_name = ctx.children[ 1 ].getText()
        agent = { 'name': agent_name, 'flows': [] }

        self.STACK.append(agent)


    # Exit a parse tree produced by APiParser#s_agent.
    def exitS_agent(self, ctx:APiParser.S_agentContext):
        agent = self.STACK[ -1 ]
        self.ns.add_agent( agent )


    # Enter a parse tree produced by APiParser#arglist.
    def enterArglist(self, ctx:APiParser.ArglistContext):
        agent = self.STACK[ -1 ]
        args = [ ctx.children[ i ].getText() for i in range( 1, len( ctx.children ) - 1 ) ]
        agent[ 'args' ] = args

    # Exit a parse tree produced by APiParser#arglist.
    def exitArglist(self, ctx:APiParser.ArglistContext):
        pass


    # Enter a parse tree produced by APiParser#flow.
    def enterFlow(self, ctx:APiParser.FlowContext):
        pass

    # Exit a parse tree produced by APiParser#flow.
    def exitFlow(self, ctx:APiParser.FlowContext):
        flow = []
        while ( type(self.STACK[ -1 ] ) is not dict ):
            channel_name = self.STACK.pop().getText()
            flow.insert( 0, channel_name )

        agent = self.STACK[ -1 ]
        agent[ 'flows' ].append( flow )

    # Enter a parse tree produced by APiParser#valid_channel.
    def enterValid_channel(self, ctx:APiParser.Valid_channelContext):
        channel_name = ctx.children[ 0 ]
        self.STACK.append( channel_name )

    # Exit a parse tree produced by APiParser#valid_channel.
    def exitValid_channel(self, ctx:APiParser.Valid_channelContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel.
    def enterS_channel(self, ctx:APiParser.S_channelContext):
        channel_name = ctx.children[ 1 ].getText()
        agent = { 'name': channel_name }

        self.STACK.append( agent )

    # Exit a parse tree produced by APiParser#s_channel.
    def exitS_channel(self, ctx:APiParser.S_channelContext):
        channel = self.STACK[ -1 ]
        self.ns.add_channel( channel )


    # Enter a parse tree produced by APiParser#s_channel_transformer.
    def enterS_channel_transformer(self, ctx:APiParser.S_channel_transformerContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel_transformer.
    def exitS_channel_transformer(self, ctx:APiParser.S_channel_transformerContext):
        pass


    # Enter a parse tree produced by APiParser#s_channel_spec.
    def enterS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        pass

    # Exit a parse tree produced by APiParser#s_channel_spec.
    def exitS_channel_spec(self, ctx:APiParser.S_channel_specContext):
        output_payload = self.STACK.pop()
        input_payload = self.STACK.pop()
        channel = self.STACK[ -1 ]
        
        channel[ 'input' ] = input_payload
        channel[ 'output' ] = output_payload


    # Enter a parse tree produced by APiParser#s_import.
    def enterS_import(self, ctx:APiParser.S_importContext):
        pass

    # Exit a parse tree produced by APiParser#s_import.
    def exitS_import(self, ctx:APiParser.S_importContext):
        holon_name = ctx.children[ 1 ].getText()
        self.ns.add_holon( holon_name )


    # Enter a parse tree produced by APiParser#s_input.
    def enterS_input(self, ctx:APiParser.S_inputContext):
        input_payload = ctx.children[ 0 ].getText()
        self.STACK.append( input_payload )


    # Exit a parse tree produced by APiParser#s_input.
    def exitS_input(self, ctx:APiParser.S_inputContext):
        pass


    # Enter a parse tree produced by APiParser#s_output.
    def enterS_output(self, ctx:APiParser.S_outputContext):
        output_payload = ctx.children[ 0 ].getText()
        self.STACK.append( output_payload )


    # Exit a parse tree produced by APiParser#s_output.
    def exitS_output(self, ctx:APiParser.S_outputContext):
        pass


    # Enter a parse tree produced by APiParser#s_xml.
    def enterS_xml(self, ctx:APiParser.S_xmlContext):
        self.PARSING_XML = True

    # Exit a parse tree produced by APiParser#s_xml.
    def exitS_xml(self, ctx:APiParser.S_xmlContext):
        self.PARSING_XML = False


    # Enter a parse tree produced by APiParser#s_json.
    def enterS_json(self, ctx:APiParser.S_jsonContext):
        pass

    # Exit a parse tree produced by APiParser#s_json.
    def exitS_json(self, ctx:APiParser.S_jsonContext):
        pass


    # Enter a parse tree produced by APiParser#s_regex.
    def enterS_regex(self, ctx:APiParser.S_regexContext):
        # self.STACK.append( 'regex( ' + ctx.children[ 1 ].getText()[ 1:-1 ] + ' )' )
        pass


    # Exit a parse tree produced by APiParser#s_regex.
    def exitS_regex(self, ctx:APiParser.S_regexContext):
        pass


    # Enter a parse tree produced by APiParser#json.
    def enterJson(self, ctx:APiParser.JsonContext):
        try:
            # print( ctx.children[ 0 ].getText() )
            pass
        except:
            pass

    # Exit a parse tree produced by APiParser#json.
    def exitJson(self, ctx:APiParser.JsonContext):
        # top = self.STACK.pop()
        # self.STACK.append( 'json( %s )' % top )
        # print( self.STACK[ -1 ] )
        pass

    # Enter a parse tree produced by APiParser#obj.
    def enterObj(self, ctx:APiParser.ObjContext):
        # self.STACK.append( 'api_object_begin' )
        pass

    # Exit a parse tree produced by APiParser#obj.
    def exitObj(self, ctx:APiParser.ObjContext):
        # prolog = 'object( '
        # pair = None
        # res = []
        # while pair != 'api_object_begin':
        #     pair = self.STACK.pop()
        #     if pair != 'api_object_begin':
        #         res.append( pair )
        # res.reverse()
        # for val in res:
        #     prolog += "%s, " % val
        # prolog = prolog[ :-2 ] + ' )'
        # self.STACK.append( prolog )
        pass


    # Enter a parse tree produced by APiParser#pair.
    def enterPair(self, ctx:APiParser.PairContext):
        # self.STACK.append( 'pair' )
        # ch = ctx.children[ 0 ].getText()
        # if ch[ 0 ] in [ "'", '"' ]:
        #     val = "'string:%s'" % ch[ 1:-1 ]
        # elif ch[ 0 ] == '?':
        #     val = 'X' + ch[ 1: ]
        # self.STACK.append( val )
        pass

    # Exit a parse tree produced by APiParser#pair.
    def exitPair(self, ctx:APiParser.PairContext):
        # val = self.STACK.pop()
        # key = self.STACK.pop()
        # self.STACK.pop()
        # self.STACK.append( "pair( %s, %s )" % ( key, val ) )
        pass


    # Enter a parse tree produced by APiParser#arr.
    def enterArr(self, ctx:APiParser.ArrContext):
        # self.STACK.append( 'api_array_begin' )
        pass
        
    # Exit a parse tree produced by APiParser#arr.
    def exitArr(self, ctx:APiParser.ArrContext):
        # val = None
        # prolog = 'array( ['
        # res = []
        # while val != 'api_array_begin':
        #     val = self.STACK.pop()
        #     if val != 'api_array_begin':
        #         res.append( val )
        # res.reverse()
        # for val in res:
        #     prolog += "%s, " % val
        # prolog = prolog[ :-2 ] + ' ] )'
        # self.STACK.append( prolog )
        pass
        


    # Enter a parse tree produced by APiParser#value.
    def enterValue(self, ctx:APiParser.ValueContext):
        # if not self.PARSING_XML:
        #     val = ctx.getText()
        #     if ctx.VARIABLE():
        #         self.STACK.append( 'X' + val[ 1: ] )
        #     elif ctx.STRING():
        #         self.STACK.append( "'string:%s'" % val[ 1:-1 ] )
        #     elif ctx.NUMBER():
        #         self.STACK.append( "'number:%s'" % val )
        #     elif val in [ 'true', 'false', 'null' ]:
        #         self.STACK.append( "'atom:%s'" % val )
        pass

    # Exit a parse tree produced by APiParser#value.
    def exitValue(self, ctx:APiParser.ValueContext):
        pass


    # Enter a parse tree produced by APiParser#xml.
    def enterXml(self, ctx:APiParser.XmlContext):
        # self.STACK.append( 'xml' )
        pass

    # Exit a parse tree produced by APiParser#xml.
    def exitXml(self, ctx:APiParser.XmlContext):
        # top = self.STACK.pop()
        # self.STACK.append( 'xml( %s )' % top )
        # print( self.STACK[ -1 ] )
        pass


    # Enter a parse tree produced by APiParser#prolog.
    def enterProlog(self, ctx:APiParser.PrologContext):
        # self.STACK.append( 'api_prolog_begin' )
        pass

    # Exit a parse tree produced by APiParser#prolog.
    def exitProlog(self, ctx:APiParser.PrologContext):
        # val = None
        # prolog = 'prolog( '
        # res = []
        # while val != 'api_prolog_begin':
        #     val = self.STACK.pop()
        #     if val != 'api_prolog_begin':
        #         res.append( val )
        # res.reverse()
        # for val in res:
        #     prolog += '%s, ' % val
        # prolog = prolog[ :-2 ] + ' )'
        # self.STACK.append( prolog )
        pass


    # Enter a parse tree produced by APiParser#content.
    def enterContent(self, ctx:APiParser.ContentContext):
        # self.STACK.append( 'api_content_begin' )
        pass

    # Exit a parse tree produced by APiParser#content.
    def exitContent(self, ctx:APiParser.ContentContext):
        # val = None
        # prolog = 'content( '
        # res = []
        # while val != 'api_content_begin':
        #     val = self.STACK.pop()
        #     if val != 'api_content_begin':
        #         res.append( val )
        # res.reverse()
        # for val in res:
        #     prolog += '%s, ' % val
        # prolog = prolog[ :-2 ] + ' )'
        # self.STACK.append( prolog )
        pass


    # Enter a parse tree produced by APiParser#element.
    def enterElement(self, ctx:APiParser.ElementContext):
        # self.STACK.append( 'api_element_begin' )
        pass

    # Exit a parse tree produced by APiParser#element.
    def exitElement(self, ctx:APiParser.ElementContext):
        # val = None
        # prolog = 'element( '
        # res = []
        # while val != 'api_element_begin':
        #     val = self.STACK.pop()
        #     if val != 'api_element_begin':
        #         res.append( val )
        # elem_name = res.pop()
        # prolog += 'elem( %s ), ' % elem_name
        # res.reverse()
        # for val in res:
        #     prolog += '%s, ' % val
        # prolog = prolog[ :-2 ] + ' )'
        # self.STACK.append( prolog )
        pass

    # Enter a parse tree produced by APiParser#var_or_ident.
    def enterVar_or_ident(self, ctx:APiParser.Var_or_identContext):
        # val = ctx.getText()
        # if ctx.IDENT():
        #     self.STACK.append( "'ident:%s'" % val )
        # elif ctx.VARIABLE():
        #     self.STACK.append( 'X' + val[ 1: ] )
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
        # self.STACK.append( 'api_attribute_begin' )
        # ch = ctx.children[ 2 ].getText()
        # if ch[ 0 ] in [ "'", '"' ]:
        #     val = "'string:%s'" % ch[ 1:-1 ]
        # elif ch[ 0 ] == '?':
        #     val = 'X' + ch[ 1: ]
        # self.STACK.append( val )
        pass

    # Exit a parse tree produced by APiParser#attribute.
    def exitAttribute(self, ctx:APiParser.AttributeContext):
        # val = None
        # prolog = 'attribute( '
        # res = []
        # while val != 'api_attribute_begin':
        #     val = self.STACK.pop()
        #     if val != 'api_attribute_begin':
        #         res.append( val )
        # for val in res:
        #     prolog += '%s, ' % val
        # prolog = prolog[ :-2 ] + ' )'
        # self.STACK.append( prolog )
        pass


    # Enter a parse tree produced by APiParser#chardata.
    def enterChardata(self, ctx:APiParser.ChardataContext):
        # TODO: This is a hackish solution. There must be a more elegant one.
        # values = [ i.getText() for i in ctx.children ]
        # for val in values:
        #     if val[ 0 ] == '?':
        #         self.STACK.append( 'X' + val[ 1: ] )
        #     else:
        #         self.STACK.append( "'atom:%s'" % val )
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
