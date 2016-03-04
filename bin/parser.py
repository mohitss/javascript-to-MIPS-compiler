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
	p[0]= ["start"] + [p[i] for i in range(1,len(p))]

def p_sourceElements(p):
	'''sourceElements : sourceElement
					| sourceElements sourceElement '''
	p[0]= ["sourceElements"] + [p[i] for i in range(1,len(p))]

def p_sourceElement(p):
	'''sourceElement : functionDeclaration
						| statement'''
	p[0]= ["sourceElement"] + [p[i] for i in range(1,len(p))]

def p_functionDeclaration(p):
	'''functionDeclaration : FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN functionBody
						| FUNCTION IDENTIFIER LPAREN RPAREN functionBody '''
	p[0]= ["functionDeclaration"] + [p[i] for i in range(1,len(p))]




def p_formalParameterList(p):
	'''formalParameterList : IDENTIFIER
							| formalParameterList COMMA IDENTIFIER'''
	p[0]= ["formalParameterList"] + [p[i] for i in range(1,len(p))]


def p_functionBody(p):
	'''functionBody : OPEN_BRACE sourceElements CLOSE_BRACE
					| OPEN_BRACE CLOSE_BRACE '''
	p[0]= ["functionBody"] + [p[i] for i in range(1,len(p))]


def p_statement(p):
	'''statement : block
				| emptyStatement
				| variableStatement
				| continueStatement
				| breakStatement
				| returnStatement
				| withStatement
				| labelledStatement
				| switchStatement
				| throwStatement
				| tryStatement
				| ifStatement
				| expressionStatement
				| iterationStatement'''
	p[0]= ["statement"] + [p[i] for i in range(1,len(p))]

def p_statementNoIf(p):
	'''statementNoIf : block
				| emptyStatement
				| variableStatement
				| continueStatement
				| breakStatement
				| returnStatement
				| withStatementNoIf
				| labelledStatementNoIf
				| switchStatement
				| throwStatement
				| tryStatement
				| ifStatementNoIf
				| expressionStatement
				| iterationStatementNoIf'''
	p[0]= ["statementNoIf"] + [p[i] for i in range(1,len(p))]


def p_continueStatement(p):
	'''continueStatement : CONTINUE SEMI_COLON
						| CONTINUE IDENTIFIER SEMI_COLON'''
	p[0]= ["continueStatement"] + [p[i] for i in range(1,len(p))]


def p_breakStatement(p):
	'''breakStatement :  BREAK SEMI_COLON
						| BREAK IDENTIFIER SEMI_COLON'''
	p[0]= ["breakStatement"] + [p[i] for i in range(1,len(p))]


def p_returnStatement(p):
	'''returnStatement :  RETURN SEMI_COLON
						| RETURN expression SEMI_COLON'''
	p[0]= ["returnStatement"] + [p[i] for i in range(1,len(p))]


def p_withStatement(p):
	'''withStatement : WITH LPAREN expression RPAREN statement'''
	p[0]= ["withStatement"] + [p[i] for i in range(1,len(p))]


def p_withStatementNoIf(p):
	'''withStatementNoIf : WITH LPAREN expression RPAREN statementNoIf'''
	p[0]= ["withStatementNoIf"] + [p[i] for i in range(1,len(p))]


def p_switchStatement(p):
	'''switchStatement : SWITCH LPAREN expression RPAREN caseBlock'''
	p[0]= ["switchStatement"] + [p[i] for i in range(1,len(p))]


def p_caseBlock(p):
	'''caseBlock : OPEN_BRACE CLOSE_BRACE
					| OPEN_BRACE caseClauses CLOSE_BRACE
					| OPEN_BRACE defaultClause CLOSE_BRACE
					| OPEN_BRACE defaultClause caseClauses CLOSE_BRACE
					| OPEN_BRACE caseClauses defaultClause caseClauses CLOSE_BRACE
					| OPEN_BRACE caseClauses defaultClause CLOSE_BRACE'''
	p[0]= ["caseBlock"] + [p[i] for i in range(1,len(p))]


def p_defaultClause(p):
	'''defaultClause : DEFAULT COLON
					| DEFAULT COLON statementList'''
	p[0]= ["defaultClause"] + [p[i] for i in range(1,len(p))]


def p_caseClauses(p):
	'''caseClauses : caseClause
					| caseClause caseClauses'''
	p[0]= ["caseClauses"] + [p[i] for i in range(1,len(p))]


def p_caseClause(p):
	'''caseClause : CASE expression COLON
					| CASE expression COLON statementList'''
	p[0]= ["caseClause"] + [p[i] for i in range(1,len(p))]



def p_labelledStatement(p):
	'''labelledStatement : IDENTIFIER COLON statement'''
	p[0]= ["labelledStatement"] + [p[i] for i in range(1,len(p))]


def p_labelledStatementNoIf(p):
	'''labelledStatementNoIf : IDENTIFIER COLON statementNoIf'''
	p[0]= ["labelledStatementNoIf"] + [p[i] for i in range(1,len(p))]


def p_throwStatement(p):
	'''throwStatement : THROW expression SEMI_COLON'''
	p[0]= ["throwStatement"] + [p[i] for i in range(1,len(p))]


def p_tryStatement(p):
	'''tryStatement : TRY block finally
					| TRY block catch
					| TRY block catch finally'''
	p[0]= ["tryStatement"] + [p[i] for i in range(1,len(p))]


def p_catch(p):
	'''catch : CATCH LPAREN IDENTIFIER RPAREN block'''
	p[0]= ["catch"] + [p[i] for i in range(1,len(p))]


def p_finally(p):
	'''finally : FINALLY block'''
	p[0]= ["finally"] + [p[i] for i in range(1,len(p))]


def p_emptyStatement(p):
	'''emptyStatement : SEMI_COLON '''
	p[0]= ["emptyStatement"] + [p[i] for i in range(1,len(p))]


def p_expressionStatement(p):
	'''expressionStatement : expressionWithoutFunc SEMI_COLON'''
	p[0]= ["expressionStatement"] + [p[i] for i in range(1,len(p))]


def p_ifStatement(p):
	'''ifStatement : IF LPAREN expression RPAREN statement
					| IF LPAREN expression RPAREN statementNoIf ELSE statement'''
	p[0]= ["ifStatement"] + [p[i] for i in range(1,len(p))]


def p_ifStatementNoIf(p):
	'''ifStatementNoIf : IF LPAREN expression RPAREN statementNoIf ELSE statementNoIf'''
	p[0]= ["ifStatementNoIf"] + [p[i] for i in range(1,len(p))]


def p_iterationStatement(p):
	'''iterationStatement :  DO statement WHILE LPAREN expression RPAREN SEMI_COLON
							| WHILE LPAREN expression RPAREN statement
							| FOR LPAREN SEMI_COLON SEMI_COLON RPAREN statement
							| FOR LPAREN SEMI_COLON SEMI_COLON expression RPAREN statement
							| FOR LPAREN SEMI_COLON expression SEMI_COLON RPAREN statement
							| FOR LPAREN SEMI_COLON expression SEMI_COLON expression RPAREN statement
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON SEMI_COLON RPAREN statement
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON SEMI_COLON expression RPAREN statement
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON expression SEMI_COLON RPAREN statement
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON expression SEMI_COLON expression RPAREN statement
							| FOR LPAREN leftHandSideExpression IN expression RPAREN statement
							| FOR LPAREN expressionNoIn SEMI_COLON SEMI_COLON RPAREN statement
							| FOR LPAREN expressionNoIn SEMI_COLON SEMI_COLON expression RPAREN statement
							| FOR LPAREN expressionNoIn SEMI_COLON expression SEMI_COLON RPAREN statement
							| FOR LPAREN expressionNoIn SEMI_COLON expression SEMI_COLON expression RPAREN statement
							| FOR LPAREN VAR variableDeclarationNoIn IN expression RPAREN statement'''
	p[0]= ["iterationStatement"] + [p[i] for i in range(1,len(p))]


def p_iterationStatementNoIf(p):
	'''iterationStatementNoIf :  DO statement WHILE LPAREN expression RPAREN SEMI_COLON
							| WHILE LPAREN expression RPAREN statementNoIf
							| FOR LPAREN SEMI_COLON SEMI_COLON RPAREN statementNoIf
							| FOR LPAREN SEMI_COLON SEMI_COLON expression RPAREN statementNoIf
							| FOR LPAREN SEMI_COLON expression SEMI_COLON RPAREN statementNoIf
							| FOR LPAREN SEMI_COLON expression SEMI_COLON expression RPAREN statementNoIf
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON SEMI_COLON RPAREN statementNoIf
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON SEMI_COLON expression RPAREN statementNoIf
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON expression SEMI_COLON RPAREN statementNoIf
							| FOR LPAREN VAR variableDeclarationListNoIn SEMI_COLON expression SEMI_COLON expression RPAREN statementNoIf
							| FOR LPAREN leftHandSideExpression IN expression RPAREN statementNoIf
							| FOR LPAREN expressionNoIn SEMI_COLON SEMI_COLON RPAREN statementNoIf
							| FOR LPAREN expressionNoIn SEMI_COLON SEMI_COLON expression RPAREN statementNoIf
							| FOR LPAREN expressionNoIn SEMI_COLON expression SEMI_COLON RPAREN statementNoIf
							| FOR LPAREN expressionNoIn SEMI_COLON expression SEMI_COLON expression RPAREN statementNoIf
							| FOR LPAREN VAR variableDeclarationNoIn IN expression RPAREN statementNoIf'''
	p[0]= ["iterationStatementNoIf"] + [p[i] for i in range(1,len(p))]


def p_block(p):
	'''block : OPEN_BRACE statementList CLOSE_BRACE
			| OPEN_BRACE CLOSE_BRACE'''
	p[0]= ["block"] + [p[i] for i in range(1,len(p))]


def p_statementList(p):
	'''statementList : statement
					| statementList statement'''
	p[0]= ["statementList"] + [p[i] for i in range(1,len(p))]


def p_variableStatement(p):
	'''variableStatement : VAR variableDeclarationList SEMI_COLON '''
	p[0]= ["variableStatement"] + [p[i] for i in range(1,len(p))]


def p_variableDeclarationList(p):
	'''variableDeclarationList : variableDeclaration
								| variableDeclarationList COMMA variableDeclaration '''
	p[0]= ["variableDeclarationList"] + [p[i] for i in range(1,len(p))]


def p_variableDeclarationListNoIn(p):
	'''variableDeclarationListNoIn : variableDeclarationNoIn
								| variableDeclarationListNoIn COMMA variableDeclarationNoIn '''
	p[0]= ["variableDeclarationListNoIn"] + [p[i] for i in range(1,len(p))]


def p_variableDeclaration(p):
	'''variableDeclaration : IDENTIFIER initialiser
							| IDENTIFIER'''
	p[0]= ["variableDeclaration"] + [p[i] for i in range(1,len(p))]


def p_variableDeclarationNoIn(p):
	'''variableDeclarationNoIn : IDENTIFIER initialiserNoIn
							| IDENTIFIER'''
	p[0]= ["variableDeclarationNoIn"] + [p[i] for i in range(1,len(p))]



def p_initialiser(p):
	'''initialiser : OP_ASSIGNMENT assignmentExpression'''
	p[0]= ["initialiser"] + [p[i] for i in range(1,len(p))]



def p_initialiserNoIn(p):
	'''initialiserNoIn : OP_ASSIGNMENT assignmentExpressionNoIn'''
	p[0]= ["initialiserNoIn"] + [p[i] for i in range(1,len(p))]



def p_assignmentExpressionWithoutFunc(p):
	'''assignmentExpressionWithoutFunc : conditionalExpressionWithoutFunc
							| leftHandSideExpressionWithoutFunc assignmentOperator assignmentExpression'''
	p[0]= ["assignmentExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_assignmentExpression(p):
	'''assignmentExpression : conditionalExpression
							| leftHandSideExpression assignmentOperator assignmentExpression'''
	p[0]= ["assignmentExpression"] + [p[i] for i in range(1,len(p))]


def p_assignmentExpressionNoIn(p):
	'''assignmentExpressionNoIn : conditionalExpressionNoIn
							| leftHandSideExpression assignmentOperator assignmentExpressionNoIn'''
	p[0]= ["assignmentExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_assignmentOperator(p):
	'''assignmentOperator : OP_ASSIGNMENT
							| OP_PLUSEQUAL
							| OP_MINUSEQUAL
							| OP_MULTEQUAL
							| OP_DIVEQUAL
							| OP_MODEQUAL'''
	p[0]= ["assignmentOperator"] + [p[i] for i in range(1,len(p))]


def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression
							 | logicalOrExpression OP_TERNARY assignmentExpression COLON assignmentExpression '''
	p[0]= ["conditionalExpression"] + [p[i] for i in range(1,len(p))]


def p_conditionalExpressionWithoutFunc(p):
	'''conditionalExpressionWithoutFunc : logicalOrExpressionWithoutFunc
							 | logicalOrExpressionWithoutFunc OP_TERNARY assignmentExpression COLON assignmentExpression '''
	p[0]= ["conditionalExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]



def p_conditionalExpressionNoIn(p):
	'''conditionalExpressionNoIn : logicalOrExpressionNoIn
							 | logicalOrExpressionNoIn OP_TERNARY assignmentExpressionNoIn COLON assignmentExpressionNoIn '''
	p[0]= ["conditionalExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_logicalOrExpressionWithoutFunc(p):
	'''logicalOrExpressionWithoutFunc : logicalAndExpressionWithoutFunc
							| logicalAndExpressionWithoutFunc tempLogicalOrExpression'''
	p[0]= ["logicalOrExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_logicalOrExpression(p):
	'''logicalOrExpression : logicalAndExpression
							| logicalAndExpression tempLogicalOrExpression'''
	p[0]= ["logicalOrExpression"] + [p[i] for i in range(1,len(p))]


def p_logicalOrExpressionNoIn(p):
	'''logicalOrExpressionNoIn : logicalAndExpressionNoIn
							| logicalAndExpressionNoIn tempLogicalOrExpressionNoIn'''
	p[0]= ["logicalOrExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_tempLogicalOrExpression(p):
	'''tempLogicalOrExpression : logicalOrOperator logicalAndExpression
								| logicalOrOperator logicalAndExpression tempLogicalOrExpression'''
	p[0]= ["tempLogicalOrExpression"] + [p[i] for i in range(1,len(p))]


def p_tempLogicalOrExpressionNoIn(p):
	'''tempLogicalOrExpressionNoIn : logicalOrOperator logicalAndExpressionNoIn
								| logicalOrOperator logicalAndExpressionNoIn tempLogicalOrExpressionNoIn'''
	p[0]= ["tempLogicalOrExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_logicalOrOperator(p):
	'''logicalOrOperator : OP_OR '''
	p[0]= ["logicalOrOperator"] + [p[i] for i in range(1,len(p))]

def p_logicalAndExpression(p):
	'''logicalAndExpression : bitWiseOrExpression
	 						| bitWiseOrExpression tempLogicalAndExpression'''
	p[0]= ["logicalAndExpression"] + [p[i] for i in range(1,len(p))]


def p_logicalAndExpressionWithoutFunc(p):
	'''logicalAndExpressionWithoutFunc : bitWiseOrExpressionWithoutFunc
	 						| bitWiseOrExpressionWithoutFunc tempLogicalAndExpression'''
	p[0]= ["logicalAndExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempLogicalAndExpression(p):
	'''tempLogicalAndExpression : logicalAndOperator bitWiseOrExpression
								| logicalAndOperator bitWiseOrExpression tempLogicalAndExpression'''
	p[0]= ["tempLogicalAndExpression"] + [p[i] for i in range(1,len(p))]


def p_logicalAndExpressionNoIn(p):
	'''logicalAndExpressionNoIn : bitWiseOrExpressionNoIn
							| bitWiseOrExpressionNoIn tempLogicalAndExpressionNoIn'''
	p[0]= ["logicalAndExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_tempLogicalAndExpressionNoIn(p):
	'''tempLogicalAndExpressionNoIn : logicalAndOperator bitWiseOrExpressionNoIn
								| logicalAndOperator bitWiseOrExpressionNoIn tempLogicalAndExpressionNoIn'''
	p[0]= ["tempLogicalAndExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_logicalAndOperator(p):
	'''logicalAndOperator : OP_AND'''
	p[0]= ["logicalAndOperator"] + [p[i] for i in range(1,len(p))]


def p_bitWiseOrExpression(p):
	'''bitWiseOrExpression : bitWiseXorExpression
 							| bitWiseXorExpression tempBitWiseOrExpression'''
	p[0]= ["bitWiseOrExpression"] + [p[i] for i in range(1,len(p))]


def p_bitWiseOrExpressionWithoutFunc(p):
	'''bitWiseOrExpressionWithoutFunc : bitWiseXorExpressionWithoutFunc
 							| bitWiseXorExpressionWithoutFunc tempBitWiseOrExpression'''
	p[0]= ["bitWiseOrExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempBitWiseOrExpression(p):
	'''tempBitWiseOrExpression : bitWiseOrOperator bitWiseXorExpression
								| bitWiseOrOperator bitWiseXorExpression tempBitWiseOrExpression'''
	p[0]= ["tempBitWiseOrExpression"] + [p[i] for i in range(1,len(p))]


def p_bitWiseOrExpressionNoIn(p):
	'''bitWiseOrExpressionNoIn : bitWiseXorExpressionNoIn
							| bitWiseXorExpressionNoIn tempBitWiseOrExpressionNoIn'''
	p[0]= ["bitWiseOrExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_tempBitWiseOrExpressionNoIn(p):
	'''tempBitWiseOrExpressionNoIn : bitWiseOrOperator bitWiseXorExpressionNoIn
								| bitWiseOrOperator bitWiseXorExpressionNoIn tempBitWiseOrExpressionNoIn'''
	p[0]= ["tempBitWiseOrExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_bitWiseOrOperator(p):
	'''bitWiseOrOperator : BITWISE_OR'''
	p[0]= ["bitWiseOrOperator"] + [p[i] for i in range(1,len(p))]


def p_bitWiseXorExpression(p):
	'''bitWiseXorExpression : bitWiseAndExpression
							| bitWiseAndExpression tempBitWiseXorExpression'''
	p[0]= ["bitWiseXorExpression"] + [p[i] for i in range(1,len(p))]


def p_bitWiseXorExpressionWithoutFunc(p):
	'''bitWiseXorExpressionWithoutFunc : bitWiseAndExpressionWithoutFunc
							| bitWiseAndExpressionWithoutFunc tempBitWiseXorExpression'''
	p[0]= ["bitWiseXorExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempBitWiseXorExpression(p):
	'''tempBitWiseXorExpression : bitWiseXorOperator bitWiseAndExpression
								| bitWiseXorOperator bitWiseAndExpression tempBitWiseXorExpression'''
	p[0]= ["tempBitWiseXorExpression"] + [p[i] for i in range(1,len(p))]


def p_bitWiseXorExpressionNoIn(p):
	'''bitWiseXorExpressionNoIn : bitWiseAndExpressionNoIn
							| bitWiseAndExpressionNoIn tempBitWiseXorExpressionNoIn'''
	p[0]= ["bitWiseXorExpressionNoIn"] + [p[i] for i in range(1,len(p))]



def p_tempBitWiseXorExpressionNoIn(p):
	'''tempBitWiseXorExpressionNoIn : bitWiseXorOperator bitWiseAndExpressionNoIn
								| bitWiseXorOperator bitWiseAndExpressionNoIn tempBitWiseXorExpressionNoIn'''
	p[0]= ["tempBitWiseXorExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_bitWiseXorOperator(p):
	'''bitWiseXorOperator : BITWISE_XOR'''
	p[0]= ["bitWiseXorOperator"] + [p[i] for i in range(1,len(p))]


def p_bitWiseAndExpression(p):
	'''bitWiseAndExpression : equalityExpression
							| equalityExpression tempBitWiseAndExpression'''
	p[0]= ["bitWiseAndExpression"] + [p[i] for i in range(1,len(p))]


def p_bitWiseAndExpressionWithoutFunc(p):
	'''bitWiseAndExpressionWithoutFunc : equalityExpressionWithoutFunc
							| equalityExpressionWithoutFunc tempBitWiseAndExpression'''
	p[0]= ["bitWiseAndExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempBitWiseAndExpression(p):
	'''tempBitWiseAndExpression : bitWiseAndOperator equalityExpression
								| bitWiseAndOperator equalityExpression tempBitWiseAndExpression'''
	p[0]= ["tempBitWiseAndExpression"] + [p[i] for i in range(1,len(p))]


def p_bitWiseAndExpressionNoIn(p):
	'''bitWiseAndExpressionNoIn : equalityExpressionNoIn
							| equalityExpressionNoIn tempBitWiseAndExpressionNoIn'''
	p[0]= ["bitWiseAndExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_tempBitWiseAndExpressionNoIn(p):
	'''tempBitWiseAndExpressionNoIn : bitWiseAndOperator equalityExpressionNoIn
								| bitWiseAndOperator equalityExpressionNoIn tempBitWiseAndExpressionNoIn'''
	p[0]= ["tempBitWiseAndExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_bitWiseAndOperator(p):
	'''bitWiseAndOperator : BITWISE_AND'''
	p[0]= ["bitWiseAndOperator"] + [p[i] for i in range(1,len(p))]


def p_equalityExpression(p):
	'''equalityExpression : relationalExpression
							 | relationalExpression tempEqualityExpression'''
	p[0]= ["equalityExpression"] + [p[i] for i in range(1,len(p))]


def p_equalityExpressionWithoutFunc(p):
	'''equalityExpressionWithoutFunc : relationalExpressionWithoutFunc
							 | relationalExpressionWithoutFunc tempEqualityExpression'''
	p[0]= ["equalityExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempEqualityExpression(p):
	'''tempEqualityExpression : equalityOperator relationalExpression
								| equalityOperator relationalExpression tempEqualityExpression'''
	p[0]= ["tempEqualityExpression"] + [p[i] for i in range(1,len(p))]


def p_equalityExpressionNoIn(p):
	'''equalityExpressionNoIn : relationalExpressionNoIn
							| equalityExpressionNoIn OP_EQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_UNIVEQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_NOTEQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_NOTUNIVEQUAL relationalExpressionNoIn'''
	p[0]= ["equalityExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_equalityOperator(p):
	'''equalityOperator : OP_EQUAL
						| OP_UNIVEQUAL
						| OP_NOTEQUAL
						| OP_NOTUNIVEQUAL'''
	p[0]= ["equalityOperator"] + [p[i] for i in range(1,len(p))]


def p_relationalExpression(p):
	'''relationalExpression :  shiftExpression
							| relationalExpression OP_GREATER shiftExpression
							| relationalExpression OP_LESS shiftExpression
							| relationalExpression OP_GREATEREQUAL shiftExpression
							| relationalExpression OP_LESSEQUAL shiftExpression
							| relationalExpression INSTANCEOF shiftExpression
							| relationalExpression IN shiftExpression'''
	p[0]= ["relationalExpression"] + [p[i] for i in range(1,len(p))]


def p_relationalExpressionWithoutFunc(p):
	'''relationalExpressionWithoutFunc :  shiftExpressionWithoutFunc
							| relationalExpressionWithoutFunc OP_GREATER shiftExpression
							| relationalExpressionWithoutFunc OP_LESS shiftExpression
							| relationalExpressionWithoutFunc OP_GREATEREQUAL shiftExpression
							| relationalExpressionWithoutFunc OP_LESSEQUAL shiftExpression
							| relationalExpressionWithoutFunc INSTANCEOF shiftExpression
							| relationalExpressionWithoutFunc IN shiftExpression'''
	p[0]= ["relationalExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]

# def p_tempRelationalExpression(p):
# 	'''tempRelationalExpression : relationalOperator shiftExpression
# 								| relationalOperator shiftExpression tempRelationalExpression'''



# def p_relationalOperator(p):
# 	'''relationalOperator : OP_GREATER
# 							| OP_LESS
# 							| OP_GREATEREQUAL
# 							| OP_LESSEQUAL
# 							| INSTANCEOF
# 							| IN'''



def p_relationalExpressionNoIn(p):
	'''relationalExpressionNoIn : shiftExpression
							| relationalExpressionNoIn OP_GREATER shiftExpression
							| relationalExpressionNoIn OP_LESS shiftExpression
							| relationalExpressionNoIn OP_GREATEREQUAL shiftExpression
							| relationalExpressionNoIn OP_LESSEQUAL shiftExpression
							| relationalExpressionNoIn INSTANCEOF shiftExpression'''
	p[0]= ["relationalExpressionNoIn"] + [p[i] for i in range(1,len(p))]


def p_shiftExpression(p):
	'''shiftExpression : additiveExpression
						| additiveExpression tempShiftExpression'''
	p[0]= ["shiftExpression"] + [p[i] for i in range(1,len(p))]


def p_shiftExpressionWithoutFunc(p):
	'''shiftExpressionWithoutFunc : additiveExpressionWithoutFunc
						| additiveExpressionWithoutFunc tempShiftExpression'''
	p[0]= ["shiftExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempShiftExpression(p):
	'''tempShiftExpression : shiftOperator additiveExpression
							| shiftOperator additiveExpression tempShiftExpression'''
	p[0]= ["tempShiftExpression"] + [p[i] for i in range(1,len(p))]



def p_shiftOperator(p):
	'''shiftOperator : OP_LSHIFT
					| OP_RSHIFT'''
	p[0]= ["shiftOperator"] + [p[i] for i in range(1,len(p))]


def p_additiveExpression(p):
	'''additiveExpression  : multiplicativeExpression
 							| multiplicativeExpression tempAdditiveExpression'''
	p[0]= ["additiveExpression"] + [p[i] for i in range(1,len(p))]


def p_additiveExpressionWithoutFunc(p):
	'''additiveExpressionWithoutFunc  : multiplicativeExpressionWithoutFunc
 							| multiplicativeExpressionWithoutFunc tempAdditiveExpression'''
	p[0]= ["additiveExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_tempAdditiveExpression(p):
	'''tempAdditiveExpression : additiveOperator multiplicativeExpression
								| additiveOperator multiplicativeExpression tempAdditiveExpression'''
	p[0]= ["tempAdditiveExpression"] + [p[i] for i in range(1,len(p))]


def p_multiplicativeExpressionWithoutFunc(p):
	'''multiplicativeExpressionWithoutFunc : unaryExpressionWithoutFunc
								| unaryExpressionWithoutFunc tempMultiplicativeExpression'''
	p[0]= ["multiplicativeExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_multiplicativeExpression(p):
	'''multiplicativeExpression : unaryExpression
	 							| unaryExpression tempMultiplicativeExpression'''
	p[0]= ["multiplicativeExpression"] + [p[i] for i in range(1,len(p))]


def p_tempMultiplicativeExpression(p):
	'''tempMultiplicativeExpression : multiplicativeOperator unaryExpression
									| multiplicativeOperator unaryExpression tempMultiplicativeExpression'''
	p[0]= ["tempMultiplicativeExpression"] + [p[i] for i in range(1,len(p))]


def p_multiplicativeOperator(p):
	'''multiplicativeOperator : OP_MULT
								| OP_MODULUS
								| OP_DIVIDE'''
	p[0]= ["multiplicativeOperator"] + [p[i] for i in range(1,len(p))]


def p_additiveOperator(p):
	'''additiveOperator : OP_PLUS
						| OP_MINUS '''
	p[0]= ["additiveOperator"] + [p[i] for i in range(1,len(p))]

def p_unaryExpression(p):
	'''unaryExpression : postFixExpression
					| DELETE unaryExpression
					| VOID unaryExpression
					| TYPEOF unaryExpression
					| OP_INCREMENT unaryExpression
					| OP_DECREMENT unaryExpression
					| OP_PLUS unaryExpression
					| OP_MINUS unaryExpression
					| BITWISE_NOT unaryExpression
					| OP_NOT unaryExpression'''
	p[0]= ["unaryExpression"] + [p[i] for i in range(1,len(p))]


def p_unaryExpressionWithoutFunc(p):
	'''unaryExpressionWithoutFunc : postFixExpressionWithoutFunc
					| DELETE unaryExpression
					| VOID unaryExpression
					| TYPEOF unaryExpression
					| OP_INCREMENT unaryExpression
					| OP_DECREMENT unaryExpression
					| OP_PLUS unaryExpression
					| OP_MINUS unaryExpression
					| BITWISE_NOT unaryExpression
					| OP_NOT unaryExpression'''
	p[0]= ["unaryExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_postFixExpression(p):
	'''postFixExpression :  leftHandSideExpression
							| leftHandSideExpression OP_INCREMENT
							| leftHandSideExpression OP_DECREMENT'''
	p[0]= ["postFixExpression"] + [p[i] for i in range(1,len(p))]


def p_postFixExpressionWithoutFunc(p):
	'''postFixExpressionWithoutFunc :  leftHandSideExpressionWithoutFunc
							| leftHandSideExpressionWithoutFunc OP_INCREMENT
							| leftHandSideExpressionWithoutFunc OP_DECREMENT'''
	p[0]= ["postFixExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]



def p_leftHandSideExpression(p):
	'''leftHandSideExpression : newExpression
								| callExpression'''
	p[0]= ["leftHandSideExpression"] + [p[i] for i in range(1,len(p))]

def p_leftHandSideExpressionWithoutFunc(p):
	'''leftHandSideExpressionWithoutFunc : newExpressionWithoutFunc
								| callExpressionWithoutFunc'''
	p[0]= ["leftHandSideExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]

def p_newExpression(p):
	'''newExpression : memberExpression
						| NEW newExpression'''
	p[0]= ["newExpression"] + [p[i] for i in range(1,len(p))]

def p_newExpressionWithoutFunc(p):
	'''newExpressionWithoutFunc : memberExpressionWithoutFunc
						| NEW newExpression'''
	p[0]= ["newExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]

def p_memberExpression(p):
	'''memberExpression : functionExpression
							| primaryExpression
							| memberExpression LSQUARE expression RSQUARE
							| memberExpression DOT IDENTIFIER
							| NEW memberExpression arguements '''
	p[0]= ["memberExpression"] + [p[i] for i in range(1,len(p))]

def p_memberExpressionWithoutFunc(p):
	'''memberExpressionWithoutFunc : primaryExpressionWithoutFunc
							| memberExpressionWithoutFunc LSQUARE expression RSQUARE
							| memberExpressionWithoutFunc DOT IDENTIFIER
							| NEW memberExpression arguements '''
	p[0]= ["memberExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]



# def p_memberExpressionForIn(p):
# 	'''memberExpressionForIn : functionExpression
# 							| primaryExpression
# 							| memberExpression LSQUARE expression RSQUARE
# 							| memberExpression DOT IDENTIFIER
# 							| NEW memberExpression arguements'''


def p_expression(p):
	'''expression : assignmentExpression
					| expression COMMA assignmentExpression '''
	p[0]= ["expression"] + [p[i] for i in range(1,len(p))]

def p_expressionWithoutFunc(p):
	'''expressionWithoutFunc : assignmentExpressionWithoutFunc
					| expressionWithoutFunc COMMA assignmentExpression '''
	p[0]= ["expressionWithoutFunc"] + [p[i] for i in range(1,len(p))]

def p_expressionNoIn(p):
	'''expressionNoIn : assignmentExpressionNoIn
					| assignmentExpressionNoIn tempExpressionNoIn'''
	p[0]= ["expressionNoIn"] + [p[i] for i in range(1,len(p))]

def p_tempExpressionNoIn(p):
	'''tempExpressionNoIn : COMMA assignmentExpressionNoIn
						| COMMA assignmentExpressionNoIn tempExpressionNoIn'''
	p[0]= ["tempExpressionNoIn"] + [p[i] for i in range(1,len(p))]

def p_primaryExpression(p):
	'''primaryExpression : THIS
						 | objectLiteral
						 | LPAREN expression RPAREN
						 | IDENTIFIER
						 | literal
						 | arrayLiteral '''
	p[0]= ["primaryExpression"] + [p[i] for i in range(1,len(p))]

def p_primaryExpressionWithoutFunc(p):
	'''primaryExpressionWithoutFunc : THIS
						 | LPAREN expression RPAREN
						 | IDENTIFIER
						 | literal
						 | arrayLiteral '''
	p[0]= ["primaryExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]


def p_literal(p):
	'''literal : NUMBER
				| EXPO_NUMBER
				| OCTAL_NUMBER
				| HEXADECIMAL
				| STRING
				| NULL
				| FALSE'''
	p[0]= ["literal"] + [p[i] for i in range(1,len(p))]


def p_arrayLiteral(p):
	'''arrayLiteral : LSQUARE RSQUARE
					| LSQUARE elison RSQUARE
					| LSQUARE elementList COMMA elison RSQUARE
					| LSQUARE elementList COMMA RSQUARE'''
	p[0]= ["arrayLiteral"] + [p[i] for i in range(1,len(p))]

def p_elementList(p):
	'''elementList : elison assignmentExpression
					| assignmentExpression
					| elementList COMMA elison assignmentExpression
					| elementList COMMA assignmentExpression'''
	p[0]= ["elementList"] + [p[i] for i in range(1,len(p))]

def p_elison(p):
	'''elison : COMMA
				| elison COMMA'''
	p[0]= ["elison"] + [p[i] for i in range(1,len(p))]

def p_objectLiteral(p):
	'''objectLiteral : OPEN_BRACE CLOSE_BRACE
					| OPEN_BRACE propertyNameAndValueList CLOSE_BRACE'''
	p[0]= ["objectLiteral"] + [p[i] for i in range(1,len(p))]

def p_propertyNameAndValueList(p):
	'''propertyNameAndValueList : propertyNameAndValue
								| propertyNameAndValue COMMA propertyNameAndValueList'''
	p[0]= ["propertyNameAndValueList"] + [p[i] for i in range(1,len(p))]

def p_propertyNameAndValue(p):
	'''propertyNameAndValue : propertyName COLON assignmentExpression'''
	p[0]= ["propertyNameAndValue"] + [p[i] for i in range(1,len(p))]


def p_propertyName(p):
	'''propertyName : IDENTIFIER
					| STRING
					| NUMBER'''
	p[0]= ["propertyName"] + [p[i] for i in range(1,len(p))]

def p_functionExpression(p):
	'''functionExpression : FUNCTION LPAREN RPAREN functionBody
							| FUNCTION IDENTIFIER LPAREN RPAREN functionBody
							| FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN functionBody
							| FUNCTION LPAREN formalParameterList RPAREN functionBody'''
	p[0]= ["functionExpression"] + [p[i] for i in range(1,len(p))]

def p_arguements(p):
	'''arguements : LPAREN RPAREN
				| LPAREN arguementList RPAREN'''
	p[0]= ["arguements"] + [p[i] for i in range(1,len(p))]

def p_arguementList(p):
	'''arguementList : assignmentExpression
					| assignmentExpression COMMA arguementList'''
	p[0]= ["arguementList"] + [p[i] for i in range(1,len(p))]

def p_callExpression(p):
	'''callExpression : memberExpression arguements
						| callExpression arguements
						| callExpression LSQUARE expression RSQUARE
						| callExpression DOT IDENTIFIER'''
	p[0]= ["callExpression"] + [p[i] for i in range(1,len(p))]

def p_callExpressionWithoutFunc(p):
	'''callExpressionWithoutFunc : memberExpressionWithoutFunc arguements
						| callExpressionWithoutFunc arguements
						| callExpressionWithoutFunc LSQUARE expression RSQUARE
						| callExpressionWithoutFunc DOT IDENTIFIER'''
	p[0]= ["callExpressionWithoutFunc"] + [p[i] for i in range(1,len(p))]

# def p_callExpressionForIn(p):
# 	'''callExpressionForIn : memberExpressionForIn arguements
# 						| memberExpressionForIn arguements tempCallExpression'''



parser = yacc.yacc()
if __name__ == "__main__":
	file_input = sys.argv[1]
	program = open(file_input).read()
	parsed_code = parser.parse(program,lexer = lexer)
	print parsed_code
