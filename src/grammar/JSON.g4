
/** Taken from "The Definitive ANTLR 4 Reference" by Terence Parr */

// Derived from http://json.org

// Tweaked a bit for awkward π-nguin
grammar JSON;

json
   : value
   ;

obj
   : '{' pair (',' pair)* '}'
   | '{' '}'
   ;

pair
   : STRING ':' value
   | VARIABLE ':' value
   ;

arr
   : '[' value (',' value)* ']'
   | '[' ']'
   ;

value
   : VARIABLE
   | STRING
   | NUMBER
   | SPEC_CHAR 
   | obj
   | arr
   | 'true'
   | 'false'
   | 'null'
   ; // TODO: find out why SPEC_CHAR is here

SPEC_CHAR : ~('a'..'z' | 'A' .. 'Z' | '0' .. '9' | ':' | '.' | '-' | '>' | '<' | '/' | ' ' ) ;

VARIABLE : '?' IDENT ;

IDENT   : NameStartChar1 NameChar1* ; //[a-zA-Z_] [a-zA-Z0-9]*;

fragment
NameChar1    :   NameStartChar1
            |   '-' | '_' | INT
            |   '\u00B7'
            |   '\u0300'..'\u036F'
            |   '\u203F'..'\u2040'
            ;

fragment
NameStartChar1
            :   [a-zA-Z]
            |   '\u2070'..'\u218F'
            |   '\u2C00'..'\u2FEF'
            |   '\u3001'..'\uD7FF'
            |   '\uF900'..'\uFDCF'
            |   '\uFDF0'..'\uFFFD'
            ;


STRING
   : '"' (ESC1 | SAFECODEPOINT1)* '"'
   | '\'' (ESC2 | SAFECODEPOINT2)* '\''
   ;


fragment ESC1
   : '\\' (["\\/bfnrt] | UNICODE)
   ;

fragment ESC2
   : '\\' (['\\/bfnrt] | UNICODE)
   ;


fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;


fragment HEX
   : [0-9a-fA-F]
   ;


fragment SAFECODEPOINT1
   : ~ ["\\\u0000-\u001F]
   ;

fragment SAFECODEPOINT2
   : ~ ['\\\u0000-\u001F]
   ;


NUMBER
   : '-'? INT ('.' [0-9] +)? EXP?
   ;


fragment INT
   : '0' | [1-9] [0-9]*
   ;

// no leading zeros

fragment EXP
   : [Ee] [+\-]? INT
   ;

// \- since - means "range" inside [...]


SPACE
   : [ \r]+ -> skip
   ;