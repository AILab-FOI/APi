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
		T__9=10, T__10=11, T__11=12, STDIN=13, STDOUT=14, STDERR=15, VOID=16, 
		IMPORT=17, ENVIRONMENT=18, ONSUCCESS=19, ONFAIL=20, RESTART=21, PARALLEL=22, 
		START=23, SELF=24, AGENT=25, CHANNEL=26, FORMAT=27, SENDS=28, NIL=29, 
		COMMENT=30, COMMENT1=31, COMMENT2=32, NEWLINE=33, TAB=34, VARIABLE=35, 
		IDENT=36, STRING=37, NUMBER=38, SPACE=39;
	public static final int
		RULE_api_program = 0, RULE_s_environment = 1, RULE_ioflow = 2, RULE_s_start = 3, 
		RULE_pi_expr = 4, RULE_s_agent = 5, RULE_arglist = 6, RULE_flow = 7, RULE_valid_channel = 8, 
		RULE_s_channel = 9, RULE_s_channel_transformer = 10, RULE_s_channel_spec = 11, 
		RULE_s_import = 12, RULE_json = 13, RULE_obj = 14, RULE_pair = 15, RULE_arr = 16, 
		RULE_value = 17;
	private static String[] makeRuleNames() {
		return new String[] {
			"api_program", "s_environment", "ioflow", "s_start", "pi_expr", "s_agent", 
			"arglist", "flow", "valid_channel", "s_channel", "s_channel_transformer", 
			"s_channel_spec", "s_import", "json", "obj", "pair", "arr", "value"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "':'", "'('", "')'", "'.'", "'{'", "','", "'}'", "'['", "']'", 
			"'true'", "'false'", "'null'", "'stdin'", "'stdout'", "'stderr'", "'void'", 
			"'import'", "'environment'", "'&'", "'!'", "'+'", "'|'", "'start'", "'self'", 
			"'agent'", "'channel'", "'<->'", "'->'", "'0'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "STDIN", "STDOUT", "STDERR", "VOID", "IMPORT", "ENVIRONMENT", "ONSUCCESS", 
			"ONFAIL", "RESTART", "PARALLEL", "START", "SELF", "AGENT", "CHANNEL", 
			"FORMAT", "SENDS", "NIL", "COMMENT", "COMMENT1", "COMMENT2", "NEWLINE", 
			"TAB", "VARIABLE", "IDENT", "STRING", "NUMBER", "SPACE"
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
			setState(46);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=1 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1+1 ) {
					{
					setState(44);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
					case 1:
						{
						setState(36);
						s_import();
						}
						break;
					case 2:
						{
						setState(37);
						s_environment();
						}
						break;
					case 3:
						{
						setState(38);
						s_channel();
						}
						break;
					case 4:
						{
						setState(39);
						s_channel_transformer();
						}
						break;
					case 5:
						{
						setState(40);
						s_agent();
						}
						break;
					case 6:
						{
						setState(41);
						s_start();
						}
						break;
					case 7:
						{
						setState(42);
						match(COMMENT);
						}
						break;
					case 8:
						{
						setState(43);
						match(NEWLINE);
						}
						break;
					}
					} 
				}
				setState(48);
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
			setState(49);
			match(ENVIRONMENT);
			setState(50);
			match(T__0);
			setState(51);
			match(NEWLINE);
			setState(53); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(52);
				ioflow();
				}
				}
				setState(55); 
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
		public JsonContext json() {
			return getRuleContext(JsonContext.class,0);
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
			setState(57);
			match(IDENT);
			setState(58);
			match(FORMAT);
			setState(59);
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
			setState(61);
			match(START);
			setState(62);
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
			setState(70);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
				{
				setState(65);
				match(T__1);
				setState(66);
				pi_expr(0);
				setState(67);
				match(T__2);
				}
				break;
			case IDENT:
				{
				setState(69);
				match(IDENT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(87);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(85);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
					case 1:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(72);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(73);
						match(PARALLEL);
						setState(74);
						pi_expr(6);
						}
						break;
					case 2:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(75);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(76);
						match(ONSUCCESS);
						setState(77);
						pi_expr(5);
						}
						break;
					case 3:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(78);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(79);
						match(ONFAIL);
						setState(80);
						pi_expr(4);
						}
						break;
					case 4:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(81);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(82);
						pi_expr(3);
						}
						break;
					case 5:
						{
						_localctx = new Pi_exprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_pi_expr);
						setState(83);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(84);
						match(RESTART);
						}
						break;
					}
					} 
				}
				setState(89);
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
			setState(90);
			match(AGENT);
			setState(91);
			match(IDENT);
			setState(93);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(92);
				arglist();
				}
			}

			setState(95);
			match(T__0);
			setState(96);
			match(NEWLINE);
			setState(98); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(97);
				flow();
				}
				}
				setState(100); 
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
			setState(102);
			match(T__1);
			setState(103);
			match(IDENT);
			setState(107);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==IDENT) {
				{
				{
				setState(104);
				match(IDENT);
				}
				}
				setState(109);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(110);
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
			setState(112);
			match(TAB);
			setState(113);
			valid_channel();
			setState(114);
			match(SENDS);
			setState(115);
			valid_channel();
			setState(120);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==SENDS) {
				{
				{
				setState(116);
				match(SENDS);
				setState(117);
				valid_channel();
				}
				}
				setState(122);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(123);
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
			setState(125);
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
			setState(127);
			match(CHANNEL);
			setState(128);
			match(IDENT);
			setState(129);
			match(T__0);
			setState(130);
			match(NEWLINE);
			setState(131);
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
			setState(133);
			match(CHANNEL);
			setState(134);
			match(IDENT);
			setState(135);
			match(T__3);
			setState(136);
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
		public List<JsonContext> json() {
			return getRuleContexts(JsonContext.class);
		}
		public JsonContext json(int i) {
			return getRuleContext(JsonContext.class,i);
		}
		public TerminalNode SENDS() { return getToken(APiParser.SENDS, 0); }
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
			setState(138);
			match(TAB);
			setState(139);
			json();
			setState(140);
			match(SENDS);
			setState(141);
			json();
			setState(142);
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
			setState(144);
			match(IMPORT);
			setState(145);
			match(IDENT);
			setState(146);
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
		enterRule(_localctx, 26, RULE_json);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(148);
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
		enterRule(_localctx, 28, RULE_obj);
		int _la;
		try {
			setState(163);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(150);
				match(T__4);
				setState(151);
				pair();
				setState(156);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__5) {
					{
					{
					setState(152);
					match(T__5);
					setState(153);
					pair();
					}
					}
					setState(158);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(159);
				match(T__6);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(161);
				match(T__4);
				setState(162);
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
		enterRule(_localctx, 30, RULE_pair);
		try {
			setState(171);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(165);
				match(STRING);
				setState(166);
				match(T__0);
				setState(167);
				value();
				}
				break;
			case VARIABLE:
				enterOuterAlt(_localctx, 2);
				{
				setState(168);
				match(VARIABLE);
				setState(169);
				match(T__0);
				setState(170);
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
		enterRule(_localctx, 32, RULE_arr);
		int _la;
		try {
			setState(186);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,14,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(173);
				match(T__7);
				setState(174);
				value();
				setState(179);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__5) {
					{
					{
					setState(175);
					match(T__5);
					setState(176);
					value();
					}
					}
					setState(181);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(182);
				match(T__8);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(184);
				match(T__7);
				setState(185);
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
		enterRule(_localctx, 34, RULE_value);
		try {
			setState(196);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case VARIABLE:
				enterOuterAlt(_localctx, 1);
				{
				setState(188);
				match(VARIABLE);
				}
				break;
			case STRING:
				enterOuterAlt(_localctx, 2);
				{
				setState(189);
				match(STRING);
				}
				break;
			case NUMBER:
				enterOuterAlt(_localctx, 3);
				{
				setState(190);
				match(NUMBER);
				}
				break;
			case T__4:
				enterOuterAlt(_localctx, 4);
				{
				setState(191);
				obj();
				}
				break;
			case T__7:
				enterOuterAlt(_localctx, 5);
				{
				setState(192);
				arr();
				}
				break;
			case T__9:
				enterOuterAlt(_localctx, 6);
				{
				setState(193);
				match(T__9);
				}
				break;
			case T__10:
				enterOuterAlt(_localctx, 7);
				{
				setState(194);
				match(T__10);
				}
				break;
			case T__11:
				enterOuterAlt(_localctx, 8);
				{
				setState(195);
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3)\u00c9\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2/\n\2\f\2\16\2\62\13\2\3"+
		"\3\3\3\3\3\3\3\6\38\n\3\r\3\16\39\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6"+
		"\3\6\3\6\3\6\3\6\5\6I\n\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6"+
		"\3\6\3\6\7\6X\n\6\f\6\16\6[\13\6\3\7\3\7\3\7\5\7`\n\7\3\7\3\7\3\7\6\7"+
		"e\n\7\r\7\16\7f\3\b\3\b\3\b\7\bl\n\b\f\b\16\bo\13\b\3\b\3\b\3\t\3\t\3"+
		"\t\3\t\3\t\3\t\7\ty\n\t\f\t\16\t|\13\t\3\t\3\t\3\n\3\n\3\13\3\13\3\13"+
		"\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16"+
		"\3\16\3\16\3\17\3\17\3\20\3\20\3\20\3\20\7\20\u009d\n\20\f\20\16\20\u00a0"+
		"\13\20\3\20\3\20\3\20\3\20\5\20\u00a6\n\20\3\21\3\21\3\21\3\21\3\21\3"+
		"\21\5\21\u00ae\n\21\3\22\3\22\3\22\3\22\7\22\u00b4\n\22\f\22\16\22\u00b7"+
		"\13\22\3\22\3\22\3\22\3\22\5\22\u00bd\n\22\3\23\3\23\3\23\3\23\3\23\3"+
		"\23\3\23\3\23\5\23\u00c7\n\23\3\23\3\60\3\n\24\2\4\6\b\n\f\16\20\22\24"+
		"\26\30\32\34\36 \"$\2\3\6\2\17\22\32\32\37\37&&\2\u00d5\2\60\3\2\2\2\4"+
		"\63\3\2\2\2\6;\3\2\2\2\b?\3\2\2\2\nH\3\2\2\2\f\\\3\2\2\2\16h\3\2\2\2\20"+
		"r\3\2\2\2\22\177\3\2\2\2\24\u0081\3\2\2\2\26\u0087\3\2\2\2\30\u008c\3"+
		"\2\2\2\32\u0092\3\2\2\2\34\u0096\3\2\2\2\36\u00a5\3\2\2\2 \u00ad\3\2\2"+
		"\2\"\u00bc\3\2\2\2$\u00c6\3\2\2\2&/\5\32\16\2\'/\5\4\3\2(/\5\24\13\2)"+
		"/\5\26\f\2*/\5\f\7\2+/\5\b\5\2,/\7 \2\2-/\7#\2\2.&\3\2\2\2.\'\3\2\2\2"+
		".(\3\2\2\2.)\3\2\2\2.*\3\2\2\2.+\3\2\2\2.,\3\2\2\2.-\3\2\2\2/\62\3\2\2"+
		"\2\60\61\3\2\2\2\60.\3\2\2\2\61\3\3\2\2\2\62\60\3\2\2\2\63\64\7\24\2\2"+
		"\64\65\7\3\2\2\65\67\7#\2\2\668\5\6\4\2\67\66\3\2\2\289\3\2\2\29\67\3"+
		"\2\2\29:\3\2\2\2:\5\3\2\2\2;<\7&\2\2<=\7\35\2\2=>\5\34\17\2>\7\3\2\2\2"+
		"?@\7\31\2\2@A\5\n\6\2A\t\3\2\2\2BC\b\6\1\2CD\7\4\2\2DE\5\n\6\2EF\7\5\2"+
		"\2FI\3\2\2\2GI\7&\2\2HB\3\2\2\2HG\3\2\2\2IY\3\2\2\2JK\f\7\2\2KL\7\30\2"+
		"\2LX\5\n\6\bMN\f\6\2\2NO\7\25\2\2OX\5\n\6\7PQ\f\5\2\2QR\7\26\2\2RX\5\n"+
		"\6\6ST\f\4\2\2TX\5\n\6\5UV\f\b\2\2VX\7\27\2\2WJ\3\2\2\2WM\3\2\2\2WP\3"+
		"\2\2\2WS\3\2\2\2WU\3\2\2\2X[\3\2\2\2YW\3\2\2\2YZ\3\2\2\2Z\13\3\2\2\2["+
		"Y\3\2\2\2\\]\7\33\2\2]_\7&\2\2^`\5\16\b\2_^\3\2\2\2_`\3\2\2\2`a\3\2\2"+
		"\2ab\7\3\2\2bd\7#\2\2ce\5\20\t\2dc\3\2\2\2ef\3\2\2\2fd\3\2\2\2fg\3\2\2"+
		"\2g\r\3\2\2\2hi\7\4\2\2im\7&\2\2jl\7&\2\2kj\3\2\2\2lo\3\2\2\2mk\3\2\2"+
		"\2mn\3\2\2\2np\3\2\2\2om\3\2\2\2pq\7\5\2\2q\17\3\2\2\2rs\7$\2\2st\5\22"+
		"\n\2tu\7\36\2\2uz\5\22\n\2vw\7\36\2\2wy\5\22\n\2xv\3\2\2\2y|\3\2\2\2z"+
		"x\3\2\2\2z{\3\2\2\2{}\3\2\2\2|z\3\2\2\2}~\7#\2\2~\21\3\2\2\2\177\u0080"+
		"\t\2\2\2\u0080\23\3\2\2\2\u0081\u0082\7\34\2\2\u0082\u0083\7&\2\2\u0083"+
		"\u0084\7\3\2\2\u0084\u0085\7#\2\2\u0085\u0086\5\30\r\2\u0086\25\3\2\2"+
		"\2\u0087\u0088\7\34\2\2\u0088\u0089\7&\2\2\u0089\u008a\7\6\2\2\u008a\u008b"+
		"\7#\2\2\u008b\27\3\2\2\2\u008c\u008d\7$\2\2\u008d\u008e\5\34\17\2\u008e"+
		"\u008f\7\36\2\2\u008f\u0090\5\34\17\2\u0090\u0091\7#\2\2\u0091\31\3\2"+
		"\2\2\u0092\u0093\7\23\2\2\u0093\u0094\7&\2\2\u0094\u0095\7#\2\2\u0095"+
		"\33\3\2\2\2\u0096\u0097\5$\23\2\u0097\35\3\2\2\2\u0098\u0099\7\7\2\2\u0099"+
		"\u009e\5 \21\2\u009a\u009b\7\b\2\2\u009b\u009d\5 \21\2\u009c\u009a\3\2"+
		"\2\2\u009d\u00a0\3\2\2\2\u009e\u009c\3\2\2\2\u009e\u009f\3\2\2\2\u009f"+
		"\u00a1\3\2\2\2\u00a0\u009e\3\2\2\2\u00a1\u00a2\7\t\2\2\u00a2\u00a6\3\2"+
		"\2\2\u00a3\u00a4\7\7\2\2\u00a4\u00a6\7\t\2\2\u00a5\u0098\3\2\2\2\u00a5"+
		"\u00a3\3\2\2\2\u00a6\37\3\2\2\2\u00a7\u00a8\7\'\2\2\u00a8\u00a9\7\3\2"+
		"\2\u00a9\u00ae\5$\23\2\u00aa\u00ab\7%\2\2\u00ab\u00ac\7\3\2\2\u00ac\u00ae"+
		"\5$\23\2\u00ad\u00a7\3\2\2\2\u00ad\u00aa\3\2\2\2\u00ae!\3\2\2\2\u00af"+
		"\u00b0\7\n\2\2\u00b0\u00b5\5$\23\2\u00b1\u00b2\7\b\2\2\u00b2\u00b4\5$"+
		"\23\2\u00b3\u00b1\3\2\2\2\u00b4\u00b7\3\2\2\2\u00b5\u00b3\3\2\2\2\u00b5"+
		"\u00b6\3\2\2\2\u00b6\u00b8\3\2\2\2\u00b7\u00b5\3\2\2\2\u00b8\u00b9\7\13"+
		"\2\2\u00b9\u00bd\3\2\2\2\u00ba\u00bb\7\n\2\2\u00bb\u00bd\7\13\2\2\u00bc"+
		"\u00af\3\2\2\2\u00bc\u00ba\3\2\2\2\u00bd#\3\2\2\2\u00be\u00c7\7%\2\2\u00bf"+
		"\u00c7\7\'\2\2\u00c0\u00c7\7(\2\2\u00c1\u00c7\5\36\20\2\u00c2\u00c7\5"+
		"\"\22\2\u00c3\u00c7\7\f\2\2\u00c4\u00c7\7\r\2\2\u00c5\u00c7\7\16\2\2\u00c6"+
		"\u00be\3\2\2\2\u00c6\u00bf\3\2\2\2\u00c6\u00c0\3\2\2\2\u00c6\u00c1\3\2"+
		"\2\2\u00c6\u00c2\3\2\2\2\u00c6\u00c3\3\2\2\2\u00c6\u00c4\3\2\2\2\u00c6"+
		"\u00c5\3\2\2\2\u00c7%\3\2\2\2\22.\609HWY_fmz\u009e\u00a5\u00ad\u00b5\u00bc"+
		"\u00c6";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}