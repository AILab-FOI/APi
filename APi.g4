grammar APi ;

/* TODO: I am quite unhappy with the way the XML grammar
   is integrated into this grammar since there are a number
   of overlapping rules. It would be much better to rewrite
   parts of the XML grammar and integrate it better herein. */

import JSON, XMLParser ;

options { tokenVocab=XMLLexer; }


api_program : ( s_import | s_environment | s_channel | s_channel_transformer | s_agent | s_start | COMMENT | NEWLINE )*? ;

s_environment : ENVIRONMENT ':' NEWLINE ioflow+ ;

ioflow : IDENT FORMAT s_input ;

s_start : START pi_expr ;

pi_expr : '(' pi_expr ')'
	| pi_expr RESTART
	| pi_expr PARALLEL pi_expr
	| pi_expr ONSUCCESS pi_expr
	| pi_expr ONFAIL pi_expr
	| pi_expr pi_expr
	| IDENT ;

s_agent : AGENT IDENT ( arglist )? ':' NEWLINE flow+ ;

arglist : '(' IDENT IDENT* ')';

flow : TAB valid_channel SENDS valid_channel ( SENDS valid_channel )* NEWLINE ;

valid_channel : IDENT | SELF | NIL | STDIN | STDOUT | STDERR | VOID ;

s_channel : CHANNEL IDENT ':' NEWLINE s_channel_spec ;

s_channel_transformer : CHANNEL IDENT '.' NEWLINE ;

s_channel_spec : TAB s_input SENDS s_output NEWLINE;

s_import : IMPORT IDENT NEWLINE ;

s_input : s_json | s_xml | s_regex ;

s_output : s_json | s_xml ;

s_xml : XML xml ;

s_json : JSON json ;

s_regex : REGEX STRING ;

STDIN : 'stdin' ;

STDOUT : 'stdout' ;

STDERR : 'stderr' ;

VOID : 'void' ;

IMPORT : 'import' ;

ENVIRONMENT : 'environment' ;

ONSUCCESS : '&' ;

ONFAIL : '!' ;

RESTART : '+' ;

PARALLEL : '|' ;

START   : 'start' ;

SELF    : 'self' ;

AGENT   : 'agent' ;

CHANNEL : 'channel' ;

REGEX : 'regex' ;

JSON : 'json' ;

XML : 'xml' ;

FORMAT : '<->' ;

SENDS  : '->' ;

NIL     : '0' ;

COMMENT : COMMENT1 | COMMENT2 ;

COMMENT1: '//'~[\n]* ;

COMMENT2: '/*' .*? '*/' ;

//SPACE   : [ \r]+ -> skip ;

NEWLINE : [\n] ;

TAB : [\t] ;

