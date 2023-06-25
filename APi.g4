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


api_program : ( s_import | s_environment | s_environment_forward | s_channel | s_channel_forward | s_agent | s_start | COMMENT | NEWLINE )*? ;

s_environment : ENVIRONMENT WS ':' NEWLINE ( iflow | oflow )+ ;

s_environment_forward : ENVIRONMENT WS '.' NEWLINE ;

iflow : TAB INPUT WS C_SENDS WS s_input NEWLINE ;

oflow : TAB OUTPUT WS E_SENDS WS s_output NEWLINE ;

s_start : START WS pi_expr ;

pi_expr : '(' pi_expr ')'
	| pi_expr RESTART
	| pi_expr WS PARALLEL WS pi_expr
	| pi_expr WS ONSUCCESS WS pi_expr
	| pi_expr WS ONFAIL WS pi_expr
	| pi_expr WS pi_expr
	| IDENT ( arglist )?;

s_agent : AGENT WS IDENT ( arglist WS )? ':' NEWLINE aflow+ ;

arglist : '(' IDENT (WS IDENT)* ')';

aflow : TAB valid_channel WS A_SENDS WS valid_channel NEWLINE ;

valid_channel : IDENT | SELF | STDIN | STDOUT | STDERR | VOID ;

s_channel : CHANNEL WS IDENT WS ':' NEWLINE s_channel_spec ;

s_channel_forward : CHANNEL WS IDENT WS '.' NEWLINE ;

s_channel_spec : TAB s_input WS C_SENDS WS s_output NEWLINE;

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

s_xml : XML '(' xml ')';

s_json : JSON '(' json ')';

s_regex : REGEX '(' STRING ')';

INPUT : 'input' ;

OUTPUT : 'output' ;

STDOUT : 'STDOUT' ;

STDERR : 'STDERR' ;

STDIN : 'STDIN' ;

VOID : 'VOID' ;

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

A_SENDS  : '->' ;

C_SENDS : TCP | UDP ;

E_SENDS : TCP_BW | UDP_BW ;

TCP : '-->' ;

UDP : '*->' ;

TCP_BW : '<--' ;

UDP_BW : '<-*' ;

COMMENT : COMMENT1 | COMMENT2 ;

COMMENT1: '//'~[\n]* ;

COMMENT2: '/*' .*? '*/' ;

WS : [ \f\r] ;

NEWLINE : [\n] ;

TAB : [\t] ;