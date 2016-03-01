import sys
import regalloc
import json
import ply.lex as lex
from lexer import tokens,lexer
import ply.yacc as yacc
import sys
start = 'start'

#empty rule
def p_empty(p):
	'empty :'
	pass

def p_start(p):
	'''start : sourceElements
			| empty'''
	p[0]= ["start"] + [[p[i]] for i in range(1,len(p))]	

def p_sourceElements(p):
	'''sourceElements : sourceElement
					| sourceElements sourceElement '''
	p[0]= ["sourceElements"] + [[p[i]] for i in range(1,len(p))]			

def p_sourceElement(p):
	'''sourceElement : functionDeclaration
					| statement '''
	p[0]= ["sourceElement"] + [[p[i]] for i in range(1,len(p))]			

def p_functionDeclaration(p):
	'''functionDeclaration : FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN OPEN_BRACE functionBody CLOSE_BRACE
						| FUNCTION IDENTIFIER LPAREN RPAREN OPEN_BRACE functionBody CLOSE_BRACE '''

def p_formalParameterList(p):
	'''formalParameterList : IDENTIFIER 
							| formalParameterList COMMA IDENTIFIER'''

def p_functionBody(p):
	'''functionBody : sourceElements'''

def p_statement(p):
	'''statement : block
				| variableStatement
				| emptyStatement
				| expressionStatement
				| ifStatement
				| iterationStatement
				| continueStatement
				| breakStatement
				| returnStatement
				| withStatement
				| labelledStatement
				| switchStatement
				| throwStatement
				| tryStatement'''

def p_block(p):
	'''block : OPEN_BRACE statementList CLOSE_BRACE
			| OPEN_BRACE CLOSE_BRACE'''

def p_statementList(p):
	'''statementList : statement 
					| statementList statement'''

def p_variableStatement(p):
	'''variableStatement : VAR variableDeclarationList SEMI_COLON '''

def p_variableDeclarationList(p):
	'''variableDeclarationList : variableDeclaration 
								| variableDeclarationList COMMA variableDeclaration '''

def p_variableDeclaration(p):
	'''variableDeclaration : IDENTIFIER initialiser 
							| IDENTIFIER'''

def p_initialiser(p):
	'''initialiser : OP_ASSIGNMENT assignmentExpression'''

def p_assignmentExpression(p):
	'''assignmentExpression : conditionalExpression
							| leftHandSideExpression assignmentOperator assignmentExpression'''

def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression
							 | logicalOrExpression OP_TERNARY assignmentExpression COLON assignmentExpression '''


parser = yacc.yacc()
if __name__ == "__main__":
    file_input = sys.argv[1]
    program = open(file_input).read()
    parsed_code = parser.parse(program,lexer = lexer)
    print parsed_code
