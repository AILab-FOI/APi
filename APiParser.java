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
		REGEX=32, JSON=33, XML=34, FORMAT=35, SENDS=36, NIL=37, COMMENT=38, COMMENT1=39, 
		COMMENT2=40, NEWLINE=41, TAB=42, SPEC_CHAR=43, VARIABLE=44, IDENT=45, 
		STRING=46, NUMBER=47, SPACE=48, COMMENTXML=1, CDATA=2, DTD=3, EntityRef=4, 
		CharRef=5, SEA_WS=6, OPEN=7, XMLDeclOpen=8, TEXT=9, CLOSE=10, SPECIAL_CLOSE=11, 
		SLASH_CLOSE=12, SLASH=13, EQUALS=14, STRINGXML=15, Name=16, S=17, PI=19;
	public static final int
		RULE_api_program = 0, RULE_s_environment = 1, RULE_ioflow = 2, RULE_s_start = 3, 
		RULE_pi_expr = 4, RULE_s_agent = 5, RULE_arglist = 6, RULE_flow = 7, RULE_valid_channel = 8, 
		RULE_s_channel = 9, RULE_s_channel_transformer = 10, RULE_s_channel_spec = 11, 
		RULE_s_import = 12, RULE_s_input = 13, RULE_s_output = 14, RULE_s_xml = 15, 
		RULE_s_json = 16, RULE_s_regex = 17, RULE_json = 18, RULE_obj = 19, RULE_pair = 20, 
		RULE_arr = 21, RULE_value = 22, RULE_xml = 23, RULE_prolog = 24, RULE_content = 25, 
		RULE_element = 26, RULE_var_or_ident = 27, RULE_reference = 28, RULE_attribute = 29, 
		RULE_chardata = 30, RULE_misc = 31;
	private static String[] makeRuleNames() {
		return new String[] {
			"api_program", "s_environment", "ioflow", "s_start", "pi_expr", "s_agent", 
			"arglist", "flow", "valid_channel", "s_channel", "s_channel_transformer", 
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
			"'json'", "'xml'", "'<->'", "'->'", "'0'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, "STDIN", "STDOUT", "STDERR", "VOID", 
			"IMPORT", "ENVIRONMENT", "ONSUCCESS", "ONFAIL", "RESTART", "PARALLEL", 
			"START", "SELF", "AGENT", "CHANNEL", "REGEX", "JSON", "XML", "FORMAT", 
			"SENDS", "NIL", "COMMENT", "COMMENT1", "COMMENT2", "NEWLINE", "TAB", 
			"SPEC_CHAR", "VARIABLE", "IDENT", "STRING", "NUMBER", "SPACE"
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
			setState(74);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=1 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1+1 ) {
					{
					setState(72);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
					case 1:
						{
						setState(64);
						s_import();
						}
						break;
					case 2:
						{
						setState(65);
						s_environment();
						}
						break;
					case 3:
						{
						setState(66);
						s_channel();
						}
						break;
					case 4:
						{
						setState(67);
						s_channel_transformer();
						}
						break;
					case 5:
						{
						setState(68);
						s_agent();
						}
						break;
					case 6:
						{
						setState(69);
						s_start();
						}
						break;
					case 7:
						{
						setState(70);
						match(COMMENT);
						}
						break;
					case 8:
						{
						setState(71);
						match(NEWLINE);
						}
						break;
					}
					} 
				}
				setState(76);
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
		public List<IoflowContext> ioflow() {
			return getRuleContexts(IoflowContext.class);
		}
		public IoflowContext ioflow(int i) {
			return getRuleContext(IoflowContext.class,i);
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
			setState(77);
			match(ENVIRONMENT);
			setState(78);
			match(T__0);
			setState(79);
			match(NEWLINE);
			setState(81); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(80);
				ioflow();
				}
				}
				setState(83); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==IDENT );
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

	public static class IoflowContext extends ParserRuleContext {
		public TerminalNode IDENT() { return getToken(APiParser.IDENT, 0); }
		public TerminalNode FORMAT() { return getToken(APiParser.FORMAT, 0); }
		public S_inputContext s_input() {
			return getRuleContext(S_inputContext.class,0);
		}
		public IoflowContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ioflow; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).enterIoflow(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof APiListener ) ((APiListener)listener).exitIoflow(this);
		}
	}

	public final IoflowContext ioflow() throws RecognitionException {
		IoflowContext _localctx = new IoflowContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_ioflow);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(85);
			match(IDENT);
			setState(86);
			match(FORMAT);
			setState(87);
			s_input();
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
		enterRule(_localctx, 6, RULE_s_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(89);
			match(START);
			setState(90);
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
		int _startState = 8;
		enterRecursionRule(_localctx, 8, RULE_pi_expr, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(98);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
				{
				setState(93);
				match(T__1);
				setState(94);
				pi_expr(0);
				setState(95);
				match(T__2);
				}
				break;
			case IDENT:
				{
				setState(97);
				match(IDENT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(115);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(113);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
					case 1:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(100);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(101);
						match(PARALLEL);
						setState(102);
						pi_expr(6);
						}
						break;
					case 2:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(103);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(104);
						match(ONSUCCESS);
						setState(105);
						pi_expr(5);
						}
						break;
					case 3:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(106);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(107);
						match(ONFAIL);
						setState(108);
						pi_expr(4);
						}
						break;
					case 4:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(109);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(110);
						pi_expr(3);
						}
						break;
					case 5:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(111);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(112);
						match(RESTART);
						}
						break;
					}
					} 
				}
				setState(117);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
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
		enterRule(_localctx, 10, RULE_s_agent);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(118);
			match(AGENT);
			setState(119);
			match(IDENT);
			setState(121);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(120);
				arglist();
				}
			}

			setState(123);
			match(T__0);
			setState(124);
			match(NEWLINE);
			setState(126); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(125);
				flow();
				}
				}
				setState(128); 
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
		enterRule(_localctx, 12, RULE_arglist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(130);
			match(T__1);
			setState(131);
			match(IDENT);
			setState(135);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==IDENT) {
				{
				{
				setState(132);
				match(IDENT);
				}
				}
				setState(137);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(138);
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
		enterRule(_localctx, 14, RULE_flow);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(140);
			match(TAB);
			setState(141);
			valid_channel();
			setState(142);
			match(SENDS);
			setState(143);
			valid_channel();
			setState(148);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==SENDS) {
				{
				{
				setState(144);
				match(SENDS);
				setState(145);
				valid_channel();
				}
				}
				setState(150);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(151);
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
		enterRule(_localctx, 16, RULE_valid_channel);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(153);
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
		enterRule(_localctx, 18, RULE_s_channel);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(155);
			match(CHANNEL);
			setState(156);
			match(IDENT);
			setState(157);
			match(T__0);
			setState(158);
			match(NEWLINE);
			setState(159);
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
		enterRule(_localctx, 20, RULE_s_channel_transformer);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(161);
			match(CHANNEL);
			setState(162);
			match(IDENT);
			setState(163);
			match(T__3);
			setState(164);
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
		enterRule(_localctx, 22, RULE_s_channel_spec);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(166);
			match(TAB);
			setState(167);
			s_input();
			setState(168);
			match(SENDS);
			setState(169);
			s_output();
			setState(170);
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
		enterRule(_localctx, 24, RULE_s_import);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(172);
			match(IMPORT);
			setState(173);
			match(IDENT);
			setState(174);
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
		enterRule(_localctx, 26, RULE_s_input);
		try {
			setState(179);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case JSON:
				enterOuterAlt(_localctx, 1);
				{
				setState(176);
				s_json();
				}
				break;
			case XML:
				enterOuterAlt(_localctx, 2);
				{
				setState(177);
				s_xml();
				}
				break;
			case REGEX:
				enterOuterAlt(_localctx, 3);
				{
				setState(178);
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
		enterRule(_localctx, 28, RULE_s_output);
		try {
			setState(183);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case JSON:
				enterOuterAlt(_localctx, 1);
				{
				setState(181);
				s_json();
				}
				break;
			case XML:
				enterOuterAlt(_localctx, 2);
				{
				setState(182);
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
		enterRule(_localctx, 30, RULE_s_xml);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(185);
			match(XML);
			setState(186);
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
		enterRule(_localctx, 32, RULE_s_json);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(188);
			match(JSON);
			setState(189);
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
		enterRule(_localctx, 34, RULE_s_regex);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(191);
			match(REGEX);
			setState(192);
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
		enterRule(_localctx, 36, RULE_json);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(194);
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
		enterRule(_localctx, 38, RULE_obj);
		int _la;
		try {
			setState(209);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,13,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(196);
				match(T__4);
				setState(197);
				pair();
				setState(202);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__5) {
					{
					{
					setState(198);
					match(T__5);
					setState(199);
					pair();
					}
					}
					setState(204);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(205);
				match(T__6);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(207);
				match(T__4);
				setState(208);
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
		enterRule(_localctx, 40, RULE_pair);
		try {
			setState(217);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(211);
				match(STRING);
				setState(212);
				match(T__0);
				setState(213);
				value();
				}
				break;
			case VARIABLE:
				enterOuterAlt(_localctx, 2);
				{
				setState(214);
				match(VARIABLE);
				setState(215);
				match(T__0);
				setState(216);
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
		enterRule(_localctx, 42, RULE_arr);
		int _la;
		try {
			setState(232);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,16,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(219);
				match(T__7);
				setState(220);
				value();
				setState(225);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__5) {
					{
					{
					setState(221);
					match(T__5);
					setState(222);
					value();
					}
					}
					setState(227);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(228);
				match(T__8);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(230);
				match(T__7);
				setState(231);
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
		public TerminalNode TEXT() { return getToken(APiParser.TEXT, 0); }
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
		enterRule(_localctx, 44, RULE_value);
		try {
			setState(244);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case VARIABLE:
				enterOuterAlt(_localctx, 1);
				{
				setState(234);
				match(VARIABLE);
				}
				break;
			case T__8:
				enterOuterAlt(_localctx, 2);
				{
				setState(235);
				match(T__8);
				}
				break;
			case STRING:
				enterOuterAlt(_localctx, 3);
				{
				setState(236);
				match(STRING);
				}
				break;
			case NUMBER:
				enterOuterAlt(_localctx, 4);
				{
				setState(237);
				match(NUMBER);
				}
				break;
			case SPEC_CHAR:
				enterOuterAlt(_localctx, 5);
				{
				setState(238);
				match(SPEC_CHAR);
				}
				break;
			case T__4:
				enterOuterAlt(_localctx, 6);
				{
				setState(239);
				obj();
				}
				break;
			case T__7:
				enterOuterAlt(_localctx, 7);
				{
				setState(240);
				arr();
				}
				break;
			case T__9:
				enterOuterAlt(_localctx, 8);
				{
				setState(241);
				match(T__9);
				}
				break;
			case T__10:
				enterOuterAlt(_localctx, 9);
				{
				setState(242);
				match(T__10);
				}
				break;
			case T__11:
				enterOuterAlt(_localctx, 10);
				{
				setState(243);
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
		enterRule(_localctx, 46, RULE_xml);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(247);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__7) {
				{
				setState(246);
				prolog();
				}
			}

			setState(252);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__0) | (1L << T__5) | (1L << STDOUT))) != 0)) {
				{
				{
				setState(249);
				misc();
				}
				}
				setState(254);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(255);
			element();
			setState(259);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__0) | (1L << T__5) | (1L << STDOUT))) != 0)) {
				{
				{
				setState(256);
				misc();
				}
				}
				setState(261);
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
		enterRule(_localctx, 48, RULE_prolog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(262);
			match(T__7);
			setState(266);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==VARIABLE || _la==IDENT) {
				{
				{
				setState(263);
				attribute();
				}
				}
				setState(268);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(269);
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
		enterRule(_localctx, 50, RULE_content);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(272);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
			case 1:
				{
				setState(271);
				chardata();
				}
				break;
			}
			setState(286);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,25,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(279);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case T__12:
						{
						setState(274);
						element();
						}
						break;
					case T__3:
					case T__4:
						{
						setState(275);
						reference();
						}
						break;
					case T__1:
						{
						setState(276);
						match(T__1);
						}
						break;
					case STDOUT:
						{
						setState(277);
						match(STDOUT);
						}
						break;
					case T__0:
						{
						setState(278);
						match(T__0);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(282);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,24,_ctx) ) {
					case 1:
						{
						setState(281);
						chardata();
						}
						break;
					}
					}
					} 
				}
				setState(288);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,25,_ctx);
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
		enterRule(_localctx, 52, RULE_element);
		int _la;
		try {
			setState(314);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,28,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(289);
				match(T__12);
				setState(290);
				var_or_ident();
				setState(294);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==VARIABLE || _la==IDENT) {
					{
					{
					setState(291);
					attribute();
					}
					}
					setState(296);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(297);
				match(T__13);
				setState(298);
				content();
				setState(299);
				match(T__12);
				setState(300);
				match(T__14);
				setState(301);
				var_or_ident();
				setState(302);
				match(T__13);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(304);
				match(T__12);
				setState(305);
				var_or_ident();
				setState(309);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==VARIABLE || _la==IDENT) {
					{
					{
					setState(306);
					attribute();
					}
					}
					setState(311);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(312);
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
		enterRule(_localctx, 54, RULE_var_or_ident);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(316);
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
		enterRule(_localctx, 56, RULE_reference);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(318);
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
		enterRule(_localctx, 58, RULE_attribute);
		try {
			setState(328);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,29,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				{
				setState(320);
				var_or_ident();
				setState(321);
				match(T__16);
				setState(322);
				match(VARIABLE);
				}
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				{
				setState(324);
				var_or_ident();
				setState(325);
				match(T__16);
				setState(326);
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
		enterRule(_localctx, 60, RULE_chardata);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(335); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					setState(335);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,30,_ctx) ) {
					case 1:
						{
						setState(330);
						match(T__8);
						}
						break;
					case 2:
						{
						setState(331);
						match(T__5);
						}
						break;
					case 3:
						{
						setState(332);
						value();
						}
						break;
					case 4:
						{
						setState(333);
						match(IDENT);
						}
						break;
					case 5:
						{
						setState(334);
						match(VARIABLE);
						}
						break;
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(337); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,31,_ctx);
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
		enterRule(_localctx, 62, RULE_misc);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(339);
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
		case 4:
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\62\u0158\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2K\n\2\f\2\16\2N\13\2\3\3\3\3\3"+
		"\3\3\3\6\3T\n\3\r\3\16\3U\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\6\3\6"+
		"\3\6\3\6\5\6e\n\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6"+
		"\7\6t\n\6\f\6\16\6w\13\6\3\7\3\7\3\7\5\7|\n\7\3\7\3\7\3\7\6\7\u0081\n"+
		"\7\r\7\16\7\u0082\3\b\3\b\3\b\7\b\u0088\n\b\f\b\16\b\u008b\13\b\3\b\3"+
		"\b\3\t\3\t\3\t\3\t\3\t\3\t\7\t\u0095\n\t\f\t\16\t\u0098\13\t\3\t\3\t\3"+
		"\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3"+
		"\r\3\r\3\r\3\16\3\16\3\16\3\16\3\17\3\17\3\17\5\17\u00b6\n\17\3\20\3\20"+
		"\5\20\u00ba\n\20\3\21\3\21\3\21\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24"+
		"\3\25\3\25\3\25\3\25\7\25\u00cb\n\25\f\25\16\25\u00ce\13\25\3\25\3\25"+
		"\3\25\3\25\5\25\u00d4\n\25\3\26\3\26\3\26\3\26\3\26\3\26\5\26\u00dc\n"+
		"\26\3\27\3\27\3\27\3\27\7\27\u00e2\n\27\f\27\16\27\u00e5\13\27\3\27\3"+
		"\27\3\27\3\27\5\27\u00eb\n\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30"+
		"\3\30\3\30\5\30\u00f7\n\30\3\31\5\31\u00fa\n\31\3\31\7\31\u00fd\n\31\f"+
		"\31\16\31\u0100\13\31\3\31\3\31\7\31\u0104\n\31\f\31\16\31\u0107\13\31"+
		"\3\32\3\32\7\32\u010b\n\32\f\32\16\32\u010e\13\32\3\32\3\32\3\33\5\33"+
		"\u0113\n\33\3\33\3\33\3\33\3\33\3\33\5\33\u011a\n\33\3\33\5\33\u011d\n"+
		"\33\7\33\u011f\n\33\f\33\16\33\u0122\13\33\3\34\3\34\3\34\7\34\u0127\n"+
		"\34\f\34\16\34\u012a\13\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34"+
		"\3\34\7\34\u0136\n\34\f\34\16\34\u0139\13\34\3\34\3\34\5\34\u013d\n\34"+
		"\3\35\3\35\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\5\37\u014b"+
		"\n\37\3 \3 \3 \3 \3 \6 \u0152\n \r \16 \u0153\3!\3!\3!\3L\3\n\"\2\4\6"+
		"\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:<>@\2\6\6\2\24"+
		"\27\37\37\'\'//\3\2./\3\2\6\7\5\2\3\3\b\b\25\25\2\u016f\2L\3\2\2\2\4O"+
		"\3\2\2\2\6W\3\2\2\2\b[\3\2\2\2\nd\3\2\2\2\fx\3\2\2\2\16\u0084\3\2\2\2"+
		"\20\u008e\3\2\2\2\22\u009b\3\2\2\2\24\u009d\3\2\2\2\26\u00a3\3\2\2\2\30"+
		"\u00a8\3\2\2\2\32\u00ae\3\2\2\2\34\u00b5\3\2\2\2\36\u00b9\3\2\2\2 \u00bb"+
		"\3\2\2\2\"\u00be\3\2\2\2$\u00c1\3\2\2\2&\u00c4\3\2\2\2(\u00d3\3\2\2\2"+
		"*\u00db\3\2\2\2,\u00ea\3\2\2\2.\u00f6\3\2\2\2\60\u00f9\3\2\2\2\62\u0108"+
		"\3\2\2\2\64\u0112\3\2\2\2\66\u013c\3\2\2\28\u013e\3\2\2\2:\u0140\3\2\2"+
		"\2<\u014a\3\2\2\2>\u0151\3\2\2\2@\u0155\3\2\2\2BK\5\32\16\2CK\5\4\3\2"+
		"DK\5\24\13\2EK\5\26\f\2FK\5\f\7\2GK\5\b\5\2HK\7(\2\2IK\7+\2\2JB\3\2\2"+
		"\2JC\3\2\2\2JD\3\2\2\2JE\3\2\2\2JF\3\2\2\2JG\3\2\2\2JH\3\2\2\2JI\3\2\2"+
		"\2KN\3\2\2\2LM\3\2\2\2LJ\3\2\2\2M\3\3\2\2\2NL\3\2\2\2OP\7\31\2\2PQ\7\3"+
		"\2\2QS\7+\2\2RT\5\6\4\2SR\3\2\2\2TU\3\2\2\2US\3\2\2\2UV\3\2\2\2V\5\3\2"+
		"\2\2WX\7/\2\2XY\7%\2\2YZ\5\34\17\2Z\7\3\2\2\2[\\\7\36\2\2\\]\5\n\6\2]"+
		"\t\3\2\2\2^_\b\6\1\2_`\7\4\2\2`a\5\n\6\2ab\7\5\2\2be\3\2\2\2ce\7/\2\2"+
		"d^\3\2\2\2dc\3\2\2\2eu\3\2\2\2fg\f\7\2\2gh\7\35\2\2ht\5\n\6\bij\f\6\2"+
		"\2jk\7\32\2\2kt\5\n\6\7lm\f\5\2\2mn\7\33\2\2nt\5\n\6\6op\f\4\2\2pt\5\n"+
		"\6\5qr\f\b\2\2rt\7\34\2\2sf\3\2\2\2si\3\2\2\2sl\3\2\2\2so\3\2\2\2sq\3"+
		"\2\2\2tw\3\2\2\2us\3\2\2\2uv\3\2\2\2v\13\3\2\2\2wu\3\2\2\2xy\7 \2\2y{"+
		"\7/\2\2z|\5\16\b\2{z\3\2\2\2{|\3\2\2\2|}\3\2\2\2}~\7\3\2\2~\u0080\7+\2"+
		"\2\177\u0081\5\20\t\2\u0080\177\3\2\2\2\u0081\u0082\3\2\2\2\u0082\u0080"+
		"\3\2\2\2\u0082\u0083\3\2\2\2\u0083\r\3\2\2\2\u0084\u0085\7\4\2\2\u0085"+
		"\u0089\7/\2\2\u0086\u0088\7/\2\2\u0087\u0086\3\2\2\2\u0088\u008b\3\2\2"+
		"\2\u0089\u0087\3\2\2\2\u0089\u008a\3\2\2\2\u008a\u008c\3\2\2\2\u008b\u0089"+
		"\3\2\2\2\u008c\u008d\7\5\2\2\u008d\17\3\2\2\2\u008e\u008f\7,\2\2\u008f"+
		"\u0090\5\22\n\2\u0090\u0091\7&\2\2\u0091\u0096\5\22\n\2\u0092\u0093\7"+
		"&\2\2\u0093\u0095\5\22\n\2\u0094\u0092\3\2\2\2\u0095\u0098\3\2\2\2\u0096"+
		"\u0094\3\2\2\2\u0096\u0097\3\2\2\2\u0097\u0099\3\2\2\2\u0098\u0096\3\2"+
		"\2\2\u0099\u009a\7+\2\2\u009a\21\3\2\2\2\u009b\u009c\t\2\2\2\u009c\23"+
		"\3\2\2\2\u009d\u009e\7!\2\2\u009e\u009f\7/\2\2\u009f\u00a0\7\3\2\2\u00a0"+
		"\u00a1\7+\2\2\u00a1\u00a2\5\30\r\2\u00a2\25\3\2\2\2\u00a3\u00a4\7!\2\2"+
		"\u00a4\u00a5\7/\2\2\u00a5\u00a6\7\6\2\2\u00a6\u00a7\7+\2\2\u00a7\27\3"+
		"\2\2\2\u00a8\u00a9\7,\2\2\u00a9\u00aa\5\34\17\2\u00aa\u00ab\7&\2\2\u00ab"+
		"\u00ac\5\36\20\2\u00ac\u00ad\7+\2\2\u00ad\31\3\2\2\2\u00ae\u00af\7\30"+
		"\2\2\u00af\u00b0\7/\2\2\u00b0\u00b1\7+\2\2\u00b1\33\3\2\2\2\u00b2\u00b6"+
		"\5\"\22\2\u00b3\u00b6\5 \21\2\u00b4\u00b6\5$\23\2\u00b5\u00b2\3\2\2\2"+
		"\u00b5\u00b3\3\2\2\2\u00b5\u00b4\3\2\2\2\u00b6\35\3\2\2\2\u00b7\u00ba"+
		"\5\"\22\2\u00b8\u00ba\5 \21\2\u00b9\u00b7\3\2\2\2\u00b9\u00b8\3\2\2\2"+
		"\u00ba\37\3\2\2\2\u00bb\u00bc\7$\2\2\u00bc\u00bd\5\60\31\2\u00bd!\3\2"+
		"\2\2\u00be\u00bf\7#\2\2\u00bf\u00c0\5&\24\2\u00c0#\3\2\2\2\u00c1\u00c2"+
		"\7\"\2\2\u00c2\u00c3\7\60\2\2\u00c3%\3\2\2\2\u00c4\u00c5\5.\30\2\u00c5"+
		"\'\3\2\2\2\u00c6\u00c7\7\7\2\2\u00c7\u00cc\5*\26\2\u00c8\u00c9\7\b\2\2"+
		"\u00c9\u00cb\5*\26\2\u00ca\u00c8\3\2\2\2\u00cb\u00ce\3\2\2\2\u00cc\u00ca"+
		"\3\2\2\2\u00cc\u00cd\3\2\2\2\u00cd\u00cf\3\2\2\2\u00ce\u00cc\3\2\2\2\u00cf"+
		"\u00d0\7\t\2\2\u00d0\u00d4\3\2\2\2\u00d1\u00d2\7\7\2\2\u00d2\u00d4\7\t"+
		"\2\2\u00d3\u00c6\3\2\2\2\u00d3\u00d1\3\2\2\2\u00d4)\3\2\2\2\u00d5\u00d6"+
		"\7\60\2\2\u00d6\u00d7\7\3\2\2\u00d7\u00dc\5.\30\2\u00d8\u00d9\7.\2\2\u00d9"+
		"\u00da\7\3\2\2\u00da\u00dc\5.\30\2\u00db\u00d5\3\2\2\2\u00db\u00d8\3\2"+
		"\2\2\u00dc+\3\2\2\2\u00dd\u00de\7\n\2\2\u00de\u00e3\5.\30\2\u00df\u00e0"+
		"\7\b\2\2\u00e0\u00e2\5.\30\2\u00e1\u00df\3\2\2\2\u00e2\u00e5\3\2\2\2\u00e3"+
		"\u00e1\3\2\2\2\u00e3\u00e4\3\2\2\2\u00e4\u00e6\3\2\2\2\u00e5\u00e3\3\2"+
		"\2\2\u00e6\u00e7\7\13\2\2\u00e7\u00eb\3\2\2\2\u00e8\u00e9\7\n\2\2\u00e9"+
		"\u00eb\7\13\2\2\u00ea\u00dd\3\2\2\2\u00ea\u00e8\3\2\2\2\u00eb-\3\2\2\2"+
		"\u00ec\u00f7\7.\2\2\u00ed\u00f7\7\13\2\2\u00ee\u00f7\7\60\2\2\u00ef\u00f7"+
		"\7\61\2\2\u00f0\u00f7\7-\2\2\u00f1\u00f7\5(\25\2\u00f2\u00f7\5,\27\2\u00f3"+
		"\u00f7\7\f\2\2\u00f4\u00f7\7\r\2\2\u00f5\u00f7\7\16\2\2\u00f6\u00ec\3"+
		"\2\2\2\u00f6\u00ed\3\2\2\2\u00f6\u00ee\3\2\2\2\u00f6\u00ef\3\2\2\2\u00f6"+
		"\u00f0\3\2\2\2\u00f6\u00f1\3\2\2\2\u00f6\u00f2\3\2\2\2\u00f6\u00f3\3\2"+
		"\2\2\u00f6\u00f4\3\2\2\2\u00f6\u00f5\3\2\2\2\u00f7/\3\2\2\2\u00f8\u00fa"+
		"\5\62\32\2\u00f9\u00f8\3\2\2\2\u00f9\u00fa\3\2\2\2\u00fa\u00fe\3\2\2\2"+
		"\u00fb\u00fd\5@!\2\u00fc\u00fb\3\2\2\2\u00fd\u0100\3\2\2\2\u00fe\u00fc"+
		"\3\2\2\2\u00fe\u00ff\3\2\2\2\u00ff\u0101\3\2\2\2\u0100\u00fe\3\2\2\2\u0101"+
		"\u0105\5\66\34\2\u0102\u0104\5@!\2\u0103\u0102\3\2\2\2\u0104\u0107\3\2"+
		"\2\2\u0105\u0103\3\2\2\2\u0105\u0106\3\2\2\2\u0106\61\3\2\2\2\u0107\u0105"+
		"\3\2\2\2\u0108\u010c\7\n\2\2\u0109\u010b\5<\37\2\u010a\u0109\3\2\2\2\u010b"+
		"\u010e\3\2\2\2\u010c\u010a\3\2\2\2\u010c\u010d\3\2\2\2\u010d\u010f\3\2"+
		"\2\2\u010e\u010c\3\2\2\2\u010f\u0110\7\r\2\2\u0110\63\3\2\2\2\u0111\u0113"+
		"\5> \2\u0112\u0111\3\2\2\2\u0112\u0113\3\2\2\2\u0113\u0120\3\2\2\2\u0114"+
		"\u011a\5\66\34\2\u0115\u011a\5:\36\2\u0116\u011a\7\4\2\2\u0117\u011a\7"+
		"\25\2\2\u0118\u011a\7\3\2\2\u0119\u0114\3\2\2\2\u0119\u0115\3\2\2\2\u0119"+
		"\u0116\3\2\2\2\u0119\u0117\3\2\2\2\u0119\u0118\3\2\2\2\u011a\u011c\3\2"+
		"\2\2\u011b\u011d\5> \2\u011c\u011b\3\2\2\2\u011c\u011d\3\2\2\2\u011d\u011f"+
		"\3\2\2\2\u011e\u0119\3\2\2\2\u011f\u0122\3\2\2\2\u0120\u011e\3\2\2\2\u0120"+
		"\u0121\3\2\2\2\u0121\65\3\2\2\2\u0122\u0120\3\2\2\2\u0123\u0124\7\17\2"+
		"\2\u0124\u0128\58\35\2\u0125\u0127\5<\37\2\u0126\u0125\3\2\2\2\u0127\u012a"+
		"\3\2\2\2\u0128\u0126\3\2\2\2\u0128\u0129\3\2\2\2\u0129\u012b\3\2\2\2\u012a"+
		"\u0128\3\2\2\2\u012b\u012c\7\20\2\2\u012c\u012d\5\64\33\2\u012d\u012e"+
		"\7\17\2\2\u012e\u012f\7\21\2\2\u012f\u0130\58\35\2\u0130\u0131\7\20\2"+
		"\2\u0131\u013d\3\2\2\2\u0132\u0133\7\17\2\2\u0133\u0137\58\35\2\u0134"+
		"\u0136\5<\37\2\u0135\u0134\3\2\2\2\u0136\u0139\3\2\2\2\u0137\u0135\3\2"+
		"\2\2\u0137\u0138\3\2\2\2\u0138\u013a\3\2\2\2\u0139\u0137\3\2\2\2\u013a"+
		"\u013b\7\22\2\2\u013b\u013d\3\2\2\2\u013c\u0123\3\2\2\2\u013c\u0132\3"+
		"\2\2\2\u013d\67\3\2\2\2\u013e\u013f\t\3\2\2\u013f9\3\2\2\2\u0140\u0141"+
		"\t\4\2\2\u0141;\3\2\2\2\u0142\u0143\58\35\2\u0143\u0144\7\23\2\2\u0144"+
		"\u0145\7.\2\2\u0145\u014b\3\2\2\2\u0146\u0147\58\35\2\u0147\u0148\7\23"+
		"\2\2\u0148\u0149\7\60\2\2\u0149\u014b\3\2\2\2\u014a\u0142\3\2\2\2\u014a"+
		"\u0146\3\2\2\2\u014b=\3\2\2\2\u014c\u0152\7\13\2\2\u014d\u0152\7\b\2\2"+
		"\u014e\u0152\5.\30\2\u014f\u0152\7/\2\2\u0150\u0152\7.\2\2\u0151\u014c"+
		"\3\2\2\2\u0151\u014d\3\2\2\2\u0151\u014e\3\2\2\2\u0151\u014f\3\2\2\2\u0151"+
		"\u0150\3\2\2\2\u0152\u0153\3\2\2\2\u0153\u0151\3\2\2\2\u0153\u0154\3\2"+
		"\2\2\u0154?\3\2\2\2\u0155\u0156\t\5\2\2\u0156A\3\2\2\2\"JLUdsu{\u0082"+
		"\u0089\u0096\u00b5\u00b9\u00cc\u00d3\u00db\u00e3\u00ea\u00f6\u00f9\u00fe"+
		"\u0105\u010c\u0112\u0119\u011c\u0120\u0128\u0137\u013c\u014a\u0151\u0153";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}