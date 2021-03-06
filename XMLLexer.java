// Generated from XMLLexer.g4 by ANTLR 4.9
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class XMLLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		COMMENTXML=1, CDATA=2, DTD=3, EntityRef=4, CharRef=5, SEA_WS=6, OPEN=7, 
		XMLDeclOpen=8, TEXT=9, CLOSE=10, SPECIAL_CLOSE=11, SLASH_CLOSE=12, SLASH=13, 
		EQUALS=14, STRINGXML=15, Name=16, S=17, IDENT=18, PI=19;
	public static final int
		INSIDE=1, PROC_INSTR=2;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE", "INSIDE", "PROC_INSTR"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"COMMENTXML", "CDATA", "DTD", "EntityRef", "CharRef", "SEA_WS", "OPEN", 
			"XMLDeclOpen", "SPECIAL_OPEN", "TEXT", "CLOSE", "SPECIAL_CLOSE", "SLASH_CLOSE", 
			"SLASH", "EQUALS", "STRINGXML", "Name", "S", "HEXDIGIT", "DIGIT", "NameChar", 
			"NameStartChar", "IDENT", "NameChar1", "NameStartChar1", "INT", "PI", 
			"IGNORE"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, null, null, null, null, null, "'<'", null, null, "'>'", null, 
			"'/>'", "'/'", "'='"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "COMMENTXML", "CDATA", "DTD", "EntityRef", "CharRef", "SEA_WS", 
			"OPEN", "XMLDeclOpen", "TEXT", "CLOSE", "SPECIAL_CLOSE", "SLASH_CLOSE", 
			"SLASH", "EQUALS", "STRINGXML", "Name", "S", "IDENT", "PI"
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


	public XMLLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "XMLLexer.g4"; }

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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\25\u010b\b\1\b\1"+
		"\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4"+
		"\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t"+
		"\21\4\22\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t"+
		"\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\3\2\3\2\3\2\3\2"+
		"\3\2\3\2\7\2D\n\2\f\2\16\2G\13\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3"+
		"\3\3\3\3\3\3\3\3\3\3\3\7\3X\n\3\f\3\16\3[\13\3\3\3\3\3\3\3\3\3\3\4\3\4"+
		"\3\4\3\4\7\4e\n\4\f\4\16\4h\13\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3"+
		"\6\3\6\3\6\6\6v\n\6\r\6\16\6w\3\6\3\6\3\6\3\6\3\6\3\6\3\6\6\6\u0081\n"+
		"\6\r\6\16\6\u0082\3\6\3\6\5\6\u0087\n\6\3\7\3\7\5\7\u008b\n\7\3\7\6\7"+
		"\u008e\n\7\r\7\16\7\u008f\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\6\13\u00a9\n\13\r\13"+
		"\16\13\u00aa\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3"+
		"\16\3\17\3\17\3\20\3\20\3\21\3\21\7\21\u00c1\n\21\f\21\16\21\u00c4\13"+
		"\21\3\21\3\21\3\21\7\21\u00c9\n\21\f\21\16\21\u00cc\13\21\3\21\5\21\u00cf"+
		"\n\21\3\22\3\22\7\22\u00d3\n\22\f\22\16\22\u00d6\13\22\3\23\3\23\3\23"+
		"\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\26\3\26\5\26\u00e4\n\26\3\27\5\27"+
		"\u00e7\n\27\3\30\3\30\7\30\u00eb\n\30\f\30\16\30\u00ee\13\30\3\31\3\31"+
		"\3\31\3\31\5\31\u00f4\n\31\3\32\5\32\u00f7\n\32\3\33\3\33\3\33\7\33\u00fc"+
		"\n\33\f\33\16\33\u00ff\13\33\5\33\u0101\n\33\3\34\3\34\3\34\3\34\3\34"+
		"\3\35\3\35\3\35\3\35\5EYf\2\36\5\3\7\4\t\5\13\6\r\7\17\b\21\t\23\n\25"+
		"\2\27\13\31\f\33\r\35\16\37\17!\20#\21%\22\'\23)\2+\2-\2/\2\61\24\63\2"+
		"\65\2\67\29\25;\2\5\2\3\4\17\4\2\13\13\"\"\4\2((>>\4\2$$>>\4\2))>>\5\2"+
		"\13\f\17\17\"\"\5\2\62;CHch\3\2\62;\4\2/\60aa\5\2\u00b9\u00b9\u0302\u0371"+
		"\u2041\u2042\n\2<<C\\c|\u2072\u2191\u2c02\u2ff1\u3003\ud801\uf902\ufdd1"+
		"\ufdf2\uffff\4\2//aa\t\2C\\c|\u2072\u2191\u2c02\u2ff1\u3003\ud801\uf902"+
		"\ufdd1\ufdf2\uffff\3\2\63;\2\u0118\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2"+
		"\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25"+
		"\3\2\2\2\2\27\3\2\2\2\3\31\3\2\2\2\3\33\3\2\2\2\3\35\3\2\2\2\3\37\3\2"+
		"\2\2\3!\3\2\2\2\3#\3\2\2\2\3%\3\2\2\2\3\'\3\2\2\2\3\61\3\2\2\2\49\3\2"+
		"\2\2\4;\3\2\2\2\5=\3\2\2\2\7L\3\2\2\2\t`\3\2\2\2\13m\3\2\2\2\r\u0086\3"+
		"\2\2\2\17\u008d\3\2\2\2\21\u0091\3\2\2\2\23\u0095\3\2\2\2\25\u009f\3\2"+
		"\2\2\27\u00a8\3\2\2\2\31\u00ac\3\2\2\2\33\u00b0\3\2\2\2\35\u00b5\3\2\2"+
		"\2\37\u00ba\3\2\2\2!\u00bc\3\2\2\2#\u00ce\3\2\2\2%\u00d0\3\2\2\2\'\u00d7"+
		"\3\2\2\2)\u00db\3\2\2\2+\u00dd\3\2\2\2-\u00e3\3\2\2\2/\u00e6\3\2\2\2\61"+
		"\u00e8\3\2\2\2\63\u00f3\3\2\2\2\65\u00f6\3\2\2\2\67\u0100\3\2\2\29\u0102"+
		"\3\2\2\2;\u0107\3\2\2\2=>\7>\2\2>?\7#\2\2?@\7/\2\2@A\7/\2\2AE\3\2\2\2"+
		"BD\13\2\2\2CB\3\2\2\2DG\3\2\2\2EF\3\2\2\2EC\3\2\2\2FH\3\2\2\2GE\3\2\2"+
		"\2HI\7/\2\2IJ\7/\2\2JK\7@\2\2K\6\3\2\2\2LM\7>\2\2MN\7#\2\2NO\7]\2\2OP"+
		"\7E\2\2PQ\7F\2\2QR\7C\2\2RS\7V\2\2ST\7C\2\2TU\7]\2\2UY\3\2\2\2VX\13\2"+
		"\2\2WV\3\2\2\2X[\3\2\2\2YZ\3\2\2\2YW\3\2\2\2Z\\\3\2\2\2[Y\3\2\2\2\\]\7"+
		"_\2\2]^\7_\2\2^_\7@\2\2_\b\3\2\2\2`a\7>\2\2ab\7#\2\2bf\3\2\2\2ce\13\2"+
		"\2\2dc\3\2\2\2eh\3\2\2\2fg\3\2\2\2fd\3\2\2\2gi\3\2\2\2hf\3\2\2\2ij\7@"+
		"\2\2jk\3\2\2\2kl\b\4\2\2l\n\3\2\2\2mn\7(\2\2no\5\61\30\2op\7=\2\2p\f\3"+
		"\2\2\2qr\7(\2\2rs\7%\2\2su\3\2\2\2tv\5+\25\2ut\3\2\2\2vw\3\2\2\2wu\3\2"+
		"\2\2wx\3\2\2\2xy\3\2\2\2yz\7=\2\2z\u0087\3\2\2\2{|\7(\2\2|}\7%\2\2}~\7"+
		"z\2\2~\u0080\3\2\2\2\177\u0081\5)\24\2\u0080\177\3\2\2\2\u0081\u0082\3"+
		"\2\2\2\u0082\u0080\3\2\2\2\u0082\u0083\3\2\2\2\u0083\u0084\3\2\2\2\u0084"+
		"\u0085\7=\2\2\u0085\u0087\3\2\2\2\u0086q\3\2\2\2\u0086{\3\2\2\2\u0087"+
		"\16\3\2\2\2\u0088\u008e\t\2\2\2\u0089\u008b\7\17\2\2\u008a\u0089\3\2\2"+
		"\2\u008a\u008b\3\2\2\2\u008b\u008c\3\2\2\2\u008c\u008e\7\f\2\2\u008d\u0088"+
		"\3\2\2\2\u008d\u008a\3\2\2\2\u008e\u008f\3\2\2\2\u008f\u008d\3\2\2\2\u008f"+
		"\u0090\3\2\2\2\u0090\20\3\2\2\2\u0091\u0092\7>\2\2\u0092\u0093\3\2\2\2"+
		"\u0093\u0094\b\b\3\2\u0094\22\3\2\2\2\u0095\u0096\7>\2\2\u0096\u0097\7"+
		"A\2\2\u0097\u0098\7z\2\2\u0098\u0099\7o\2\2\u0099\u009a\7n\2\2\u009a\u009b"+
		"\3\2\2\2\u009b\u009c\5\'\23\2\u009c\u009d\3\2\2\2\u009d\u009e\b\t\3\2"+
		"\u009e\24\3\2\2\2\u009f\u00a0\7>\2\2\u00a0\u00a1\7A\2\2\u00a1\u00a2\3"+
		"\2\2\2\u00a2\u00a3\5\61\30\2\u00a3\u00a4\3\2\2\2\u00a4\u00a5\b\n\4\2\u00a5"+
		"\u00a6\b\n\5\2\u00a6\26\3\2\2\2\u00a7\u00a9\n\3\2\2\u00a8\u00a7\3\2\2"+
		"\2\u00a9\u00aa\3\2\2\2\u00aa\u00a8\3\2\2\2\u00aa\u00ab\3\2\2\2\u00ab\30"+
		"\3\2\2\2\u00ac\u00ad\7@\2\2\u00ad\u00ae\3\2\2\2\u00ae\u00af\b\f\6\2\u00af"+
		"\32\3\2\2\2\u00b0\u00b1\7A\2\2\u00b1\u00b2\7@\2\2\u00b2\u00b3\3\2\2\2"+
		"\u00b3\u00b4\b\r\6\2\u00b4\34\3\2\2\2\u00b5\u00b6\7\61\2\2\u00b6\u00b7"+
		"\7@\2\2\u00b7\u00b8\3\2\2\2\u00b8\u00b9\b\16\6\2\u00b9\36\3\2\2\2\u00ba"+
		"\u00bb\7\61\2\2\u00bb \3\2\2\2\u00bc\u00bd\7?\2\2\u00bd\"\3\2\2\2\u00be"+
		"\u00c2\7$\2\2\u00bf\u00c1\n\4\2\2\u00c0\u00bf\3\2\2\2\u00c1\u00c4\3\2"+
		"\2\2\u00c2\u00c0\3\2\2\2\u00c2\u00c3\3\2\2\2\u00c3\u00c5\3\2\2\2\u00c4"+
		"\u00c2\3\2\2\2\u00c5\u00cf\7$\2\2\u00c6\u00ca\7)\2\2\u00c7\u00c9\n\5\2"+
		"\2\u00c8\u00c7\3\2\2\2\u00c9\u00cc\3\2\2\2\u00ca\u00c8\3\2\2\2\u00ca\u00cb"+
		"\3\2\2\2\u00cb\u00cd\3\2\2\2\u00cc\u00ca\3\2\2\2\u00cd\u00cf\7)\2\2\u00ce"+
		"\u00be\3\2\2\2\u00ce\u00c6\3\2\2\2\u00cf$\3\2\2\2\u00d0\u00d4\5/\27\2"+
		"\u00d1\u00d3\5-\26\2\u00d2\u00d1\3\2\2\2\u00d3\u00d6\3\2\2\2\u00d4\u00d2"+
		"\3\2\2\2\u00d4\u00d5\3\2\2\2\u00d5&\3\2\2\2\u00d6\u00d4\3\2\2\2\u00d7"+
		"\u00d8\t\6\2\2\u00d8\u00d9\3\2\2\2\u00d9\u00da\b\23\2\2\u00da(\3\2\2\2"+
		"\u00db\u00dc\t\7\2\2\u00dc*\3\2\2\2\u00dd\u00de\t\b\2\2\u00de,\3\2\2\2"+
		"\u00df\u00e4\5/\27\2\u00e0\u00e4\t\t\2\2\u00e1\u00e4\5+\25\2\u00e2\u00e4"+
		"\t\n\2\2\u00e3\u00df\3\2\2\2\u00e3\u00e0\3\2\2\2\u00e3\u00e1\3\2\2\2\u00e3"+
		"\u00e2\3\2\2\2\u00e4.\3\2\2\2\u00e5\u00e7\t\13\2\2\u00e6\u00e5\3\2\2\2"+
		"\u00e7\60\3\2\2\2\u00e8\u00ec\5\65\32\2\u00e9\u00eb\5\63\31\2\u00ea\u00e9"+
		"\3\2\2\2\u00eb\u00ee\3\2\2\2\u00ec\u00ea\3\2\2\2\u00ec\u00ed\3\2\2\2\u00ed"+
		"\62\3\2\2\2\u00ee\u00ec\3\2\2\2\u00ef\u00f4\5\65\32\2\u00f0\u00f4\t\f"+
		"\2\2\u00f1\u00f4\5\67\33\2\u00f2\u00f4\t\n\2\2\u00f3\u00ef\3\2\2\2\u00f3"+
		"\u00f0\3\2\2\2\u00f3\u00f1\3\2\2\2\u00f3\u00f2\3\2\2\2\u00f4\64\3\2\2"+
		"\2\u00f5\u00f7\t\r\2\2\u00f6\u00f5\3\2\2\2\u00f7\66\3\2\2\2\u00f8\u0101"+
		"\7\62\2\2\u00f9\u00fd\t\16\2\2\u00fa\u00fc\t\b\2\2\u00fb\u00fa\3\2\2\2"+
		"\u00fc\u00ff\3\2\2\2\u00fd\u00fb\3\2\2\2\u00fd\u00fe\3\2\2\2\u00fe\u0101"+
		"\3\2\2\2\u00ff\u00fd\3\2\2\2\u0100\u00f8\3\2\2\2\u0100\u00f9\3\2\2\2\u0101"+
		"8\3\2\2\2\u0102\u0103\7A\2\2\u0103\u0104\7@\2\2\u0104\u0105\3\2\2\2\u0105"+
		"\u0106\b\34\6\2\u0106:\3\2\2\2\u0107\u0108\13\2\2\2\u0108\u0109\3\2\2"+
		"\2\u0109\u010a\b\35\4\2\u010a<\3\2\2\2\32\2\3\4EYfw\u0082\u0086\u008a"+
		"\u008d\u008f\u00aa\u00c2\u00ca\u00ce\u00d4\u00e3\u00e6\u00ec\u00f3\u00f6"+
		"\u00fd\u0100\7\b\2\2\7\3\2\5\2\2\7\4\2\6\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}