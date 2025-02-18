// Generated from APi.g4 by ANTLR 4.9
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class APiParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		STDIN=18, STDOUT=19, STDERR=20, VOID=21, IMPORT=22, ENVIRONMENT=23, ONSUCCESS=24, 
		ONFAIL=25, RESTART=26, PARALLEL=27, START=28, SELF=29, AGENT=30, CHANNEL=31, 
		REGEX=32, JSON=33, XML=34, INPUT_FORMAT=35, OUTPUT_FORMAT=36, SENDS=37, 
		NIL=38, COMMENT=39, COMMENT1=40, COMMENT2=41, NEWLINE=42, TAB=43, SPEC_CHAR=44, 
		VARIABLE=45, IDENT=46, STRING=47, NUMBER=48, SPACE=49, COMMENTXML=1, CDATA=2, 
		DTD=3, EntityRef=4, CharRef=5, SEA_WS=6, OPEN=7, XMLDeclOpen=8, TEXT=9, 
		CLOSE=10, SPECIAL_CLOSE=11, SLASH_CLOSE=12, SLASH=13, EQUALS=14, STRINGXML=15, 
		Name=16, S=17, PI=19;
	public static final int
		RULE_api_program = 0, RULE_s_environment = 1, RULE_iflow = 2, RULE_oflow = 3, 
		RULE_s_start = 4, RULE_pi_expr = 5, RULE_s_agent = 6, RULE_arglist = 7, 
		RULE_flow = 8, RULE_valid_channel = 9, RULE_s_channel = 10, RULE_s_channel_transformer = 11, 
		RULE_s_channel_spec = 12, RULE_s_import = 13, RULE_s_input = 14, RULE_s_output = 15, 
		RULE_s_xml = 16, RULE_s_json = 17, RULE_s_regex = 18, RULE_json = 19, 
		RULE_obj = 20, RULE_pair = 21, RULE_arr = 22, RULE_value = 23, RULE_xml = 24, 
		RULE_prolog = 25, RULE_content = 26, RULE_element = 27, RULE_var_or_ident = 28, 
		RULE_reference = 29, RULE_attribute = 30, RULE_chardata = 31, RULE_misc = 32;
	private static String[] makeRuleNames() {
		return new String[] {
			"api_program", "s_environment", "iflow", "oflow", "s_start", "pi_expr", 
			"s_agent", "arglist", "flow", "valid_channel", "s_channel", "s_channel_transformer", 
			"s_channel_spec", "s_import", "s_input", "s_output", "s_xml", "s_json", 
			"s_regex", "json", "obj", "pair", "arr", "value", "xml", "prolog", "content", 
			"element", "var_or_ident", "reference", "attribute", "chardata", "misc"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "':'", "'('", "')'", "'.'", "'{'", "','", "'}'", "'['", "']'", 
			"'true'", "'false'", "'null'", "'<'", "'>'", "'/'", "'/>'", "'='", "'stdin'", 
			"'stdout'", "'stderr'", "'void'", "'import'", "'environment'", "'&'", 
			"'!'", "'+'", "'|'", "'start'", "'self'", "'agent'", "'channel'", "'regex'", 
			"'json'", "'xml'", "'=>'", "'<='", "'->'", "'0'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, "STDIN", "STDOUT", "STDERR", "VOID", 
			"IMPORT", "ENVIRONMENT", "ONSUCCESS", "ONFAIL", "RESTART", "PARALLEL", 
			"START", "SELF", "AGENT", "CHANNEL", "REGEX", "JSON", "XML", "INPUT_FORMAT", 
			"OUTPUT_FORMAT", "SENDS", "NIL", "COMMENT", "COMMENT1", "COMMENT2", "NEWLINE", 
			"TAB", "SPEC_CHAR", "VARIABLE", "IDENT", "STRING", "NUMBER", "SPACE"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "APi.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public APiParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class Api_programContext extends ParserRuleContext {
		public List<S_importContext> s_import() {
			return getRuleContexts(S_importContext.class);
		}
		public S_importContext s_import(int i) {
			return getRuleContext(S_importContext.class,i);
		}
		public List<S_environmentContext> s_environment() {
			return getRuleContexts(S_environmentContext.class);
		}
		public S_environmentContext s_environment(int i) {
			return getRuleContext(S_environmentContext.class,i);
		}
		public List<S_channelContext> s_channel() {
			return getRuleContexts(S_channelContext.class);
		}
		public S_channelContext s_channel(int i) {
			return getRuleContext(S_channelContext.class,i);
		}
		public List<S_channel_transformerContext> s_channel_transformer() {
			return getRuleContexts(S_channel_transformerContext.class);
		}
		public S_channel_transformerContext s_channel_transformer(int i) {
			return getRuleContext(S_channel_transformerContext.class,i);
		}
		public List<S_agentContext> s_agent() {
			return getRuleContexts(S_agentContext.class);
		}
		public S_agentContext s_agent(int i) {
			return getRuleContext(S_agentContext.class,i);
		}
		public List<S_startContext> s_start() {
			return getRuleContexts(S_startContext.class);
		}
		public S_startContext s_start(int i) {
			return getRuleContext(S_startContext.class,i);
		}
		public List<TerminalNode> COMMENT() { return getTokens(APiParser.COMMENT); }
		public TerminalNode COMMENT(int i) {
			return getToken(APiParser.COMMENT, i);
		}
		public List<TerminalNode> NEWLINE() { return getTokens(APiParser.NEWLINE); }
		public TerminalNode NEWLINE(int i) {
			return getToken(APiParser.NEWLINE, i);
		}
		public Api_programContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_api_program; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterApi_program(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitApi_program(this);
		}
	}

	public final Api_programContext api_program() throws RecognitionException {
		Api_programContext _localctx = new Api_programContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_api_program);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(76);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=1 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1+1 ) {
					{
					setState(74);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
					case 1:
						{
						setState(66);
						s_import();
						}
						break;
					case 2:
						{
						setState(67);
						s_environment();
						}
						break;
					case 3:
						{
						setState(68);
						s_channel();
						}
						break;
					case 4:
						{
						setState(69);
						s_channel_transformer();
						}
						break;
					case 5:
						{
						setState(70);
						s_agent();
						}
						break;
					case 6:
						{
						setState(71);
						s_start();
						}
						break;
					case 7:
						{
						setState(72);
						match(COMMENT);
						}
						break;
					case 8:
						{
						setState(73);
						match(NEWLINE);
						}
						break;
					}
					} 
				}
				setState(78);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_environmentContext extends ParserRuleContext {
		public TerminalNode ENVIRONMENT() { return getToken(APiParser.ENVIRONMENT, 0); }
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public List<IflowContext> iflow() {
			return getRuleContexts(IflowContext.class);
		}
		public IflowContext iflow(int i) {
			return getRuleContext(IflowContext.class,i);
		}
		public List<OflowContext> oflow() {
			return getRuleContexts(OflowContext.class);
		}
		public OflowContext oflow(int i) {
			return getRuleContext(OflowContext.class,i);
		}
		public S_environmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_environment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_environment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_environment(this);
		}
	}

	public final S_environmentContext s_environment() throws RecognitionException {
		S_environmentContext _localctx = new S_environmentContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_s_environment);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(79);
			match(ENVIRONMENT);
			setState(80);
			match(T__0);
			setState(81);
			match(NEWLINE);
			setState(84); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				setState(84);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
				case 1:
					{
					setState(82);
					iflow();
					}
					break;
				case 2:
					{
					setState(83);
					oflow();
					}
					break;
				}
				}
				setState(86); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==TAB );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class IflowContext extends ParserRuleContext {
		public TerminalNode TAB() { return getToken(APiParser.TAB, 0); }
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode INPUT_FORMAT() { return getToken(APiParser.INPUT_FORMAT, 0); }
		public S_inputContext s_input() {
			return getRuleContext(S_inputContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public IflowContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_iflow; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterIflow(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitIflow(this);
		}
	}

	public final IflowContext iflow() throws RecognitionException {
		IflowContext _localctx = new IflowContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_iflow);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88);
			match(TAB);
			setState(89);
			match(IDENT);
			setState(90);
			match(INPUT_FORMAT);
			setState(91);
			s_input();
			setState(92);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class OflowContext extends ParserRuleContext {
		public TerminalNode TAB() { return getToken(APiParser.TAB, 0); }
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode OUTPUT_FORMAT() { return getToken(APiParser.OUTPUT_FORMAT, 0); }
		public S_outputContext s_output() {
			return getRuleContext(S_outputContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public OflowContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_oflow; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterOflow(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitOflow(this);
		}
	}

	public final OflowContext oflow() throws RecognitionException {
		OflowContext _localctx = new OflowContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_oflow);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(94);
			match(TAB);
			setState(95);
			match(IDENT);
			setState(96);
			match(OUTPUT_FORMAT);
			setState(97);
			s_output();
			setState(98);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_startContext extends ParserRuleContext {
		public TerminalNode START() { return getToken(APiParser.START, 0); }
		public Pi_exprContext pi_expr() {
			return getRuleContext(Pi_exprContext.class,0);
		}
		public S_startContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_start; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_start(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_start(this);
		}
	}

	public final S_startContext s_start() throws RecognitionException {
		S_startContext _localctx = new S_startContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_s_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(100);
			match(START);
			setState(101);
			pi_expr(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Pi_exprContext extends ParserRuleContext {
		public List<Pi_exprContext> pi_expr() {
			return getRuleContexts(Pi_exprContext.class);
		}
		public Pi_exprContext pi_expr(int i) {
			return getRuleContext(Pi_exprContext.class,i);
		}
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode PARALLEL() { return getToken(APiParser.PARALLEL, 0); }
		public TerminalNode ONSUCCESS() { return getToken(APiParser.ONSUCCESS, 0); }
		public TerminalNode ONFAIL() { return getToken(APiParser.ONFAIL, 0); }
		public TerminalNode RESTART() { return getToken(APiParser.RESTART, 0); }
		public Pi_exprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pi_expr; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterPi_expr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitPi_expr(this);
		}
	}

	public final Pi_exprContext pi_expr() throws RecognitionException {
		return pi_expr(0);
	}

	private Pi_exprContext pi_expr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		Pi_exprContext _localctx = new Pi_exprContext(_ctx, _parentState);
		Pi_exprContext _prevctx = _localctx;
		int _startState = 10;
		enterRecursionRule(_localctx, 10, RULE_pi_expr, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(109);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
				{
				setState(104);
				match(T__1);
				setState(105);
				pi_expr(0);
				setState(106);
				match(T__2);
				}
				break;
			case IDENT:
				{
				setState(108);
				match(IDENT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(126);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,6,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(124);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
					case 1:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(111);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(112);
						match(PARALLEL);
						setState(113);
						pi_expr(6);
						}
						break;
					case 2:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(114);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(115);
						match(ONSUCCESS);
						setState(116);
						pi_expr(5);
						}
						break;
					case 3:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(117);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(118);
						match(ONFAIL);
						setState(119);
						pi_expr(4);
						}
						break;
					case 4:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(120);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(121);
						pi_expr(3);
						}
						break;
					case 5:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(122);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(123);
						match(RESTART);
						}
						break;
					}
					} 
				}
				setState(128);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,6,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class S_agentContext extends ParserRuleContext {
		public TerminalNode AGENT() { return getToken(APiParser.AGENT, 0); }
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public ArglistContext arglist() {
			return getRuleContext(ArglistContext.class,0);
		}
		public List<FlowContext> flow() {
			return getRuleContexts(FlowContext.class);
		}
		public FlowContext flow(int i) {
			return getRuleContext(FlowContext.class,i);
		}
		public S_agentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_agent; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_agent(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_agent(this);
		}
	}

	public final S_agentContext s_agent() throws RecognitionException {
		S_agentContext _localctx = new S_agentContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_s_agent);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(129);
			match(AGENT);
			setState(130);
			match(IDENT);
			setState(132);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(131);
				arglist();
				}
			}

			setState(134);
			match(T__0);
			setState(135);
			match(NEWLINE);
			setState(137); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(136);
				flow();
				}
				}
				setState(139); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==TAB );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArglistContext extends ParserRuleContext {
		public List<TerminalNode> IDENT() { return getTokens(APiParser.IDENT); }
		public TerminalNode IDENT(int i) {
			return getToken(APiParser.IDENT, i);
		}
		public ArglistContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arglist; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterArglist(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitArglist(this);
		}
	}

	public final ArglistContext arglist() throws RecognitionException {
		ArglistContext _localctx = new ArglistContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_arglist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(141);
			match(T__1);
			setState(142);
			match(IDENT);
			setState(146);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==IDENT) {
				{
				{
				setState(143);
				match(IDENT);
				}
				}
				setState(148);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(149);
			match(T__2);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class FlowContext extends ParserRuleContext {
		public TerminalNode TAB() { return getToken(APiParser.TAB, 0); }
		public List<Valid_channelContext> valid_channel() {
			return getRuleContexts(Valid_channelContext.class);
		}
		public Valid_channelContext valid_channel(int i) {
			return getRuleContext(Valid_channelContext.class,i);
		}
		public List<TerminalNode> SENDS() { return getTokens(APiParser.SENDS); }
		public TerminalNode SENDS(int i) {
			return getToken(APiParser.SENDS, i);
		}
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public FlowContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_flow; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterFlow(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitFlow(this);
		}
	}

	public final FlowContext flow() throws RecognitionException {
		FlowContext _localctx = new FlowContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_flow);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(151);
			match(TAB);
			setState(152);
			valid_channel();
			setState(153);
			match(SENDS);
			setState(154);
			valid_channel();
			setState(159);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==SENDS) {
				{
				{
				setState(155);
				match(SENDS);
				setState(156);
				valid_channel();
				}
				}
				setState(161);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(162);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Valid_channelContext extends ParserRuleContext {
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode SELF() { return getToken(APiParser.SELF, 0); }
		public TerminalNode NIL() { return getToken(APiParser.NIL, 0); }
		public TerminalNode STDIN() { return getToken(APiParser.STDIN, 0); }
		public TerminalNode STDOUT() { return getToken(APiParser.STDOUT, 0); }
		public TerminalNode STDERR() { return getToken(APiParser.STDERR, 0); }
		public TerminalNode VOID() { return getToken(APiParser.VOID, 0); }
		public Valid_channelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_valid_channel; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterValid_channel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitValid_channel(this);
		}
	}

	public final Valid_channelContext valid_channel() throws RecognitionException {
		Valid_channelContext _localctx = new Valid_channelContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_valid_channel);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(164);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << STDIN) | (1L << STDOUT) | (1L << STDERR) | (1L << VOID) | (1L << SELF) | (1L << NIL) | (1L << IDENT))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_channelContext extends ParserRuleContext {
		public TerminalNode CHANNEL() { return getToken(APiParser.CHANNEL, 0); }
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public S_channel_specContext s_channel_spec() {
			return getRuleContext(S_channel_specContext.class,0);
		}
		public S_channelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_channel; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_channel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_channel(this);
		}
	}

	public final S_channelContext s_channel() throws RecognitionException {
		S_channelContext _localctx = new S_channelContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_s_channel);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(166);
			match(CHANNEL);
			setState(167);
			match(IDENT);
			setState(168);
			match(T__0);
			setState(169);
			match(NEWLINE);
			setState(170);
			s_channel_spec();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_channel_transformerContext extends ParserRuleContext {
		public TerminalNode CHANNEL() { return getToken(APiParser.CHANNEL, 0); }
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public S_channel_transformerContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_channel_transformer; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_channel_transformer(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_channel_transformer(this);
		}
	}

	public final S_channel_transformerContext s_channel_transformer() throws RecognitionException {
		S_channel_transformerContext _localctx = new S_channel_transformerContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_s_channel_transformer);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(172);
			match(CHANNEL);
			setState(173);
			match(IDENT);
			setState(174);
			match(T__3);
			setState(175);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_channel_specContext extends ParserRuleContext {
		public TerminalNode TAB() { return getToken(APiParser.TAB, 0); }
		public S_inputContext s_input() {
			return getRuleContext(S_inputContext.class,0);
		}
		public TerminalNode SENDS() { return getToken(APiParser.SENDS, 0); }
		public S_outputContext s_output() {
			return getRuleContext(S_outputContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public S_channel_specContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_channel_spec; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_channel_spec(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_channel_spec(this);
		}
	}

	public final S_channel_specContext s_channel_spec() throws RecognitionException {
		S_channel_specContext _localctx = new S_channel_specContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_s_channel_spec);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(177);
			match(TAB);
			setState(178);
			s_input();
			setState(179);
			match(SENDS);
			setState(180);
			s_output();
			setState(181);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_importContext extends ParserRuleContext {
		public TerminalNode IMPORT() { return getToken(APiParser.IMPORT, 0); }
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode NEWLINE() { return getToken(APiParser.NEWLINE, 0); }
		public S_importContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_import; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_import(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_import(this);
		}
	}

	public final S_importContext s_import() throws RecognitionException {
		S_importContext _localctx = new S_importContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_s_import);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(183);
			match(IMPORT);
			setState(184);
			match(IDENT);
			setState(185);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_inputContext extends ParserRuleContext {
		public S_jsonContext s_json() {
			return getRuleContext(S_jsonContext.class,0);
		}
		public S_xmlContext s_xml() {
			return getRuleContext(S_xmlContext.class,0);
		}
		public S_regexContext s_regex() {
			return getRuleContext(S_regexContext.class,0);
		}
		public S_inputContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_input; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_input(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_input(this);
		}
	}

	public final S_inputContext s_input() throws RecognitionException {
		S_inputContext _localctx = new S_inputContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_s_input);
		try {
			setState(190);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case JSON:
				enterOuterAlt(_localctx, 1);
				{
				setState(187);
				s_json();
				}
				break;
			case XML:
				enterOuterAlt(_localctx, 2);
				{
				setState(188);
				s_xml();
				}
				break;
			case REGEX:
				enterOuterAlt(_localctx, 3);
				{
				setState(189);
				s_regex();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_outputContext extends ParserRuleContext {
		public S_jsonContext s_json() {
			return getRuleContext(S_jsonContext.class,0);
		}
		public S_xmlContext s_xml() {
			return getRuleContext(S_xmlContext.class,0);
		}
		public S_outputContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_output; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_output(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_output(this);
		}
	}

	public final S_outputContext s_output() throws RecognitionException {
		S_outputContext _localctx = new S_outputContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_s_output);
		try {
			setState(194);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case JSON:
				enterOuterAlt(_localctx, 1);
				{
				setState(192);
				s_json();
				}
				break;
			case XML:
				enterOuterAlt(_localctx, 2);
				{
				setState(193);
				s_xml();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_xmlContext extends ParserRuleContext {
		public TerminalNode XML() { return getToken(APiParser.XML, 0); }
		public XmlContext xml() {
			return getRuleContext(XmlContext.class,0);
		}
		public S_xmlContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_xml; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_xml(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_xml(this);
		}
	}

	public final S_xmlContext s_xml() throws RecognitionException {
		S_xmlContext _localctx = new S_xmlContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_s_xml);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(196);
			match(XML);
			setState(197);
			xml();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_jsonContext extends ParserRuleContext {
		public TerminalNode JSON() { return getToken(APiParser.JSON, 0); }
		public JsonContext json() {
			return getRuleContext(JsonContext.class,0);
		}
		public S_jsonContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_json; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_json(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_json(this);
		}
	}

	public final S_jsonContext s_json() throws RecognitionException {
		S_jsonContext _localctx = new S_jsonContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_s_json);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(199);
			match(JSON);
			setState(200);
			json();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class S_regexContext extends ParserRuleContext {
		public TerminalNode REGEX() { return getToken(APiParser.REGEX, 0); }
		public TerminalNode STRING() { return getToken(APiParser.STRING, 0); }
		public S_regexContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_s_regex; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterS_regex(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitS_regex(this);
		}
	}

	public final S_regexContext s_regex() throws RecognitionException {
		S_regexContext _localctx = new S_regexContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_s_regex);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(202);
			match(REGEX);
			setState(203);
			match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class JsonContext extends ParserRuleContext {
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public JsonContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_json; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterJson(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitJson(this);
		}
	}

	public final JsonContext json() throws RecognitionException {
		JsonContext _localctx = new JsonContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_json);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(205);
			value();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ObjContext extends ParserRuleContext {
		public List<PairContext> pair() {
			return getRuleContexts(PairContext.class);
		}
		public PairContext pair(int i) {
			return getRuleContext(PairContext.class,i);
		}
		public ObjContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_obj; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterObj(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitObj(this);
		}
	}

	public final ObjContext obj() throws RecognitionException {
		ObjContext _localctx = new ObjContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_obj);
		int _la;
		try {
			setState(220);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,14,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(207);
				match(T__4);
				setState(208);
				pair();
				setState(213);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__5) {
					{
					{
					setState(209);
					match(T__5);
					setState(210);
					pair();
					}
					}
					setState(215);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(216);
				match(T__6);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(218);
				match(T__4);
				setState(219);
				match(T__6);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PairContext extends ParserRuleContext {
		public TerminalNode STRING() { return getToken(APiParser.STRING, 0); }
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public TerminalNode VARIABLE() { return getToken(APiParser.VARIABLE, 0); }
		public PairContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pair; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterPair(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitPair(this);
		}
	}

	public final PairContext pair() throws RecognitionException {
		PairContext _localctx = new PairContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_pair);
		try {
			setState(228);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(222);
				match(STRING);
				setState(223);
				match(T__0);
				setState(224);
				value();
				}
				break;
			case VARIABLE:
				enterOuterAlt(_localctx, 2);
				{
				setState(225);
				match(VARIABLE);
				setState(226);
				match(T__0);
				setState(227);
				value();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArrContext extends ParserRuleContext {
		public List<ValueContext> value() {
			return getRuleContexts(ValueContext.class);
		}
		public ValueContext value(int i) {
			return getRuleContext(ValueContext.class,i);
		}
		public ArrContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arr; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterArr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitArr(this);
		}
	}

	public final ArrContext arr() throws RecognitionException {
		ArrContext _localctx = new ArrContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_arr);
		int _la;
		try {
			setState(243);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,17,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(230);
				match(T__7);
				setState(231);
				value();
				setState(236);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__5) {
					{
					{
					setState(232);
					match(T__5);
					setState(233);
					value();
					}
					}
					setState(238);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(239);
				match(T__8);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(241);
				match(T__7);
				setState(242);
				match(T__8);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ValueContext extends ParserRuleContext {
		public TerminalNode VARIABLE() { return getToken(APiParser.VARIABLE, 0); }
		public TerminalNode STRING() { return getToken(APiParser.STRING, 0); }
		public TerminalNode NUMBER() { return getToken(APiParser.NUMBER, 0); }
		public TerminalNode SPEC_CHAR() { return getToken(APiParser.SPEC_CHAR, 0); }
		public ObjContext obj() {
			return getRuleContext(ObjContext.class,0);
		}
		public ArrContext arr() {
			return getRuleContext(ArrContext.class,0);
		}
		public ValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_value; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitValue(this);
		}
	}

	public final ValueContext value() throws RecognitionException {
		ValueContext _localctx = new ValueContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_value);
		try {
			setState(254);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case VARIABLE:
				enterOuterAlt(_localctx, 1);
				{
				setState(245);
				match(VARIABLE);
				}
				break;
			case STRING:
				enterOuterAlt(_localctx, 2);
				{
				setState(246);
				match(STRING);
				}
				break;
			case NUMBER:
				enterOuterAlt(_localctx, 3);
				{
				setState(247);
				match(NUMBER);
				}
				break;
			case SPEC_CHAR:
				enterOuterAlt(_localctx, 4);
				{
				setState(248);
				match(SPEC_CHAR);
				}
				break;
			case T__4:
				enterOuterAlt(_localctx, 5);
				{
				setState(249);
				obj();
				}
				break;
			case T__7:
				enterOuterAlt(_localctx, 6);
				{
				setState(250);
				arr();
				}
				break;
			case T__9:
				enterOuterAlt(_localctx, 7);
				{
				setState(251);
				match(T__9);
				}
				break;
			case T__10:
				enterOuterAlt(_localctx, 8);
				{
				setState(252);
				match(T__10);
				}
				break;
			case T__11:
				enterOuterAlt(_localctx, 9);
				{
				setState(253);
				match(T__11);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class XmlContext extends ParserRuleContext {
		public ElementContext element() {
			return getRuleContext(ElementContext.class,0);
		}
		public PrologContext prolog() {
			return getRuleContext(PrologContext.class,0);
		}
		public List<MiscContext> misc() {
			return getRuleContexts(MiscContext.class);
		}
		public MiscContext misc(int i) {
			return getRuleContext(MiscContext.class,i);
		}
		public XmlContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xml; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterXml(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitXml(this);
		}
	}

	public final XmlContext xml() throws RecognitionException {
		XmlContext _localctx = new XmlContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_xml);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(257);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__7) {
				{
				setState(256);
				prolog();
				}
			}

			setState(262);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__0) | (1L << T__5) | (1L << STDOUT))) != 0)) {
				{
				{
				setState(259);
				misc();
				}
				}
				setState(264);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(265);
			element();
			setState(269);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__0) | (1L << T__5) | (1L << STDOUT))) != 0)) {
				{
				{
				setState(266);
				misc();
				}
				}
				setState(271);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PrologContext extends ParserRuleContext {
		public TerminalNode XMLDeclOpen() { return getToken(APiParser.XMLDeclOpen, 0); }
		public TerminalNode SPECIAL_CLOSE() { return getToken(APiParser.SPECIAL_CLOSE, 0); }
		public List<AttributeContext> attribute() {
			return getRuleContexts(AttributeContext.class);
		}
		public AttributeContext attribute(int i) {
			return getRuleContext(AttributeContext.class,i);
		}
		public PrologContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prolog; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterProlog(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitProlog(this);
		}
	}

	public final PrologContext prolog() throws RecognitionException {
		PrologContext _localctx = new PrologContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_prolog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(272);
			match(T__7);
			setState(276);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==VARIABLE || _la==IDENT) {
				{
				{
				setState(273);
				attribute();
				}
				}
				setState(278);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(279);
			match(T__10);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ContentContext extends ParserRuleContext {
		public List<ChardataContext> chardata() {
			return getRuleContexts(ChardataContext.class);
		}
		public ChardataContext chardata(int i) {
			return getRuleContext(ChardataContext.class,i);
		}
		public List<ElementContext> element() {
			return getRuleContexts(ElementContext.class);
		}
		public ElementContext element(int i) {
			return getRuleContext(ElementContext.class,i);
		}
		public List<ReferenceContext> reference() {
			return getRuleContexts(ReferenceContext.class);
		}
		public ReferenceContext reference(int i) {
			return getRuleContext(ReferenceContext.class,i);
		}
		public List<TerminalNode> CDATA() { return getTokens(APiParser.CDATA); }
		public TerminalNode CDATA(int i) {
			return getToken(APiParser.CDATA, i);
		}
		public List<TerminalNode> PI() { return getTokens(APiParser.PI); }
		public TerminalNode PI(int i) {
			return getToken(APiParser.PI, i);
		}
		public List<TerminalNode> COMMENTXML() { return getTokens(APiParser.COMMENTXML); }
		public TerminalNode COMMENTXML(int i) {
			return getToken(APiParser.COMMENTXML, i);
		}
		public ContentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_content; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterContent(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitContent(this);
		}
	}

	public final ContentContext content() throws RecognitionException {
		ContentContext _localctx = new ContentContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_content);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(282);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,23,_ctx) ) {
			case 1:
				{
				setState(281);
				chardata();
				}
				break;
			}
			setState(296);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,26,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(289);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case T__12:
						{
						setState(284);
						element();
						}
						break;
					case T__3:
					case T__4:
						{
						setState(285);
						reference();
						}
						break;
					case T__1:
						{
						setState(286);
						match(T__1);
						}
						break;
					case STDOUT:
						{
						setState(287);
						match(STDOUT);
						}
						break;
					case T__0:
						{
						setState(288);
						match(T__0);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(292);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,25,_ctx) ) {
					case 1:
						{
						setState(291);
						chardata();
						}
						break;
					}
					}
					} 
				}
				setState(298);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,26,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ElementContext extends ParserRuleContext {
		public List<Var_or_identContext> var_or_ident() {
			return getRuleContexts(Var_or_identContext.class);
		}
		public Var_or_identContext var_or_ident(int i) {
			return getRuleContext(Var_or_identContext.class,i);
		}
		public ContentContext content() {
			return getRuleContext(ContentContext.class,0);
		}
		public List<AttributeContext> attribute() {
			return getRuleContexts(AttributeContext.class);
		}
		public AttributeContext attribute(int i) {
			return getRuleContext(AttributeContext.class,i);
		}
		public ElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_element; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterElement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitElement(this);
		}
	}

	public final ElementContext element() throws RecognitionException {
		ElementContext _localctx = new ElementContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_element);
		int _la;
		try {
			setState(324);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,29,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(299);
				match(T__12);
				setState(300);
				var_or_ident();
				setState(304);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==VARIABLE || _la==IDENT) {
					{
					{
					setState(301);
					attribute();
					}
					}
					setState(306);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(307);
				match(T__13);
				setState(308);
				content();
				setState(309);
				match(T__12);
				setState(310);
				match(T__14);
				setState(311);
				var_or_ident();
				setState(312);
				match(T__13);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(314);
				match(T__12);
				setState(315);
				var_or_ident();
				setState(319);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==VARIABLE || _la==IDENT) {
					{
					{
					setState(316);
					attribute();
					}
					}
					setState(321);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(322);
				match(T__15);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Var_or_identContext extends ParserRuleContext {
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode VARIABLE() { return getToken(APiParser.VARIABLE, 0); }
		public Var_or_identContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_or_ident; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterVar_or_ident(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitVar_or_ident(this);
		}
	}

	public final Var_or_identContext var_or_ident() throws RecognitionException {
		Var_or_identContext _localctx = new Var_or_identContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_var_or_ident);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(326);
			_la = _input.LA(1);
			if ( !(_la==VARIABLE || _la==IDENT) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ReferenceContext extends ParserRuleContext {
		public TerminalNode EntityRef() { return getToken(APiParser.EntityRef, 0); }
		public TerminalNode CharRef() { return getToken(APiParser.CharRef, 0); }
		public ReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitReference(this);
		}
	}

	public final ReferenceContext reference() throws RecognitionException {
		ReferenceContext _localctx = new ReferenceContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_reference);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(328);
			_la = _input.LA(1);
			if ( !(_la==T__3 || _la==T__4) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AttributeContext extends ParserRuleContext {
		public Var_or_identContext var_or_ident() {
			return getRuleContext(Var_or_identContext.class,0);
		}
		public TerminalNode VARIABLE() { return getToken(APiParser.VARIABLE, 0); }
		public TerminalNode STRING() { return getToken(APiParser.STRING, 0); }
		public AttributeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_attribute; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterAttribute(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitAttribute(this);
		}
	}

	public final AttributeContext attribute() throws RecognitionException {
		AttributeContext _localctx = new AttributeContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_attribute);
		try {
			setState(338);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,30,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				{
				setState(330);
				var_or_ident();
				setState(331);
				match(T__16);
				setState(332);
				match(VARIABLE);
				}
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				{
				setState(334);
				var_or_ident();
				setState(335);
				match(T__16);
				setState(336);
				match(STRING);
				}
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ChardataContext extends ParserRuleContext {
		public List<TerminalNode> TEXT() { return getTokens(APiParser.TEXT); }
		public TerminalNode TEXT(int i) {
			return getToken(APiParser.TEXT, i);
		}
		public List<TerminalNode> SEA_WS() { return getTokens(APiParser.SEA_WS); }
		public TerminalNode SEA_WS(int i) {
			return getToken(APiParser.SEA_WS, i);
		}
		public List<ValueContext> value() {
			return getRuleContexts(ValueContext.class);
		}
		public ValueContext value(int i) {
			return getRuleContext(ValueContext.class,i);
		}
		public List<TerminalNode> IDENT() { return getTokens(APiParser.IDENT); }
		public TerminalNode IDENT(int i) {
			return getToken(APiParser.IDENT, i);
		}
		public List<TerminalNode> VARIABLE() { return getTokens(APiParser.VARIABLE); }
		public TerminalNode VARIABLE(int i) {
			return getToken(APiParser.VARIABLE, i);
		}
		public ChardataContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chardata; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterChardata(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitChardata(this);
		}
	}

	public final ChardataContext chardata() throws RecognitionException {
		ChardataContext _localctx = new ChardataContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_chardata);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(345); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					setState(345);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,31,_ctx) ) {
					case 1:
						{
						setState(340);
						match(T__8);
						}
						break;
					case 2:
						{
						setState(341);
						match(T__5);
						}
						break;
					case 3:
						{
						setState(342);
						value();
						}
						break;
					case 4:
						{
						setState(343);
						match(IDENT);
						}
						break;
					case 5:
						{
						setState(344);
						match(VARIABLE);
						}
						break;
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(347); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,32,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class MiscContext extends ParserRuleContext {
		public TerminalNode COMMENTXML() { return getToken(APiParser.COMMENTXML, 0); }
		public TerminalNode PI() { return getToken(APiParser.PI, 0); }
		public TerminalNode SEA_WS() { return getToken(APiParser.SEA_WS, 0); }
		public MiscContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_misc; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterMisc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitMisc(this);
		}
	}

	public final MiscContext misc() throws RecognitionException {
		MiscContext _localctx = new MiscContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_misc);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(349);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__0) | (1L << T__5) | (1L << STDOUT))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 5:
			return pi_expr_sempred((Pi_exprContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean pi_expr_sempred(Pi_exprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 5);
		case 1:
			return precpred(_ctx, 4);
		case 2:
			return precpred(_ctx, 3);
		case 3:
			return precpred(_ctx, 2);
		case 4:
			return precpred(_ctx, 6);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\63\u0162\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2M\n\2\f\2\16\2P\13\2\3"+
		"\3\3\3\3\3\3\3\3\3\6\3W\n\3\r\3\16\3X\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5"+
		"\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\5\7p\n\7\3\7\3\7"+
		"\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7\177\n\7\f\7\16\7\u0082"+
		"\13\7\3\b\3\b\3\b\5\b\u0087\n\b\3\b\3\b\3\b\6\b\u008c\n\b\r\b\16\b\u008d"+
		"\3\t\3\t\3\t\7\t\u0093\n\t\f\t\16\t\u0096\13\t\3\t\3\t\3\n\3\n\3\n\3\n"+
		"\3\n\3\n\7\n\u00a0\n\n\f\n\16\n\u00a3\13\n\3\n\3\n\3\13\3\13\3\f\3\f\3"+
		"\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\17"+
		"\3\17\3\17\3\17\3\20\3\20\3\20\5\20\u00c1\n\20\3\21\3\21\5\21\u00c5\n"+
		"\21\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\26\3\26\3"+
		"\26\3\26\7\26\u00d6\n\26\f\26\16\26\u00d9\13\26\3\26\3\26\3\26\3\26\5"+
		"\26\u00df\n\26\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u00e7\n\27\3\30\3\30"+
		"\3\30\3\30\7\30\u00ed\n\30\f\30\16\30\u00f0\13\30\3\30\3\30\3\30\3\30"+
		"\5\30\u00f6\n\30\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\5\31\u0101"+
		"\n\31\3\32\5\32\u0104\n\32\3\32\7\32\u0107\n\32\f\32\16\32\u010a\13\32"+
		"\3\32\3\32\7\32\u010e\n\32\f\32\16\32\u0111\13\32\3\33\3\33\7\33\u0115"+
		"\n\33\f\33\16\33\u0118\13\33\3\33\3\33\3\34\5\34\u011d\n\34\3\34\3\34"+
		"\3\34\3\34\3\34\5\34\u0124\n\34\3\34\5\34\u0127\n\34\7\34\u0129\n\34\f"+
		"\34\16\34\u012c\13\34\3\35\3\35\3\35\7\35\u0131\n\35\f\35\16\35\u0134"+
		"\13\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\7\35\u0140\n"+
		"\35\f\35\16\35\u0143\13\35\3\35\3\35\5\35\u0147\n\35\3\36\3\36\3\37\3"+
		"\37\3 \3 \3 \3 \3 \3 \3 \3 \5 \u0155\n \3!\3!\3!\3!\3!\6!\u015c\n!\r!"+
		"\16!\u015d\3\"\3\"\3\"\3N\3\f#\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36"+
		" \"$&(*,.\60\62\64\668:<>@B\2\6\6\2\24\27\37\37((\60\60\3\2/\60\3\2\6"+
		"\7\5\2\3\3\b\b\25\25\2\u0178\2N\3\2\2\2\4Q\3\2\2\2\6Z\3\2\2\2\b`\3\2\2"+
		"\2\nf\3\2\2\2\fo\3\2\2\2\16\u0083\3\2\2\2\20\u008f\3\2\2\2\22\u0099\3"+
		"\2\2\2\24\u00a6\3\2\2\2\26\u00a8\3\2\2\2\30\u00ae\3\2\2\2\32\u00b3\3\2"+
		"\2\2\34\u00b9\3\2\2\2\36\u00c0\3\2\2\2 \u00c4\3\2\2\2\"\u00c6\3\2\2\2"+
		"$\u00c9\3\2\2\2&\u00cc\3\2\2\2(\u00cf\3\2\2\2*\u00de\3\2\2\2,\u00e6\3"+
		"\2\2\2.\u00f5\3\2\2\2\60\u0100\3\2\2\2\62\u0103\3\2\2\2\64\u0112\3\2\2"+
		"\2\66\u011c\3\2\2\28\u0146\3\2\2\2:\u0148\3\2\2\2<\u014a\3\2\2\2>\u0154"+
		"\3\2\2\2@\u015b\3\2\2\2B\u015f\3\2\2\2DM\5\34\17\2EM\5\4\3\2FM\5\26\f"+
		"\2GM\5\30\r\2HM\5\16\b\2IM\5\n\6\2JM\7)\2\2KM\7,\2\2LD\3\2\2\2LE\3\2\2"+
		"\2LF\3\2\2\2LG\3\2\2\2LH\3\2\2\2LI\3\2\2\2LJ\3\2\2\2LK\3\2\2\2MP\3\2\2"+
		"\2NO\3\2\2\2NL\3\2\2\2O\3\3\2\2\2PN\3\2\2\2QR\7\31\2\2RS\7\3\2\2SV\7,"+
		"\2\2TW\5\6\4\2UW\5\b\5\2VT\3\2\2\2VU\3\2\2\2WX\3\2\2\2XV\3\2\2\2XY\3\2"+
		"\2\2Y\5\3\2\2\2Z[\7-\2\2[\\\7\60\2\2\\]\7%\2\2]^\5\36\20\2^_\7,\2\2_\7"+
		"\3\2\2\2`a\7-\2\2ab\7\60\2\2bc\7&\2\2cd\5 \21\2de\7,\2\2e\t\3\2\2\2fg"+
		"\7\36\2\2gh\5\f\7\2h\13\3\2\2\2ij\b\7\1\2jk\7\4\2\2kl\5\f\7\2lm\7\5\2"+
		"\2mp\3\2\2\2np\7\60\2\2oi\3\2\2\2on\3\2\2\2p\u0080\3\2\2\2qr\f\7\2\2r"+
		"s\7\35\2\2s\177\5\f\7\btu\f\6\2\2uv\7\32\2\2v\177\5\f\7\7wx\f\5\2\2xy"+
		"\7\33\2\2y\177\5\f\7\6z{\f\4\2\2{\177\5\f\7\5|}\f\b\2\2}\177\7\34\2\2"+
		"~q\3\2\2\2~t\3\2\2\2~w\3\2\2\2~z\3\2\2\2~|\3\2\2\2\177\u0082\3\2\2\2\u0080"+
		"~\3\2\2\2\u0080\u0081\3\2\2\2\u0081\r\3\2\2\2\u0082\u0080\3\2\2\2\u0083"+
		"\u0084\7 \2\2\u0084\u0086\7\60\2\2\u0085\u0087\5\20\t\2\u0086\u0085\3"+
		"\2\2\2\u0086\u0087\3\2\2\2\u0087\u0088\3\2\2\2\u0088\u0089\7\3\2\2\u0089"+
		"\u008b\7,\2\2\u008a\u008c\5\22\n\2\u008b\u008a\3\2\2\2\u008c\u008d\3\2"+
		"\2\2\u008d\u008b\3\2\2\2\u008d\u008e\3\2\2\2\u008e\17\3\2\2\2\u008f\u0090"+
		"\7\4\2\2\u0090\u0094\7\60\2\2\u0091\u0093\7\60\2\2\u0092\u0091\3\2\2\2"+
		"\u0093\u0096\3\2\2\2\u0094\u0092\3\2\2\2\u0094\u0095\3\2\2\2\u0095\u0097"+
		"\3\2\2\2\u0096\u0094\3\2\2\2\u0097\u0098\7\5\2\2\u0098\21\3\2\2\2\u0099"+
		"\u009a\7-\2\2\u009a\u009b\5\24\13\2\u009b\u009c\7\'\2\2\u009c\u00a1\5"+
		"\24\13\2\u009d\u009e\7\'\2\2\u009e\u00a0\5\24\13\2\u009f\u009d\3\2\2\2"+
		"\u00a0\u00a3\3\2\2\2\u00a1\u009f\3\2\2\2\u00a1\u00a2\3\2\2\2\u00a2\u00a4"+
		"\3\2\2\2\u00a3\u00a1\3\2\2\2\u00a4\u00a5\7,\2\2\u00a5\23\3\2\2\2\u00a6"+
		"\u00a7\t\2\2\2\u00a7\25\3\2\2\2\u00a8\u00a9\7!\2\2\u00a9\u00aa\7\60\2"+
		"\2\u00aa\u00ab\7\3\2\2\u00ab\u00ac\7,\2\2\u00ac\u00ad\5\32\16\2\u00ad"+
		"\27\3\2\2\2\u00ae\u00af\7!\2\2\u00af\u00b0\7\60\2\2\u00b0\u00b1\7\6\2"+
		"\2\u00b1\u00b2\7,\2\2\u00b2\31\3\2\2\2\u00b3\u00b4\7-\2\2\u00b4\u00b5"+
		"\5\36\20\2\u00b5\u00b6\7\'\2\2\u00b6\u00b7\5 \21\2\u00b7\u00b8\7,\2\2"+
		"\u00b8\33\3\2\2\2\u00b9\u00ba\7\30\2\2\u00ba\u00bb\7\60\2\2\u00bb\u00bc"+
		"\7,\2\2\u00bc\35\3\2\2\2\u00bd\u00c1\5$\23\2\u00be\u00c1\5\"\22\2\u00bf"+
		"\u00c1\5&\24\2\u00c0\u00bd\3\2\2\2\u00c0\u00be\3\2\2\2\u00c0\u00bf\3\2"+
		"\2\2\u00c1\37\3\2\2\2\u00c2\u00c5\5$\23\2\u00c3\u00c5\5\"\22\2\u00c4\u00c2"+
		"\3\2\2\2\u00c4\u00c3\3\2\2\2\u00c5!\3\2\2\2\u00c6\u00c7\7$\2\2\u00c7\u00c8"+
		"\5\62\32\2\u00c8#\3\2\2\2\u00c9\u00ca\7#\2\2\u00ca\u00cb\5(\25\2\u00cb"+
		"%\3\2\2\2\u00cc\u00cd\7\"\2\2\u00cd\u00ce\7\61\2\2\u00ce\'\3\2\2\2\u00cf"+
		"\u00d0\5\60\31\2\u00d0)\3\2\2\2\u00d1\u00d2\7\7\2\2\u00d2\u00d7\5,\27"+
		"\2\u00d3\u00d4\7\b\2\2\u00d4\u00d6\5,\27\2\u00d5\u00d3\3\2\2\2\u00d6\u00d9"+
		"\3\2\2\2\u00d7\u00d5\3\2\2\2\u00d7\u00d8\3\2\2\2\u00d8\u00da\3\2\2\2\u00d9"+
		"\u00d7\3\2\2\2\u00da\u00db\7\t\2\2\u00db\u00df\3\2\2\2\u00dc\u00dd\7\7"+
		"\2\2\u00dd\u00df\7\t\2\2\u00de\u00d1\3\2\2\2\u00de\u00dc\3\2\2\2\u00df"+
		"+\3\2\2\2\u00e0\u00e1\7\61\2\2\u00e1\u00e2\7\3\2\2\u00e2\u00e7\5\60\31"+
		"\2\u00e3\u00e4\7/\2\2\u00e4\u00e5\7\3\2\2\u00e5\u00e7\5\60\31\2\u00e6"+
		"\u00e0\3\2\2\2\u00e6\u00e3\3\2\2\2\u00e7-\3\2\2\2\u00e8\u00e9\7\n\2\2"+
		"\u00e9\u00ee\5\60\31\2\u00ea\u00eb\7\b\2\2\u00eb\u00ed\5\60\31\2\u00ec"+
		"\u00ea\3\2\2\2\u00ed\u00f0\3\2\2\2\u00ee\u00ec\3\2\2\2\u00ee\u00ef\3\2"+
		"\2\2\u00ef\u00f1\3\2\2\2\u00f0\u00ee\3\2\2\2\u00f1\u00f2\7\13\2\2\u00f2"+
		"\u00f6\3\2\2\2\u00f3\u00f4\7\n\2\2\u00f4\u00f6\7\13\2\2\u00f5\u00e8\3"+
		"\2\2\2\u00f5\u00f3\3\2\2\2\u00f6/\3\2\2\2\u00f7\u0101\7/\2\2\u00f8\u0101"+
		"\7\61\2\2\u00f9\u0101\7\62\2\2\u00fa\u0101\7.\2\2\u00fb\u0101\5*\26\2"+
		"\u00fc\u0101\5.\30\2\u00fd\u0101\7\f\2\2\u00fe\u0101\7\r\2\2\u00ff\u0101"+
		"\7\16\2\2\u0100\u00f7\3\2\2\2\u0100\u00f8\3\2\2\2\u0100\u00f9\3\2\2\2"+
		"\u0100\u00fa\3\2\2\2\u0100\u00fb\3\2\2\2\u0100\u00fc\3\2\2\2\u0100\u00fd"+
		"\3\2\2\2\u0100\u00fe\3\2\2\2\u0100\u00ff\3\2\2\2\u0101\61\3\2\2\2\u0102"+
		"\u0104\5\64\33\2\u0103\u0102\3\2\2\2\u0103\u0104\3\2\2\2\u0104\u0108\3"+
		"\2\2\2\u0105\u0107\5B\"\2\u0106\u0105\3\2\2\2\u0107\u010a\3\2\2\2\u0108"+
		"\u0106\3\2\2\2\u0108\u0109\3\2\2\2\u0109\u010b\3\2\2\2\u010a\u0108\3\2"+
		"\2\2\u010b\u010f\58\35\2\u010c\u010e\5B\"\2\u010d\u010c\3\2\2\2\u010e"+
		"\u0111\3\2\2\2\u010f\u010d\3\2\2\2\u010f\u0110\3\2\2\2\u0110\63\3\2\2"+
		"\2\u0111\u010f\3\2\2\2\u0112\u0116\7\n\2\2\u0113\u0115\5> \2\u0114\u0113"+
		"\3\2\2\2\u0115\u0118\3\2\2\2\u0116\u0114\3\2\2\2\u0116\u0117\3\2\2\2\u0117"+
		"\u0119\3\2\2\2\u0118\u0116\3\2\2\2\u0119\u011a\7\r\2\2\u011a\65\3\2\2"+
		"\2\u011b\u011d\5@!\2\u011c\u011b\3\2\2\2\u011c\u011d\3\2\2\2\u011d\u012a"+
		"\3\2\2\2\u011e\u0124\58\35\2\u011f\u0124\5<\37\2\u0120\u0124\7\4\2\2\u0121"+
		"\u0124\7\25\2\2\u0122\u0124\7\3\2\2\u0123\u011e\3\2\2\2\u0123\u011f\3"+
		"\2\2\2\u0123\u0120\3\2\2\2\u0123\u0121\3\2\2\2\u0123\u0122\3\2\2\2\u0124"+
		"\u0126\3\2\2\2\u0125\u0127\5@!\2\u0126\u0125\3\2\2\2\u0126\u0127\3\2\2"+
		"\2\u0127\u0129\3\2\2\2\u0128\u0123\3\2\2\2\u0129\u012c\3\2\2\2\u012a\u0128"+
		"\3\2\2\2\u012a\u012b\3\2\2\2\u012b\67\3\2\2\2\u012c\u012a\3\2\2\2\u012d"+
		"\u012e\7\17\2\2\u012e\u0132\5:\36\2\u012f\u0131\5> \2\u0130\u012f\3\2"+
		"\2\2\u0131\u0134\3\2\2\2\u0132\u0130\3\2\2\2\u0132\u0133\3\2\2\2\u0133"+
		"\u0135\3\2\2\2\u0134\u0132\3\2\2\2\u0135\u0136\7\20\2\2\u0136\u0137\5"+
		"\66\34\2\u0137\u0138\7\17\2\2\u0138\u0139\7\21\2\2\u0139\u013a\5:\36\2"+
		"\u013a\u013b\7\20\2\2\u013b\u0147\3\2\2\2\u013c\u013d\7\17\2\2\u013d\u0141"+
		"\5:\36\2\u013e\u0140\5> \2\u013f\u013e\3\2\2\2\u0140\u0143\3\2\2\2\u0141"+
		"\u013f\3\2\2\2\u0141\u0142\3\2\2\2\u0142\u0144\3\2\2\2\u0143\u0141\3\2"+
		"\2\2\u0144\u0145\7\22\2\2\u0145\u0147\3\2\2\2\u0146\u012d\3\2\2\2\u0146"+
		"\u013c\3\2\2\2\u01479\3\2\2\2\u0148\u0149\t\3\2\2\u0149;\3\2\2\2\u014a"+
		"\u014b\t\4\2\2\u014b=\3\2\2\2\u014c\u014d\5:\36\2\u014d\u014e\7\23\2\2"+
		"\u014e\u014f\7/\2\2\u014f\u0155\3\2\2\2\u0150\u0151\5:\36\2\u0151\u0152"+
		"\7\23\2\2\u0152\u0153\7\61\2\2\u0153\u0155\3\2\2\2\u0154\u014c\3\2\2\2"+
		"\u0154\u0150\3\2\2\2\u0155?\3\2\2\2\u0156\u015c\7\13\2\2\u0157\u015c\7"+
		"\b\2\2\u0158\u015c\5\60\31\2\u0159\u015c\7\60\2\2\u015a\u015c\7/\2\2\u015b"+
		"\u0156\3\2\2\2\u015b\u0157\3\2\2\2\u015b\u0158\3\2\2\2\u015b\u0159\3\2"+
		"\2\2\u015b\u015a\3\2\2\2\u015c\u015d\3\2\2\2\u015d\u015b\3\2\2\2\u015d"+
		"\u015e\3\2\2\2\u015eA\3\2\2\2\u015f\u0160\t\5\2\2\u0160C\3\2\2\2#LNVX"+
		"o~\u0080\u0086\u008d\u0094\u00a1\u00c0\u00c4\u00d7\u00de\u00e6\u00ee\u00f5"+
		"\u0100\u0103\u0108\u010f\u0116\u011c\u0123\u0126\u012a\u0132\u0141\u0146"+
		"\u0154\u015b\u015d";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}