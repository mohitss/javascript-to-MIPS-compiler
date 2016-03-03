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
						| statement'''
	p[0]= ["sourceElement"] + [[p[i]] for i in range(1,len(p))]			

def p_functionDeclaration(p):
	'''functionDeclaration : FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN functionBody
						| FUNCTION IDENTIFIER LPAREN RPAREN functionBody '''

def p_formalParameterList(p):
	'''formalParameterList : IDENTIFIER 
							| formalParameterList COMMA IDENTIFIER'''

def p_functionBody(p):
	'''functionBody : OPEN_BRACE sourceElements CLOSE_BRACE 
					| OPEN_BRACE CLOSE_BRACE '''

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


def p_continueStatement(p):
	'''continueStatement : CONTINUE SEMI_COLON
						| CONTINUE IDENTIFIER SEMI_COLON'''


def p_breakStatement(p):
	'''breakStatement :  BREAK SEMI_COLON
						| BREAK IDENTIFIER SEMI_COLON'''

def p_returnStatement(p):
	'''returnStatement :  RETURN SEMI_COLON
						| RETURN expression SEMI_COLON'''

def p_withStatement(p):
	'''withStatement : WITH LPAREN expression RPAREN statement'''

def p_withStatementNoIf(p):
	'''withStatementNoIf : WITH LPAREN expression RPAREN statementNoIf'''

def p_switchStatement(p):
	'''switchStatement : SWITCH LPAREN expression RPAREN caseBlock'''

def p_caseBlock(p):
	'''caseBlock : OPEN_BRACE CLOSE_BRACE
					| OPEN_BRACE caseClauses CLOSE_BRACE
					| OPEN_BRACE defaultClause CLOSE_BRACE
					| OPEN_BRACE defaultClause caseClauses CLOSE_BRACE
					| OPEN_BRACE caseClauses defaultClause caseClauses CLOSE_BRACE
					| OPEN_BRACE caseClauses defaultClause CLOSE_BRACE'''

def p_defaultClause(p):
	'''defaultClause : DEFAULT COLON 
					| DEFAULT COLON statementList'''

def p_caseClauses(p):
	'''caseClauses : caseClause
					| caseClause caseClauses'''

def p_caseClause(p):
	'''caseClause : CASE expression COLON
					| CASE expression COLON statementList'''


def p_labelledStatement(p):
	'''labelledStatement : IDENTIFIER COLON statement'''

def p_labelledStatementNoIf(p):
	'''labelledStatementNoIf : IDENTIFIER COLON statementNoIf'''

def p_throwStatement(p):
	'''throwStatement : THROW expression SEMI_COLON'''

def p_tryStatement(p):
	'''tryStatement : TRY block finally 
					| TRY block catch
					| TRY block catch finally'''

def p_catch(p):
	'''catch : CATCH LPAREN IDENTIFIER RPAREN block'''

def p_finally(p):
	'''finally : FINALLY block'''

def p_emptyStatement(p):
	'''emptyStatement : SEMI_COLON '''

def p_expressionStatement(p):
	'''expressionStatement : expressionWithoutFunc SEMI_COLON'''

def p_ifStatement(p):
	'''ifStatement : IF LPAREN expression RPAREN statement
					| IF LPAREN expression RPAREN statementNoIf ELSE statement'''

def p_ifStatementNoIf(p):
	'''ifStatementNoIf : IF LPAREN expression RPAREN statementNoIf ELSE statementNoIf'''

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

def p_variableDeclarationListNoIn(p):
	'''variableDeclarationListNoIn : variableDeclarationNoIn 
								| variableDeclarationListNoIn COMMA variableDeclarationNoIn '''

def p_variableDeclaration(p):
	'''variableDeclaration : IDENTIFIER initialiser 
							| IDENTIFIER'''

def p_variableDeclarationNoIn(p):
	'''variableDeclarationNoIn : IDENTIFIER initialiserNoIn 
							| IDENTIFIER'''

def p_initialiser(p):
	'''initialiser : OP_ASSIGNMENT assignmentExpression'''


def p_initialiserNoIn(p):
	'''initialiserNoIn : OP_ASSIGNMENT assignmentExpressionNoIn'''



def p_assignmentExpressionWithoutFunc(p):
	'''assignmentExpressionWithoutFunc : conditionalExpressionWithoutFunc
							| leftHandSideExpressionWithoutFunc assignmentOperator assignmentExpression'''

def p_assignmentExpression(p):
	'''assignmentExpression : conditionalExpression
							| leftHandSideExpression assignmentOperator assignmentExpression'''

def p_assignmentExpressionNoIn(p):
	'''assignmentExpressionNoIn : conditionalExpressionNoIn
							| leftHandSideExpression assignmentOperator assignmentExpressionNoIn'''

def p_assignmentOperator(p):
	'''assignmentOperator : OP_ASSIGNMENT
							| OP_PLUSEQUAL
							| OP_MINUSEQUAL
							| OP_MULTEQUAL
							| OP_DIVEQUAL
							| OP_MODEQUAL'''

def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression
							 | logicalOrExpression OP_TERNARY assignmentExpression COLON assignmentExpression '''

def p_conditionalExpressionWithoutFunc(p):
	'''conditionalExpressionWithoutFunc : logicalOrExpressionWithoutFunc
							 | logicalOrExpressionWithoutFunc OP_TERNARY assignmentExpression COLON assignmentExpression '''


def p_conditionalExpressionNoIn(p):
	'''conditionalExpressionNoIn : logicalOrExpressionNoIn
							 | logicalOrExpressionNoIn OP_TERNARY assignmentExpressionNoIn COLON assignmentExpressionNoIn '''

def p_logicalOrExpressionWithoutFunc(p):
	'''logicalOrExpressionWithoutFunc : logicalAndExpressionWithoutFunc
							| logicalAndExpressionWithoutFunc tempLogicalOrExpression'''

def p_logicalOrExpression(p):
	'''logicalOrExpression : logicalAndExpression
							| logicalAndExpression tempLogicalOrExpression'''

def p_logicalOrExpressionNoIn(p):
	'''logicalOrExpressionNoIn : logicalAndExpressionNoIn
							| logicalAndExpressionNoIn tempLogicalOrExpressionNoIn'''

def p_tempLogicalOrExpression(p):
	'''tempLogicalOrExpression : logicalOrOperator logicalAndExpression 
								| logicalOrOperator logicalAndExpression tempLogicalOrExpression'''


def p_tempLogicalOrExpressionNoIn(p):
	'''tempLogicalOrExpressionNoIn : logicalOrOperator logicalAndExpressionNoIn 
								| logicalOrOperator logicalAndExpressionNoIn tempLogicalOrExpressionNoIn'''


def p_logicalOrOperator(p):
	'''logicalOrOperator : OP_OR '''

def p_logicalAndExpression(p):
	'''logicalAndExpression : bitWiseOrExpression 
	 						| bitWiseOrExpression tempLogicalAndExpression'''

def p_logicalAndExpressionWithoutFunc(p):
	'''logicalAndExpressionWithoutFunc : bitWiseOrExpressionWithoutFunc 
	 						| bitWiseOrExpressionWithoutFunc tempLogicalAndExpression'''

def p_tempLogicalAndExpression(p):
	'''tempLogicalAndExpression : logicalAndOperator bitWiseOrExpression 
								| logicalAndOperator bitWiseOrExpression tempLogicalAndExpression'''

def p_logicalAndExpressionNoIn(p):
	'''logicalAndExpressionNoIn : bitWiseOrExpressionNoIn 
							| bitWiseOrExpressionNoIn tempLogicalAndExpressionNoIn'''

def p_tempLogicalAndExpressionNoIn(p):
	'''tempLogicalAndExpressionNoIn : logicalAndOperator bitWiseOrExpressionNoIn 
								| logicalAndOperator bitWiseOrExpressionNoIn tempLogicalAndExpressionNoIn'''

def p_logicalAndOperator(p):
	'''logicalAndOperator : OP_AND'''


def p_bitWiseOrExpression(p):
	'''bitWiseOrExpression : bitWiseXorExpression
 							| bitWiseXorExpression tempBitWiseOrExpression'''

def p_bitWiseOrExpressionWithoutFunc(p):
	'''bitWiseOrExpressionWithoutFunc : bitWiseXorExpressionWithoutFunc
 							| bitWiseXorExpressionWithoutFunc tempBitWiseOrExpression'''

def p_tempBitWiseOrExpression(p):
	'''tempBitWiseOrExpression : bitWiseOrOperator bitWiseXorExpression
								| bitWiseOrOperator bitWiseXorExpression tempBitWiseOrExpression'''

def p_bitWiseOrExpressionNoIn(p):
	'''bitWiseOrExpressionNoIn : bitWiseXorExpressionNoIn
							| bitWiseXorExpressionNoIn tempBitWiseOrExpressionNoIn'''

def p_tempBitWiseOrExpressionNoIn(p):
	'''tempBitWiseOrExpressionNoIn : bitWiseOrOperator bitWiseXorExpressionNoIn
								| bitWiseOrOperator bitWiseXorExpressionNoIn tempBitWiseOrExpressionNoIn'''

def p_bitWiseOrOperator(p):
	'''bitWiseOrOperator : BITWISE_OR'''


def p_bitWiseXorExpression(p):
	'''bitWiseXorExpression : bitWiseAndExpression
							| bitWiseAndExpression tempBitWiseXorExpression'''

def p_bitWiseXorExpressionWithoutFunc(p):
	'''bitWiseXorExpressionWithoutFunc : bitWiseAndExpressionWithoutFunc
							| bitWiseAndExpressionWithoutFunc tempBitWiseXorExpression'''

def p_tempBitWiseXorExpression(p):
	'''tempBitWiseXorExpression : bitWiseXorOperator bitWiseAndExpression
								| bitWiseXorOperator bitWiseAndExpression tempBitWiseXorExpression'''

def p_bitWiseXorExpressionNoIn(p):
	'''bitWiseXorExpressionNoIn : bitWiseAndExpressionNoIn
							| bitWiseAndExpressionNoIn tempBitWiseXorExpressionNoIn'''


def p_tempBitWiseXorExpressionNoIn(p):
	'''tempBitWiseXorExpressionNoIn : bitWiseXorOperator bitWiseAndExpressionNoIn
								| bitWiseXorOperator bitWiseAndExpressionNoIn tempBitWiseXorExpressionNoIn'''

def p_bitWiseXorOperator(p):
	'''bitWiseXorOperator : BITWISE_XOR'''


def p_bitWiseAndExpression(p):
	'''bitWiseAndExpression : equalityExpression
							| equalityExpression tempBitWiseAndExpression'''

def p_bitWiseAndExpressionWithoutFunc(p):
	'''bitWiseAndExpressionWithoutFunc : equalityExpressionWithoutFunc
							| equalityExpressionWithoutFunc tempBitWiseAndExpression'''


def p_tempBitWiseAndExpression(p):
	'''tempBitWiseAndExpression : bitWiseAndOperator equalityExpression
								| bitWiseAndOperator equalityExpression tempBitWiseAndExpression'''


def p_bitWiseAndExpressionNoIn(p):
	'''bitWiseAndExpressionNoIn : equalityExpressionNoIn
							| equalityExpressionNoIn tempBitWiseAndExpressionNoIn'''


def p_tempBitWiseAndExpressionNoIn(p):
	'''tempBitWiseAndExpressionNoIn : bitWiseAndOperator equalityExpressionNoIn
								| bitWiseAndOperator equalityExpressionNoIn tempBitWiseAndExpressionNoIn'''

def p_bitWiseAndOperator(p):
	'''bitWiseAndOperator : BITWISE_AND'''


def p_equalityExpression(p):
	'''equalityExpression : relationalExpression 
							 | relationalExpression tempEqualityExpression'''

def p_equalityExpressionWithoutFunc(p):
	'''equalityExpressionWithoutFunc : relationalExpressionWithoutFunc 
							 | relationalExpressionWithoutFunc tempEqualityExpression'''

def p_tempEqualityExpression(p):
	'''tempEqualityExpression : equalityOperator relationalExpression
								| equalityOperator relationalExpression tempEqualityExpression'''


def p_equalityExpressionNoIn(p):
	'''equalityExpressionNoIn : relationalExpressionNoIn 
							| equalityExpressionNoIn OP_EQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_UNIVEQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_NOTEQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_NOTUNIVEQUAL relationalExpressionNoIn'''


def p_equalityOperator(p):
	'''equalityOperator : OP_EQUAL
						| OP_UNIVEQUAL
						| OP_NOTEQUAL
						| OP_NOTUNIVEQUAL'''


def p_relationalExpression(p):
	'''relationalExpression :  shiftExpression
							| relationalExpression OP_GREATER shiftExpression
							| relationalExpression OP_LESS shiftExpression
							| relationalExpression OP_GREATEREQUAL shiftExpression
							| relationalExpression OP_LESSEQUAL shiftExpression
							| relationalExpression INSTANCEOF shiftExpression
							| relationalExpression IN shiftExpression'''

def p_relationalExpressionWithoutFunc(p):
	'''relationalExpressionWithoutFunc :  shiftExpressionWithoutFunc
							| relationalExpressionWithoutFunc OP_GREATER shiftExpression
							| relationalExpressionWithoutFunc OP_LESS shiftExpression
							| relationalExpressionWithoutFunc OP_GREATEREQUAL shiftExpression
							| relationalExpressionWithoutFunc OP_LESSEQUAL shiftExpression
							| relationalExpressionWithoutFunc INSTANCEOF shiftExpression
							| relationalExpressionWithoutFunc IN shiftExpression'''														

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


def p_shiftExpression(p):
	'''shiftExpression : additiveExpression
						| additiveExpression tempShiftExpression'''

def p_shiftExpressionWithoutFunc(p):
	'''shiftExpressionWithoutFunc : additiveExpressionWithoutFunc
						| additiveExpressionWithoutFunc tempShiftExpression'''						

def p_tempShiftExpression(p):
	'''tempShiftExpression : shiftOperator additiveExpression
							| shiftOperator additiveExpression tempShiftExpression'''


def p_shiftOperator(p):
	'''shiftOperator : OP_LSHIFT
					| OP_RSHIFT'''


def p_additiveExpression(p):
	'''additiveExpression  : multiplicativeExpression 
 							| multiplicativeExpression tempAdditiveExpression'''

def p_additiveExpressionWithoutFunc(p):
	'''additiveExpressionWithoutFunc  : multiplicativeExpressionWithoutFunc 
 							| multiplicativeExpressionWithoutFunc tempAdditiveExpression''' 							

def p_tempAdditiveExpression(p):
	'''tempAdditiveExpression : additiveOperator multiplicativeExpression
								| additiveOperator multiplicativeExpression tempAdditiveExpression'''

def p_multiplicativeExpressionWithoutFunc(p):
	'''multiplicativeExpressionWithoutFunc : unaryExpressionWithoutFunc 
								| unaryExpressionWithoutFunc tempMultiplicativeExpression'''

def p_multiplicativeExpression(p):
	'''multiplicativeExpression : unaryExpression 
								| unaryExpression tempMultiplicativeExpression'''								

def p_tempMultiplicativeExpression(p):
	'''tempMultiplicativeExpression : multiplicativeOperator unaryExpression
									| multiplicativeOperator unaryExpression tempMultiplicativeExpression'''


def p_multiplicativeOperator(p):
	'''multiplicativeOperator : OP_MULT
								| OP_MODULUS
								| OP_DIVIDE'''

def p_additiveOperator(p):
	'''additiveOperator : OP_PLUS 
						| OP_MINUS '''


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

def p_postFixExpression(p):
	'''postFixExpression :  leftHandSideExpression 
							| leftHandSideExpression OP_INCREMENT
							| leftHandSideExpression OP_DECREMENT'''

def p_postFixExpressionWithoutFunc(p):
	'''postFixExpressionWithoutFunc :  leftHandSideExpressionWithoutFunc
							| leftHandSideExpressionWithoutFunc OP_INCREMENT
							| leftHandSideExpressionWithoutFunc OP_DECREMENT'''


def p_leftHandSideExpression(p):
	'''leftHandSideExpression : newExpression
								| callExpression'''

def p_leftHandSideExpressionWithoutFunc(p):
	'''leftHandSideExpressionWithoutFunc : newExpressionWithoutFunc
								| callExpressionWithoutFunc'''

def p_newExpression(p):
	'''newExpression : memberExpression
						| NEW newExpression'''

def p_newExpressionWithoutFunc(p):
	'''newExpressionWithoutFunc : memberExpressionWithoutFunc
						| NEW newExpression'''						

def p_memberExpression(p):
	'''memberExpression : functionExpression 
							| primaryExpression 
							| memberExpression LSQUARE expression RSQUARE
							| memberExpression DOT IDENTIFIER
							| NEW memberExpression arguements '''

def p_memberExpressionWithoutFunc(p):
	'''memberExpressionWithoutFunc : primaryExpressionWithoutFunc 
							| memberExpressionWithoutFunc LSQUARE expression RSQUARE
							| memberExpressionWithoutFunc DOT IDENTIFIER
							| NEW memberExpression arguements '''							



# def p_memberExpressionForIn(p):
# 	'''memberExpressionForIn : functionExpression 
# 							| primaryExpression 
# 							| memberExpression LSQUARE expression RSQUARE
# 							| memberExpression DOT IDENTIFIER
# 							| NEW memberExpression arguements'''


def p_expression(p):
	'''expression : assignmentExpression 
					| expression COMMA assignmentExpression '''

def p_expressionWithoutFunc(p):
	'''expressionWithoutFunc : assignmentExpressionWithoutFunc 
					| expressionWithoutFunc COMMA assignmentExpression '''

def p_expressionNoIn(p):
	'''expressionNoIn : assignmentExpressionNoIn 
					| assignmentExpressionNoIn tempExpressionNoIn'''

def p_tempExpressionNoIn(p):
	'''tempExpressionNoIn : COMMA assignmentExpressionNoIn
						| COMMA assignmentExpressionNoIn tempExpressionNoIn'''

def p_primaryExpression(p):
	'''primaryExpression : THIS
						 | objectLiteral
						 | LPAREN expression RPAREN
						 | IDENTIFIER 
						 | literal 
						 | arrayLiteral '''

def p_primaryExpressionWithoutFunc(p):
	'''primaryExpressionWithoutFunc : THIS
						 | LPAREN expression RPAREN
						 | IDENTIFIER 
						 | literal 
						 | arrayLiteral '''


def p_literal(p):
	'''literal : NUMBER 
				| EXPO_NUMBER
				| OCTAL_NUMBER
				| HEXADECIMAL
				| STRING
				| NULL
				| FALSE'''


def p_arrayLiteral(p):
	'''arrayLiteral : LSQUARE RSQUARE
					| LSQUARE elison RSQUARE
					| LSQUARE elementList COMMA elison RSQUARE
					| LSQUARE elementList COMMA RSQUARE'''

def p_elementList(p):
	'''elementList : elison assignmentExpression
					| assignmentExpression
					| elementList COMMA elison assignmentExpression
					| elementList COMMA assignmentExpression'''

def p_elison(p):
	'''elison : COMMA
				| elison COMMA'''

def p_objectLiteral(p):
	'''objectLiteral : OPEN_BRACE CLOSE_BRACE
					| OPEN_BRACE propertyNameAndValueList CLOSE_BRACE'''

def p_propertyNameAndValueList(p):
	'''propertyNameAndValueList : propertyNameAndValue
								| propertyNameAndValue COMMA propertyNameAndValueList'''

def p_propertyNameAndValue(p):
	'''propertyNameAndValue : propertyName COLON assignmentExpression'''


def p_propertyName(p):
	'''propertyName : IDENTIFIER 
					| STRING
					| NUMBER'''

def p_functionExpression(p):
	'''functionExpression : FUNCTION LPAREN RPAREN functionBody
							| FUNCTION IDENTIFIER LPAREN RPAREN functionBody
							| FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN functionBody
							| FUNCTION LPAREN formalParameterList RPAREN functionBody'''

def p_arguements(p):
	'''arguements : LPAREN RPAREN
				| LPAREN arguementList RPAREN'''

def p_arguementList(p):
	'''arguementList : assignmentExpression 
					| assignmentExpression COMMA arguementList'''

def p_callExpression(p):
	'''callExpression : memberExpression arguements 
						| callExpression arguements
						| callExpression LSQUARE expression RSQUARE
						| callExpression DOT IDENTIFIER'''

def p_callExpressionWithoutFunc(p):
	'''callExpressionWithoutFunc : memberExpressionWithoutFunc arguements 
						| callExpressionWithoutFunc arguements
						| callExpressionWithoutFunc LSQUARE expression RSQUARE
						| callExpressionWithoutFunc DOT IDENTIFIER'''

# def p_callExpressionForIn(p):
# 	'''callExpressionForIn : memberExpressionForIn arguements 
# 						| memberExpressionForIn arguements tempCallExpression'''



parser = yacc.yacc()
if __name__ == "__main__":
    file_input = sys.argv[1]
    program = open(file_input).read()
    parsed_code = parser.parse(program,lexer = lexer)
    print parsed_code
