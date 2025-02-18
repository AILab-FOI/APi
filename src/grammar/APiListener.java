// Generated from APi.g4 by ANTLR 4.9
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link APiParser}.
 */
public interface APiListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link APiParser#api_program}.
	 * @param ctx the parse tree
	 */
	void enterApi_program(APiParser.Api_programContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#api_program}.
	 * @param ctx the parse tree
	 */
	void exitApi_program(APiParser.Api_programContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_environment}.
	 * @param ctx the parse tree
	 */
	void enterS_environment(APiParser.S_environmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_environment}.
	 * @param ctx the parse tree
	 */
	void exitS_environment(APiParser.S_environmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#iflow}.
	 * @param ctx the parse tree
	 */
	void enterIflow(APiParser.IflowContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#iflow}.
	 * @param ctx the parse tree
	 */
	void exitIflow(APiParser.IflowContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#oflow}.
	 * @param ctx the parse tree
	 */
	void enterOflow(APiParser.OflowContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#oflow}.
	 * @param ctx the parse tree
	 */
	void exitOflow(APiParser.OflowContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_start}.
	 * @param ctx the parse tree
	 */
	void enterS_start(APiParser.S_startContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_start}.
	 * @param ctx the parse tree
	 */
	void exitS_start(APiParser.S_startContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#pi_expr}.
	 * @param ctx the parse tree
	 */
	void enterPi_expr(APiParser.Pi_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#pi_expr}.
	 * @param ctx the parse tree
	 */
	void exitPi_expr(APiParser.Pi_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_agent}.
	 * @param ctx the parse tree
	 */
	void enterS_agent(APiParser.S_agentContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_agent}.
	 * @param ctx the parse tree
	 */
	void exitS_agent(APiParser.S_agentContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#arglist}.
	 * @param ctx the parse tree
	 */
	void enterArglist(APiParser.ArglistContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#arglist}.
	 * @param ctx the parse tree
	 */
	void exitArglist(APiParser.ArglistContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#flow}.
	 * @param ctx the parse tree
	 */
	void enterFlow(APiParser.FlowContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#flow}.
	 * @param ctx the parse tree
	 */
	void exitFlow(APiParser.FlowContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#valid_channel}.
	 * @param ctx the parse tree
	 */
	void enterValid_channel(APiParser.Valid_channelContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#valid_channel}.
	 * @param ctx the parse tree
	 */
	void exitValid_channel(APiParser.Valid_channelContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_channel}.
	 * @param ctx the parse tree
	 */
	void enterS_channel(APiParser.S_channelContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_channel}.
	 * @param ctx the parse tree
	 */
	void exitS_channel(APiParser.S_channelContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_channel_transformer}.
	 * @param ctx the parse tree
	 */
	void enterS_channel_transformer(APiParser.S_channel_transformerContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_channel_transformer}.
	 * @param ctx the parse tree
	 */
	void exitS_channel_transformer(APiParser.S_channel_transformerContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_channel_spec}.
	 * @param ctx the parse tree
	 */
	void enterS_channel_spec(APiParser.S_channel_specContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_channel_spec}.
	 * @param ctx the parse tree
	 */
	void exitS_channel_spec(APiParser.S_channel_specContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_import}.
	 * @param ctx the parse tree
	 */
	void enterS_import(APiParser.S_importContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_import}.
	 * @param ctx the parse tree
	 */
	void exitS_import(APiParser.S_importContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_input}.
	 * @param ctx the parse tree
	 */
	void enterS_input(APiParser.S_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_input}.
	 * @param ctx the parse tree
	 */
	void exitS_input(APiParser.S_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_output}.
	 * @param ctx the parse tree
	 */
	void enterS_output(APiParser.S_outputContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_output}.
	 * @param ctx the parse tree
	 */
	void exitS_output(APiParser.S_outputContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_xml}.
	 * @param ctx the parse tree
	 */
	void enterS_xml(APiParser.S_xmlContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_xml}.
	 * @param ctx the parse tree
	 */
	void exitS_xml(APiParser.S_xmlContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_json}.
	 * @param ctx the parse tree
	 */
	void enterS_json(APiParser.S_jsonContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_json}.
	 * @param ctx the parse tree
	 */
	void exitS_json(APiParser.S_jsonContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#s_regex}.
	 * @param ctx the parse tree
	 */
	void enterS_regex(APiParser.S_regexContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#s_regex}.
	 * @param ctx the parse tree
	 */
	void exitS_regex(APiParser.S_regexContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#json}.
	 * @param ctx the parse tree
	 */
	void enterJson(APiParser.JsonContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#json}.
	 * @param ctx the parse tree
	 */
	void exitJson(APiParser.JsonContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#obj}.
	 * @param ctx the parse tree
	 */
	void enterObj(APiParser.ObjContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#obj}.
	 * @param ctx the parse tree
	 */
	void exitObj(APiParser.ObjContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#pair}.
	 * @param ctx the parse tree
	 */
	void enterPair(APiParser.PairContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#pair}.
	 * @param ctx the parse tree
	 */
	void exitPair(APiParser.PairContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#arr}.
	 * @param ctx the parse tree
	 */
	void enterArr(APiParser.ArrContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#arr}.
	 * @param ctx the parse tree
	 */
	void exitArr(APiParser.ArrContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#value}.
	 * @param ctx the parse tree
	 */
	void enterValue(APiParser.ValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#value}.
	 * @param ctx the parse tree
	 */
	void exitValue(APiParser.ValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#xml}.
	 * @param ctx the parse tree
	 */
	void enterXml(APiParser.XmlContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#xml}.
	 * @param ctx the parse tree
	 */
	void exitXml(APiParser.XmlContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#prolog}.
	 * @param ctx the parse tree
	 */
	void enterProlog(APiParser.PrologContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#prolog}.
	 * @param ctx the parse tree
	 */
	void exitProlog(APiParser.PrologContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#content}.
	 * @param ctx the parse tree
	 */
	void enterContent(APiParser.ContentContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#content}.
	 * @param ctx the parse tree
	 */
	void exitContent(APiParser.ContentContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#element}.
	 * @param ctx the parse tree
	 */
	void enterElement(APiParser.ElementContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#element}.
	 * @param ctx the parse tree
	 */
	void exitElement(APiParser.ElementContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#var_or_ident}.
	 * @param ctx the parse tree
	 */
	void enterVar_or_ident(APiParser.Var_or_identContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#var_or_ident}.
	 * @param ctx the parse tree
	 */
	void exitVar_or_ident(APiParser.Var_or_identContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#reference}.
	 * @param ctx the parse tree
	 */
	void enterReference(APiParser.ReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#reference}.
	 * @param ctx the parse tree
	 */
	void exitReference(APiParser.ReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#attribute}.
	 * @param ctx the parse tree
	 */
	void enterAttribute(APiParser.AttributeContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#attribute}.
	 * @param ctx the parse tree
	 */
	void exitAttribute(APiParser.AttributeContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#chardata}.
	 * @param ctx the parse tree
	 */
	void enterChardata(APiParser.ChardataContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#chardata}.
	 * @param ctx the parse tree
	 */
	void exitChardata(APiParser.ChardataContext ctx);
	/**
	 * Enter a parse tree produced by {@link APiParser#misc}.
	 * @param ctx the parse tree
	 */
	void enterMisc(APiParser.MiscContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#misc}.
	 * @param ctx the parse tree
	 */
	void exitMisc(APiParser.MiscContext ctx);
}