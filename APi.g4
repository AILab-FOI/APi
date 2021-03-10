grammar APi ;


/* NOTE: Make sure that TODO's below are reflected in APi.py's syntax
   	 walker (i.e. when processing command input).*/

/* TODO:
   I am quite unhappy with the way the XML and JSON grammars
   are integrated into this grammar since there are a number
   of overlapping rules. It might be a better solution to
   just use strings, and leave the parsing to the actual
   implementation (with swipl for example). */

import JSON, XMLParser ;

options { tokenVocab=XMLLexer; }


api_program : ( s_import | s_environment | s_channel | s_channel_transformer | s_agent | s_start | COMMENT | NEWLINE )*? ;

s_environment : ENVIRONMENT ':' NEWLINE ( iflow | oflow )+ ;

iflow : TAB IDENT INPUT_FORMAT s_input NEWLINE ;

oflow : TAB IDENT OUTPUT_FORMAT s_output NEWLINE ;

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

/* TODO: Implement remote holon import (e.g. from another server like
   	 holon1@bla.foi.hr). The import statement needs to be changed
	 to something like: from holon1 import output1 as h1out
	 or from holon2@rec.foi.hr import * (similar to Python
	 syntax), since if a holon has multiple inputs or outputs
	 we need a way to differentiate between them. Also to avoid
	 possible nameclashes we should use "as" as a way to rename
	 the symbols for local use. */

s_import : IMPORT IDENT NEWLINE ;


/* TODO: Nice to have feature would be to be able to load
         a JSON or XML template from a file, instead of
	 writing it into the production rule, i.e. something
	 like:
		json load "template1.json" > xml load "template1.xml" */


/* TODO: Implement transparent channels, e.g. channels that do
   	 not process input to output but only forward what they
	 get. Example:
	      channel x.
	 (no input -> output specification)*/

/* TODO: implement string output with variable placeholders so
   	 that any string can be used as output. Example:

	      json { 'x':?var } -> string "the value of var is ?var"*/

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

INPUT_FORMAT : '=>' ;

OUTPUT_FORMAT : '<=' ;

SENDS  : '->' ;

NIL     : '0' ;

COMMENT : COMMENT1 | COMMENT2 ;

COMMENT1: '//'~[\n]* ;

COMMENT2: '/*' .*? '*/' ;

//SPACE   : [ \r]+ -> skip ;

NEWLINE : [\n] ;

TAB : [\t] ;

