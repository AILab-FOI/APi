// Generated from APi.g4 by ANTLR 4.9
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class APiLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, STDIN=12, STDOUT=13, STDERR=14, VOID=15, IMPORT=16, 
		ENVIRONMENT=17, ONSUCCESS=18, ONFAIL=19, RESTART=20, PARALLEL=21, START=22, 
		SELF=23, AGENT=24, CHANNEL=25, FORMAT=26, SENDS=27, NIL=28, COMMENT=29, 
		COMMENT1=30, COMMENT2=31, NEWLINE=32, TAB=33, VARIABLE=34, IDENT=35, STRING=36, 
		NUMBER=37, SPACE=38;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "STDIN", "STDOUT", "STDERR", "VOID", "IMPORT", "ENVIRONMENT", 
			"ONSUCCESS", "ONFAIL", "RESTART", "PARALLEL", "START", "SELF", "AGENT", 
			"CHANNEL", "FORMAT", "SENDS", "NIL", "COMMENT", "COMMENT1", "COMMENT2", 
			"NEWLINE", "TAB", "VARIABLE", "IDENT", "STRING", "ESC1", "ESC2", "UNICODE", 
			"HEX", "SAFECODEPOINT1", "SAFECODEPOINT2", "NUMBER", "INT", "EXP", "SPACE"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "':'", "'('", "')'", "'{'", "','", "'}'", "'['", "']'", "'true'", 
			"'false'", "'null'", "'stdin'", "'stdout'", "'stderr'", "'void'", "'import'", 
			"'environment'", "'&'", "'!'", "'+'", "'|'", "'start'", "'self'", "'agent'", 
			"'channel'", "'<->'", "'->'", "'0'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			"STDIN", "STDOUT", "STDERR", "VOID", "IMPORT", "ENVIRONMENT", "ONSUCCESS", 
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


	public APiLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "APi.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2(\u014c\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\4/\t/\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7"+
		"\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\f"+
		"\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16"+
		"\3\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\21"+
		"\3\21\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22"+
		"\3\22\3\22\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\27\3\27"+
		"\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3\31"+
		"\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\34"+
		"\3\34\3\34\3\35\3\35\3\36\3\36\5\36\u00d8\n\36\3\37\3\37\3\37\3\37\7\37"+
		"\u00de\n\37\f\37\16\37\u00e1\13\37\3 \3 \3 \3 \7 \u00e7\n \f \16 \u00ea"+
		"\13 \3 \3 \3 \3!\3!\3\"\3\"\3#\3#\3#\3$\3$\7$\u00f8\n$\f$\16$\u00fb\13"+
		"$\3%\3%\3%\7%\u0100\n%\f%\16%\u0103\13%\3%\3%\3%\3%\7%\u0109\n%\f%\16"+
		"%\u010c\13%\3%\5%\u010f\n%\3&\3&\3&\5&\u0114\n&\3\'\3\'\3\'\5\'\u0119"+
		"\n\'\3(\3(\3(\3(\3(\3(\3)\3)\3*\3*\3+\3+\3,\5,\u0128\n,\3,\3,\3,\6,\u012d"+
		"\n,\r,\16,\u012e\5,\u0131\n,\3,\5,\u0134\n,\3-\3-\3-\7-\u0139\n-\f-\16"+
		"-\u013c\13-\5-\u013e\n-\3.\3.\5.\u0142\n.\3.\3.\3/\6/\u0147\n/\r/\16/"+
		"\u0148\3/\3/\3\u00e8\2\60\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25"+
		"\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32"+
		"\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\2M\2O\2Q\2S\2U\2W\'Y\2[\2]"+
		"(\3\2\20\3\2\f\f\3\2\13\13\5\2C\\aac|\5\2\62;C\\c|\n\2$$\61\61^^ddhhp"+
		"pttvv\n\2))\61\61^^ddhhppttvv\5\2\62;CHch\5\2\2!$$^^\5\2\2!))^^\3\2\62"+
		";\3\2\63;\4\2GGgg\4\2--//\4\2\17\17\"\"\2\u0156\2\3\3\2\2\2\2\5\3\2\2"+
		"\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21"+
		"\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2"+
		"\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3"+
		"\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3"+
		"\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3"+
		"\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2W\3\2\2"+
		"\2\2]\3\2\2\2\3_\3\2\2\2\5a\3\2\2\2\7c\3\2\2\2\te\3\2\2\2\13g\3\2\2\2"+
		"\ri\3\2\2\2\17k\3\2\2\2\21m\3\2\2\2\23o\3\2\2\2\25t\3\2\2\2\27z\3\2\2"+
		"\2\31\177\3\2\2\2\33\u0085\3\2\2\2\35\u008c\3\2\2\2\37\u0093\3\2\2\2!"+
		"\u0098\3\2\2\2#\u009f\3\2\2\2%\u00ab\3\2\2\2\'\u00ad\3\2\2\2)\u00af\3"+
		"\2\2\2+\u00b1\3\2\2\2-\u00b3\3\2\2\2/\u00b9\3\2\2\2\61\u00be\3\2\2\2\63"+
		"\u00c4\3\2\2\2\65\u00cc\3\2\2\2\67\u00d0\3\2\2\29\u00d3\3\2\2\2;\u00d7"+
		"\3\2\2\2=\u00d9\3\2\2\2?\u00e2\3\2\2\2A\u00ee\3\2\2\2C\u00f0\3\2\2\2E"+
		"\u00f2\3\2\2\2G\u00f5\3\2\2\2I\u010e\3\2\2\2K\u0110\3\2\2\2M\u0115\3\2"+
		"\2\2O\u011a\3\2\2\2Q\u0120\3\2\2\2S\u0122\3\2\2\2U\u0124\3\2\2\2W\u0127"+
		"\3\2\2\2Y\u013d\3\2\2\2[\u013f\3\2\2\2]\u0146\3\2\2\2_`\7<\2\2`\4\3\2"+
		"\2\2ab\7*\2\2b\6\3\2\2\2cd\7+\2\2d\b\3\2\2\2ef\7}\2\2f\n\3\2\2\2gh\7."+
		"\2\2h\f\3\2\2\2ij\7\177\2\2j\16\3\2\2\2kl\7]\2\2l\20\3\2\2\2mn\7_\2\2"+
		"n\22\3\2\2\2op\7v\2\2pq\7t\2\2qr\7w\2\2rs\7g\2\2s\24\3\2\2\2tu\7h\2\2"+
		"uv\7c\2\2vw\7n\2\2wx\7u\2\2xy\7g\2\2y\26\3\2\2\2z{\7p\2\2{|\7w\2\2|}\7"+
		"n\2\2}~\7n\2\2~\30\3\2\2\2\177\u0080\7u\2\2\u0080\u0081\7v\2\2\u0081\u0082"+
		"\7f\2\2\u0082\u0083\7k\2\2\u0083\u0084\7p\2\2\u0084\32\3\2\2\2\u0085\u0086"+
		"\7u\2\2\u0086\u0087\7v\2\2\u0087\u0088\7f\2\2\u0088\u0089\7q\2\2\u0089"+
		"\u008a\7w\2\2\u008a\u008b\7v\2\2\u008b\34\3\2\2\2\u008c\u008d\7u\2\2\u008d"+
		"\u008e\7v\2\2\u008e\u008f\7f\2\2\u008f\u0090\7g\2\2\u0090\u0091\7t\2\2"+
		"\u0091\u0092\7t\2\2\u0092\36\3\2\2\2\u0093\u0094\7x\2\2\u0094\u0095\7"+
		"q\2\2\u0095\u0096\7k\2\2\u0096\u0097\7f\2\2\u0097 \3\2\2\2\u0098\u0099"+
		"\7k\2\2\u0099\u009a\7o\2\2\u009a\u009b\7r\2\2\u009b\u009c\7q\2\2\u009c"+
		"\u009d\7t\2\2\u009d\u009e\7v\2\2\u009e\"\3\2\2\2\u009f\u00a0\7g\2\2\u00a0"+
		"\u00a1\7p\2\2\u00a1\u00a2\7x\2\2\u00a2\u00a3\7k\2\2\u00a3\u00a4\7t\2\2"+
		"\u00a4\u00a5\7q\2\2\u00a5\u00a6\7p\2\2\u00a6\u00a7\7o\2\2\u00a7\u00a8"+
		"\7g\2\2\u00a8\u00a9\7p\2\2\u00a9\u00aa\7v\2\2\u00aa$\3\2\2\2\u00ab\u00ac"+
		"\7(\2\2\u00ac&\3\2\2\2\u00ad\u00ae\7#\2\2\u00ae(\3\2\2\2\u00af\u00b0\7"+
		"-\2\2\u00b0*\3\2\2\2\u00b1\u00b2\7~\2\2\u00b2,\3\2\2\2\u00b3\u00b4\7u"+
		"\2\2\u00b4\u00b5\7v\2\2\u00b5\u00b6\7c\2\2\u00b6\u00b7\7t\2\2\u00b7\u00b8"+
		"\7v\2\2\u00b8.\3\2\2\2\u00b9\u00ba\7u\2\2\u00ba\u00bb\7g\2\2\u00bb\u00bc"+
		"\7n\2\2\u00bc\u00bd\7h\2\2\u00bd\60\3\2\2\2\u00be\u00bf\7c\2\2\u00bf\u00c0"+
		"\7i\2\2\u00c0\u00c1\7g\2\2\u00c1\u00c2\7p\2\2\u00c2\u00c3\7v\2\2\u00c3"+
		"\62\3\2\2\2\u00c4\u00c5\7e\2\2\u00c5\u00c6\7j\2\2\u00c6\u00c7\7c\2\2\u00c7"+
		"\u00c8\7p\2\2\u00c8\u00c9\7p\2\2\u00c9\u00ca\7g\2\2\u00ca\u00cb\7n\2\2"+
		"\u00cb\64\3\2\2\2\u00cc\u00cd\7>\2\2\u00cd\u00ce\7/\2\2\u00ce\u00cf\7"+
		"@\2\2\u00cf\66\3\2\2\2\u00d0\u00d1\7/\2\2\u00d1\u00d2\7@\2\2\u00d28\3"+
		"\2\2\2\u00d3\u00d4\7\62\2\2\u00d4:\3\2\2\2\u00d5\u00d8\5=\37\2\u00d6\u00d8"+
		"\5? \2\u00d7\u00d5\3\2\2\2\u00d7\u00d6\3\2\2\2\u00d8<\3\2\2\2\u00d9\u00da"+
		"\7\61\2\2\u00da\u00db\7\61\2\2\u00db\u00df\3\2\2\2\u00dc\u00de\n\2\2\2"+
		"\u00dd\u00dc\3\2\2\2\u00de\u00e1\3\2\2\2\u00df\u00dd\3\2\2\2\u00df\u00e0"+
		"\3\2\2\2\u00e0>\3\2\2\2\u00e1\u00df\3\2\2\2\u00e2\u00e3\7\61\2\2\u00e3"+
		"\u00e4\7,\2\2\u00e4\u00e8\3\2\2\2\u00e5\u00e7\13\2\2\2\u00e6\u00e5\3\2"+
		"\2\2\u00e7\u00ea\3\2\2\2\u00e8\u00e9\3\2\2\2\u00e8\u00e6\3\2\2\2\u00e9"+
		"\u00eb\3\2\2\2\u00ea\u00e8\3\2\2\2\u00eb\u00ec\7,\2\2\u00ec\u00ed\7\61"+
		"\2\2\u00ed@\3\2\2\2\u00ee\u00ef\t\2\2\2\u00efB\3\2\2\2\u00f0\u00f1\t\3"+
		"\2\2\u00f1D\3\2\2\2\u00f2\u00f3\7A\2\2\u00f3\u00f4\5G$\2\u00f4F\3\2\2"+
		"\2\u00f5\u00f9\t\4\2\2\u00f6\u00f8\t\5\2\2\u00f7\u00f6\3\2\2\2\u00f8\u00fb"+
		"\3\2\2\2\u00f9\u00f7\3\2\2\2\u00f9\u00fa\3\2\2\2\u00faH\3\2\2\2\u00fb"+
		"\u00f9\3\2\2\2\u00fc\u0101\7$\2\2\u00fd\u0100\5K&\2\u00fe\u0100\5S*\2"+
		"\u00ff\u00fd\3\2\2\2\u00ff\u00fe\3\2\2\2\u0100\u0103\3\2\2\2\u0101\u00ff"+
		"\3\2\2\2\u0101\u0102\3\2\2\2\u0102\u0104\3\2\2\2\u0103\u0101\3\2\2\2\u0104"+
		"\u010f\7$\2\2\u0105\u010a\7)\2\2\u0106\u0109\5M\'\2\u0107\u0109\5U+\2"+
		"\u0108\u0106\3\2\2\2\u0108\u0107\3\2\2\2\u0109\u010c\3\2\2\2\u010a\u0108"+
		"\3\2\2\2\u010a\u010b\3\2\2\2\u010b\u010d\3\2\2\2\u010c\u010a\3\2\2\2\u010d"+
		"\u010f\7)\2\2\u010e\u00fc\3\2\2\2\u010e\u0105\3\2\2\2\u010fJ\3\2\2\2\u0110"+
		"\u0113\7^\2\2\u0111\u0114\t\6\2\2\u0112\u0114\5O(\2\u0113\u0111\3\2\2"+
		"\2\u0113\u0112\3\2\2\2\u0114L\3\2\2\2\u0115\u0118\7^\2\2\u0116\u0119\t"+
		"\7\2\2\u0117\u0119\5O(\2\u0118\u0116\3\2\2\2\u0118\u0117\3\2\2\2\u0119"+
		"N\3\2\2\2\u011a\u011b\7w\2\2\u011b\u011c\5Q)\2\u011c\u011d\5Q)\2\u011d"+
		"\u011e\5Q)\2\u011e\u011f\5Q)\2\u011fP\3\2\2\2\u0120\u0121\t\b\2\2\u0121"+
		"R\3\2\2\2\u0122\u0123\n\t\2\2\u0123T\3\2\2\2\u0124\u0125\n\n\2\2\u0125"+
		"V\3\2\2\2\u0126\u0128\7/\2\2\u0127\u0126\3\2\2\2\u0127\u0128\3\2\2\2\u0128"+
		"\u0129\3\2\2\2\u0129\u0130\5Y-\2\u012a\u012c\7\60\2\2\u012b\u012d\t\13"+
		"\2\2\u012c\u012b\3\2\2\2\u012d\u012e\3\2\2\2\u012e\u012c\3\2\2\2\u012e"+
		"\u012f\3\2\2\2\u012f\u0131\3\2\2\2\u0130\u012a\3\2\2\2\u0130\u0131\3\2"+
		"\2\2\u0131\u0133\3\2\2\2\u0132\u0134\5[.\2\u0133\u0132\3\2\2\2\u0133\u0134"+
		"\3\2\2\2\u0134X\3\2\2\2\u0135\u013e\7\62\2\2\u0136\u013a\t\f\2\2\u0137"+
		"\u0139\t\13\2\2\u0138\u0137\3\2\2\2\u0139\u013c\3\2\2\2\u013a\u0138\3"+
		"\2\2\2\u013a\u013b\3\2\2\2\u013b\u013e\3\2\2\2\u013c\u013a\3\2\2\2\u013d"+
		"\u0135\3\2\2\2\u013d\u0136\3\2\2\2\u013eZ\3\2\2\2\u013f\u0141\t\r\2\2"+
		"\u0140\u0142\t\16\2\2\u0141\u0140\3\2\2\2\u0141\u0142\3\2\2\2\u0142\u0143"+
		"\3\2\2\2\u0143\u0144\5Y-\2\u0144\\\3\2\2\2\u0145\u0147\t\17\2\2\u0146"+
		"\u0145\3\2\2\2\u0147\u0148\3\2\2\2\u0148\u0146\3\2\2\2\u0148\u0149\3\2"+
		"\2\2\u0149\u014a\3\2\2\2\u014a\u014b\b/\2\2\u014b^\3\2\2\2\26\2\u00d7"+
		"\u00df\u00e8\u00f9\u00ff\u0101\u0108\u010a\u010e\u0113\u0118\u0127\u012e"+
		"\u0130\u0133\u013a\u013d\u0141\u0148\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}