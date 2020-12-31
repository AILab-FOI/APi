grammar APi ;

import JSON ;

api_program : ( s_import | s_environment | s_channel | s_agent | s_start | COMMENT | NEWLINE )*? ;

s_environment : ENVIRONMENT ':' NEWLINE ioflow+ ;

ioflow : IDENT FORMAT json ;

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

s_channel : CHANNEL IDENT ':' NEWLINE s_channel_spec;

s_channel_spec : TAB json SENDS json NEWLINE;

s_import : IMPORT IDENT NEWLINE ;

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

FORMAT : '<->' ;

SENDS  : '->' ;

NIL     : '0' ;

COMMENT : COMMENT1 | COMMENT2 ;

COMMENT1: '//'~[\n]* ;

COMMENT2: '/*' .*? '*/' ;

//SPACE   : [ \r]+ -> skip ;

NEWLINE : [\n] ;

TAB : [\t] ;