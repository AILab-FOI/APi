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
	 * Enter a parse tree produced by {@link APiParser#ioflow}.
	 * @param ctx the parse tree
	 */
	void enterIoflow(APiParser.IoflowContext ctx);
	/**
	 * Exit a parse tree produced by {@link APiParser#ioflow}.
	 * @param ctx the parse tree
	 */
	void exitIoflow(APiParser.IoflowContext ctx);
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
}