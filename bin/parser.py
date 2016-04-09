import sys
import regalloc
import json
import ply.lex as lex
from lexer import tokens,lexer
import ply.yacc as yacc
import sys
import subprocess
from symbolTable import *
from threeAddressCode import *
no_if = 0
def copy(a):
	return a.copy()

symbTab = symbolTable()
tac = TAC('output.txt')

start = 'start'

def getHigherPrecedence(type1,type2):
	perecedence_order = ["string","exponumber","number","boolean"]
	if type1 == "undefined" or type2 == "undefined":
		return "NaN"
	index1 = perecedence_order.index(type1)
	index2 = perecedence_order.index(type2)
	return perecedence_order[min(index1,index2)]

start = 'start'


def raise_error(str):
	print str
	print "Stopping compilation"
	import sys
	sys.exit()

def generate_output(lis):
	non_terminal = lis[0]
	string = "<span style='color:red;'>"+str(non_terminal)+"</span>&nbsp;&nbsp;==>>"
	for i in range(1,len(lis)):
		if isinstance(lis[i],lex.LexToken):
			string += "&nbsp;&nbsp;"+str(lis[i].value)+"&nbsp;&nbsp;"
		else:
			string += "&nbsp;&nbsp;<span style='color:red;'>"+str(lis[i])+"</span>&nbsp;&nbsp;"
	string += "<br>\n"
	f.write(string)


def p_empty(p):
	'empty :'
	p[0] = {}
	p[0]["code"] = []
	pass

def p_start(p):
	'''start : sourceElements
			| empty'''
	p[0] = {}
	p[0]["code"] = p[1]["code"]
	final_code = ""
	f = open('output.s','w')
	for codes in p[0]["code"]:
		print codes
		write = str(codes[0])+","+str(codes[1])
		try:
			if codes[2] != "":
				write+=","+str(codes[2])
		except:
			pass
		try:
			if codes[3] != "":
				write+=","+str(codes[3])
		except:
			pass
		try:
			if codes[4] != "":
				write+=","+str(codes[4])
		except:
			pass
		print write
		f.write(write+"\n")
	f.close()
	generate_output(p.slice)

def p_sourceElements(p):
	'''sourceElements : sourceElement
					| sourceElements sourceElement '''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
	else:
		p[0]["code"] = p[1]["code"] + p[2]["code"]
	generate_output(p.slice)

def p_sourceElement(p):
	'''sourceElement : functionDeclaration
						| statement'''
	p[0] = {}
	p[0]["code"] = p[1]["code"]
	# print p[0]  
	
	generate_output(p.slice)

def p_functionDeclaration(p):
	'''functionDeclaration : FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN functionBody
						| FUNCTION IDENTIFIER LPAREN RPAREN functionBody '''
	generate_output(p.slice)

def p_formalParameterList(p):
	'''formalParameterList : IDENTIFIER
							| formalParameterList COMMA IDENTIFIER'''
	generate_output(p.slice)

def p_functionBody(p):
	'''functionBody : OPEN_BRACE sourceElements CLOSE_BRACE
					| OPEN_BRACE CLOSE_BRACE '''
	generate_output(p.slice)


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
	p[0] = {}
	p[0] = dict(p[1])
	# print "statement ",p[0]  
	
	generate_output(p.slice)

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
	p[0] = {}
	p[0] = dict(p[1])
	generate_output(p.slice)


def p_continueStatement(p):
	'''continueStatement : CONTINUE SEMI_COLON
						| CONTINUE IDENTIFIER SEMI_COLON'''
	generate_output(p.slice)


def p_breakStatement(p):
	'''breakStatement :  BREAK SEMI_COLON
						| BREAK IDENTIFIER SEMI_COLON'''
	generate_output(p.slice)


def p_returnStatement(p):
	'''returnStatement :  RETURN SEMI_COLON
						| RETURN expression SEMI_COLON'''
	generate_output(p.slice)


def p_withStatement(p):
	'''withStatement : WITH LPAREN expression RPAREN statement'''
	generate_output(p.slice)


def p_withStatementNoIf(p):
	'''withStatementNoIf : WITH LPAREN expression RPAREN statementNoIf'''
	generate_output(p.slice)


def p_switchStatement(p):
	'''switchStatement : SWITCH LPAREN expression RPAREN caseBlock'''
	generate_output(p.slice)


def p_caseBlock(p):
	'''caseBlock : OPEN_BRACE CLOSE_BRACE
					| OPEN_BRACE caseClauses CLOSE_BRACE
					| OPEN_BRACE defaultClause CLOSE_BRACE
					| OPEN_BRACE defaultClause caseClauses CLOSE_BRACE
					| OPEN_BRACE caseClauses defaultClause caseClauses CLOSE_BRACE
					| OPEN_BRACE caseClauses defaultClause CLOSE_BRACE'''
	generate_output(p.slice)


def p_defaultClause(p):
	'''defaultClause : DEFAULT COLON
					| DEFAULT COLON statementList'''
	generate_output(p.slice)


def p_caseClauses(p):
	'''caseClauses : caseClause
					| caseClause caseClauses'''
	generate_output(p.slice)


def p_caseClause(p):
	'''caseClause : CASE expression COLON
					| CASE expression COLON statementList'''
	generate_output(p.slice)



def p_labelledStatement(p):
	'''labelledStatement : IDENTIFIER COLON statement'''
	generate_output(p.slice)


def p_labelledStatementNoIf(p):
	'''labelledStatementNoIf : IDENTIFIER COLON statementNoIf'''
	generate_output(p.slice)


def p_throwStatement(p):
	'''throwStatement : THROW expression SEMI_COLON'''
	generate_output(p.slice)


def p_tryStatement(p):
	'''tryStatement : TRY block finally
					| TRY block catch
					| TRY block catch finally'''
	generate_output(p.slice)


def p_catch(p):
	'''catch : CATCH LPAREN IDENTIFIER RPAREN block'''
	generate_output(p.slice)


def p_finally(p):
	'''finally : FINALLY block'''
	generate_output(p.slice)


def p_emptyStatement(p):
	'''emptyStatement : SEMI_COLON '''
	p[0] = {}
	p[0]["code"] = []
	generate_output(p.slice)


def p_expressionStatement(p):
	'''expressionStatement : expressionWithoutFunc SEMI_COLON'''
	p[0] = {}
	p[0] = p[1]
	print "exp 0",p[1]
	generate_output(p.slice)


def p_ifStatementNoIf(p):
	'''ifStatementNoIf : IF LPAREN expression RPAREN statementNoIf ELSE statementNoIf'''
	p[0] = {}
	p[0]["code"] = p[3]["code"]
	no_if = tac.newLabel()
	p[0]["code"] += [["ifgoto","beq",p[3]["place"],0,"truth"+str(no_if)]]
	p[0]["code"] += [["goto","else"+str(no_if),"",""]]
	p[0]["code"] += [["label","truth"+str(no_if),"",""]]
	p[0]["code"] += p[5]["code"]
	p[0]["code"] += [["goto","after"+str(no_if),"",""]]
	p[0]["code"] += [["label","else"+str(no_if),"",""]]
	p[0]["code"] += p[7]["code"]
	p[0]["code"] += [["label","after"+str(no_if),"",""]]
	generate_output(p.slice)



def p_ifStatement(p):
	'''ifStatement :  IF LPAREN expression RPAREN statementNoIf ELSE statement
					| IF LPAREN expression RPAREN statement'''
	p[0] = {}
	p[0]["code"] = p[3]["code"]
	no_if = tac.newLabel()
	if len(p) == 6:
		p[0]["code"] += [["ifgoto","beq",p[3]["place"],0,"truth"+str(no_if)]]
		p[0]["code"] += [["goto","after"+str(no_if),"",""]]
		p[0]["code"] += [["label","truth"+str(no_if),"",""]]
		p[0]["code"] += p[5]["code"]
		p[0]["code"] += [["label","after"+str(no_if),"",""]]
	else:
		p[0]["code"] += [["ifgoto","beq",p[3]["place"],0,"truth"+str(no_if)]]
		p[0]["code"] += [["goto","else"+str(no_if),"",""]]
		p[0]["code"] += [["label","truth"+str(no_if),"",""]]
		p[0]["code"] += p[5]["code"]
		p[0]["code"] += [["goto","after"+str(no_if),"",""]]
		p[0]["code"] += [["label","else"+str(no_if),"",""]]
		p[0]["code"] += p[7]["code"]
		p[0]["code"] += [["label","after"+str(no_if),"",""]]
	generate_output(p.slice)



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
	p[0] = {}
	p[0]["code"] = []
	while_label = tac.newLabel()
	if p[1] == "while":
		p[0]["code"] += [["label","before_while_"+while_label]]
		p[0]["code"] += p[3]["code"]
		p[0]["code"] += [["ifgoto","beq",p[3]["place"],0,"truth"+while_label]]
		p[0]["code"] += [["goto","after_while_"+while_label]]
		p[0]["code"] += [["label","truth"+while_label]]
		p[0]["code"] += p[5]["code"]
		p[0]["code"] += [["goto","before_while_"+while_label]]
		p[0]["code"] += [["label","after_while_"+while_label]]
	elif p[1]=="for" and p[2] == "(" and p[3] == ";" and p[4] == ";" and p[5] == ")" :
		p[0]["code"] += [["label","before_for_"+while_label]]
		p[0]["code"] += p[6]["code"]
		p[0]["code"] += [["goto","before_for_"+while_label]]
		p[0]["code"] += [["label","after_for_"+while_label]]
	generate_output(p.slice)


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
	p[0] = {}
	p[0]["code"] = []
	while_label = tac.newLabel()
	if p[1] == "while":
		p[0]["code"] += [["label","before_while_"+while_label]]
		p[0]["code"] += p[3]["code"]
		p[0]["code"] += [["ifgoto","beq",p[3]["place"],0,"truth"+while_label]]
		p[0]["code"] += [["goto","after_while_"+while_label]]
		p[0]["code"] += [["label","truth"+while_label]]
		p[0]["code"] += p[5]["code"]
		p[0]["code"] += [["goto","before_while_"+while_label]]
		p[0]["code"] += [["label","after_while_"+while_label]]
	elif p[1]=="for" and p[2] == "(" and p[3] == ";" and p[4] == ";" and p[5] == ")" :
		p[0]["code"] += [["label","before_for_"+while_label]]
		p[0]["code"] += p[6]["code"]
		p[0]["code"] += [["goto","before_for_"+while_label]]
		p[0]["code"] += [["label","after_for_"+while_label]]
	generate_output(p.slice)


def p_block(p):
	'''block : OPEN_BRACE statementList CLOSE_BRACE
			| OPEN_BRACE CLOSE_BRACE'''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 4:
		p[0] = dict(p[2])
	generate_output(p.slice)


def p_statementList(p):
	'''statementList : statement
					| statementList statement'''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 2:
		p[0] = dict(p[1])
	else:
		p[0]["code"] = p[1]["code"] + p[2]["code"]
	# print "list is ",p[0]
	generate_output(p.slice)


def p_variableStatement(p):
	'''variableStatement : VAR variableDeclarationList SEMI_COLON '''
	p[0] = {}
	p[0]["code"] = p[2]["code"]
	generate_output(p.slice)


def p_variableDeclarationList(p):
	'''variableDeclarationList : variableDeclaration
								| variableDeclarationList COMMA variableDeclaration '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
	else:
		p[0]["code"] = p[1]["code"] + p[3]["code"]
	# print p[0]  

	generate_output(p.slice)


def p_variableDeclarationListNoIn(p):
	'''variableDeclarationListNoIn : variableDeclarationNoIn
								| variableDeclarationListNoIn COMMA variableDeclarationNoIn '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
	else:
		p[0]["code"] = p[1]["code"] + p[3]["code"]
	generate_output(p.slice)


def p_variableDeclaration(p):
	'''variableDeclaration : IDENTIFIER initialiser
							| IDENTIFIER'''
	p[0] = {}
	if len(p)==2:
		p[0]["place"] = p[1]
		p[0]["code"] = []
		temp = symbTab.lookup(p[1])
		if temp == None:
			symbTab.insert(p[1],"undefined")	
	else:
		p[0]["code"] = []
		p[0]["code"] = p[2]["code"]
		p[0]["code"] += [["=",p[1],p[2]["place"],""]]            #[operation,dest,reg1,reg2]
		temp = symbTab.lookup(p[1])
		symbTab.insert(p[1],p[2]["type"])
	# print p[0]  
	generate_output(p.slice)


def p_variableDeclarationNoIn(p):
	'''variableDeclarationNoIn : IDENTIFIER initialiserNoIn
							| IDENTIFIER'''
	p[0] = {}
	if len(p)==2:
		p[0]["place"] = p[1]
		p[0]["code"] = []
		temp = symbTab.lookup(p[1])
		if temp == None:
			symbTab.insert(p[1],"undefined")	
	else:
		p[0]["code"] = []
		p[0]["code"] = p[2]["code"]
		p[0]["code"] += [["=",p[1],p[2]["place"],""]]            #[operation,dest,reg1,reg2]
		temp = symbTab.lookup(p[1])
		symbTab.insert(p[1],p[2]["type"])  
	generate_output(p.slice)



def p_initialiser(p):
	'''initialiser : OP_ASSIGNMENT assignmentExpression'''
	p[0] = {}
	p[0]["code"] = p[2]["code"]
	p[0]["place"] = p[2]["place"]
	p[0]["type"] = p[2]["type"]
	generate_output(p.slice)



def p_initialiserNoIn(p):
	'''initialiserNoIn : OP_ASSIGNMENT assignmentExpressionNoIn'''
	p[0] = {}
	p[0]["code"] = p[2]["code"]
	p[0]["place"] = p[2]["place"]
	p[0]["type"] = p[2]["type"]
	generate_output(p.slice)



def p_assignmentExpressionWithoutFunc(p):
	'''assignmentExpressionWithoutFunc : conditionalExpressionWithoutFunc
							| leftHandSideExpressionWithoutFunc assignmentOperator assignmentExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["place"] = p[3]["place"]
		p[0]["code"] = p[1]["code"] + p[3]["code"]
		p[0]["type"] = p[3]["type"]
		symbTab.insert(p[1]["place"],p[3]["type"])
 		if p[2]["operator"] == "=":
			p[0]["code"] += [["=",p[1]["place"],p[3]["place"],""]]
			p[1]["type"] = p[3]["type"]
		else:
			p[0]["code"] += [[p[2]["operator"],p[1]["place"],p[3]["place"],""]]
			p[1]["type"] = p[3]["type"]
	generate_output(p.slice)


def p_assignmentExpression(p):
	'''assignmentExpression : conditionalExpression
							| leftHandSideExpression assignmentOperator assignmentExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["place"] = p[3]["place"]
		p[0]["code"] = p[1]["code"] + p[3]["code"]
		p[0]["type"] = p[3]["type"]
		symbTab.insert(p[1]["place"],p[3]["type"])
 		if p[2]["operator"] == "=":
			p[0]["code"] += [["=",p[1]["place"],p[3]["place"],""]]
			p[1]["type"] = p[3]["type"]
		else:
			p[0]["code"] += [[p[2]["operator"],p[1]["place"],p[3]["place"],""]]
			p[1]["type"] = p[3]["type"]
	generate_output(p.slice)


def p_assignmentExpressionNoIn(p):
	'''assignmentExpressionNoIn : conditionalExpressionNoIn
							| leftHandSideExpression assignmentOperator assignmentExpressionNoIn'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["place"] = p[3]["place"]
		p[0]["code"] = p[1]["code"] + p[3]["code"]
		p[0]["type"] = p[3]["type"]
		symbTab.insert(p[1]["place"],p[3]["type"])
 		if p[2]["operator"] == "=":
			p[0]["code"] += [["=",p[1]["place"],p[3]["place"],""]]
			p[1]["type"] = p[3]["type"]
		else:
			p[0]["code"] += [[p[2]["operator"],p[1]["place"],p[3]["place"],""]]
			p[1]["type"] = p[3]["type"]
	generate_output(p.slice)


def p_assignmentOperator(p):
	'''assignmentOperator : OP_ASSIGNMENT
							| OP_PLUSEQUAL
							| OP_MINUSEQUAL
							| OP_MULTEQUAL
							| OP_DIVEQUAL
							| OP_MODEQUAL'''
	p[0] = {}
	p[0]["operator"] = p[1]
	generate_output(p.slice)


def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression
							 | logicalOrExpression OP_TERNARY assignmentExpression COLON assignmentExpression '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)


def p_conditionalExpressionWithoutFunc(p):
	'''conditionalExpressionWithoutFunc : logicalOrExpressionWithoutFunc
							 | logicalOrExpressionWithoutFunc OP_TERNARY assignmentExpression COLON assignmentExpression '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass


	generate_output(p.slice)



def p_conditionalExpressionNoIn(p):
	'''conditionalExpressionNoIn : logicalOrExpressionNoIn
							 | logicalOrExpressionNoIn OP_TERNARY assignmentExpressionNoIn COLON assignmentExpressionNoIn '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_logicalOrExpressionWithoutFunc(p):
	'''logicalOrExpressionWithoutFunc : logicalAndExpressionWithoutFunc
							| logicalAndExpressionWithoutFunc tempLogicalOrExpression'''
	p[0] = {}
	print "p1is ",p[1]
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_logicalOrExpression(p):
	'''logicalOrExpression : logicalAndExpression
							| logicalAndExpression tempLogicalOrExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_logicalOrExpressionNoIn(p):
	'''logicalOrExpressionNoIn : logicalAndExpressionNoIn
							| logicalAndExpressionNoIn tempLogicalOrExpressionNoIn'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempLogicalOrExpression(p):
	'''tempLogicalOrExpression : logicalOrOperator logicalAndExpression
								| logicalOrOperator logicalAndExpression tempLogicalOrExpression'''
	generate_output(p.slice)


def p_tempLogicalOrExpressionNoIn(p):
	'''tempLogicalOrExpressionNoIn : logicalOrOperator logicalAndExpressionNoIn
								| logicalOrOperator logicalAndExpressionNoIn tempLogicalOrExpressionNoIn'''
	generate_output(p.slice)


def p_logicalOrOperator(p):
	'''logicalOrOperator : OP_OR '''
	generate_output(p.slice)

def p_logicalAndExpression(p):
	'''logicalAndExpression : bitWiseOrExpression
	 						| bitWiseOrExpression tempLogicalAndExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_logicalAndExpressionWithoutFunc(p):
	'''logicalAndExpressionWithoutFunc : bitWiseOrExpressionWithoutFunc
	 						| bitWiseOrExpressionWithoutFunc tempLogicalAndExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempLogicalAndExpression(p):
	'''tempLogicalAndExpression : logicalAndOperator bitWiseOrExpression
								| logicalAndOperator bitWiseOrExpression tempLogicalAndExpression'''
	generate_output(p.slice)


def p_logicalAndExpressionNoIn(p):
	'''logicalAndExpressionNoIn : bitWiseOrExpressionNoIn
							| bitWiseOrExpressionNoIn tempLogicalAndExpressionNoIn'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempLogicalAndExpressionNoIn(p):
	'''tempLogicalAndExpressionNoIn : logicalAndOperator bitWiseOrExpressionNoIn
								| logicalAndOperator bitWiseOrExpressionNoIn tempLogicalAndExpressionNoIn'''
	generate_output(p.slice)


def p_logicalAndOperator(p):
	'''logicalAndOperator : OP_AND'''
	generate_output(p.slice)


def p_bitWiseOrExpression(p):
	'''bitWiseOrExpression : bitWiseXorExpression
 							| bitWiseXorExpression tempBitWiseOrExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_bitWiseOrExpressionWithoutFunc(p):
	'''bitWiseOrExpressionWithoutFunc : bitWiseXorExpressionWithoutFunc
 							| bitWiseXorExpressionWithoutFunc tempBitWiseOrExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempBitWiseOrExpression(p):
	'''tempBitWiseOrExpression : bitWiseOrOperator bitWiseXorExpression
								| bitWiseOrOperator bitWiseXorExpression tempBitWiseOrExpression'''
	generate_output(p.slice)


def p_bitWiseOrExpressionNoIn(p):
	'''bitWiseOrExpressionNoIn : bitWiseXorExpressionNoIn
							| bitWiseXorExpressionNoIn tempBitWiseOrExpressionNoIn'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempBitWiseOrExpressionNoIn(p):
	'''tempBitWiseOrExpressionNoIn : bitWiseOrOperator bitWiseXorExpressionNoIn
								| bitWiseOrOperator bitWiseXorExpressionNoIn tempBitWiseOrExpressionNoIn'''
	generate_output(p.slice)


def p_bitWiseOrOperator(p):
	'''bitWiseOrOperator : BITWISE_OR'''
	generate_output(p.slice)


def p_bitWiseXorExpression(p):
	'''bitWiseXorExpression : bitWiseAndExpression
							| bitWiseAndExpression tempBitWiseXorExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_bitWiseXorExpressionWithoutFunc(p):
	'''bitWiseXorExpressionWithoutFunc : bitWiseAndExpressionWithoutFunc
							| bitWiseAndExpressionWithoutFunc tempBitWiseXorExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempBitWiseXorExpression(p):
	'''tempBitWiseXorExpression : bitWiseXorOperator bitWiseAndExpression
								| bitWiseXorOperator bitWiseAndExpression tempBitWiseXorExpression'''
	generate_output(p.slice)


def p_bitWiseXorExpressionNoIn(p):
	'''bitWiseXorExpressionNoIn : bitWiseAndExpressionNoIn
							| bitWiseAndExpressionNoIn tempBitWiseXorExpressionNoIn'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)



def p_tempBitWiseXorExpressionNoIn(p):
	'''tempBitWiseXorExpressionNoIn : bitWiseXorOperator bitWiseAndExpressionNoIn
								| bitWiseXorOperator bitWiseAndExpressionNoIn tempBitWiseXorExpressionNoIn'''
	generate_output(p.slice)


def p_bitWiseXorOperator(p):
	'''bitWiseXorOperator : BITWISE_XOR'''
	generate_output(p.slice)


def p_bitWiseAndExpression(p):
	'''bitWiseAndExpression : equalityExpression
							| equalityExpression tempBitWiseAndExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_bitWiseAndExpressionWithoutFunc(p):
	'''bitWiseAndExpressionWithoutFunc : equalityExpressionWithoutFunc
							| equalityExpressionWithoutFunc tempBitWiseAndExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempBitWiseAndExpression(p):
	'''tempBitWiseAndExpression : bitWiseAndOperator equalityExpression
								| bitWiseAndOperator equalityExpression tempBitWiseAndExpression'''
	generate_output(p.slice)


def p_bitWiseAndExpressionNoIn(p):
	'''bitWiseAndExpressionNoIn : equalityExpressionNoIn
							| equalityExpressionNoIn tempBitWiseAndExpressionNoIn'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


def p_tempBitWiseAndExpressionNoIn(p):
	'''tempBitWiseAndExpressionNoIn : bitWiseAndOperator equalityExpressionNoIn
								| bitWiseAndOperator equalityExpressionNoIn tempBitWiseAndExpressionNoIn'''
	generate_output(p.slice)


def p_bitWiseAndOperator(p):
	'''bitWiseAndOperator : BITWISE_AND'''
	generate_output(p.slice)


def p_equalityExpression(p):
	'''equalityExpression : relationalExpression
							 | relationalExpression tempEqualityExpression'''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] += p[1]["code"] + p[2]["code"]
		operator = p[2]["operator"]
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == "==":
			p[0]["code"] += [["ifgoto","beq",p[1]["place"],p[2]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "!=":
			p[0]["code"] += [["ifgoto","bne",p[1]["place"],p[2]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]	
		elif operator == "===":
			if p[1]["type"] != p[2]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","beq",p[1]["place"],p[2]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	
		elif operator == "!==":
			if p[1]["type"] == p[2]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","bne",p[1]["place"],p[2]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	

	generate_output(p.slice)


def p_equalityExpressionWithoutFunc(p):
	'''equalityExpressionWithoutFunc : relationalExpressionWithoutFunc
							 | relationalExpressionWithoutFunc tempEqualityExpression'''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] += p[1]["code"] + p[2]["code"]
		operator = p[2]["operator"]
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == "==":
			p[0]["code"] += [["ifgoto","beq",p[1]["place"],p[2]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "!=":
			p[0]["code"] += [["ifgoto","bne",p[1]["place"],p[2]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]	
		elif operator == "===":
			if p[1]["type"] != p[2]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","beq",p[1]["place"],p[2]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	
		elif operator == "!==":
			if p[1]["type"] == p[2]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","bne",p[1]["place"],p[2]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	

	generate_output(p.slice)


def p_tempEqualityExpression(p):
	'''tempEqualityExpression : equalityOperator relationalExpression
								| equalityOperator relationalExpression tempEqualityExpression'''
	p[0] = {}
	p[0]["operator"] = p[1]
	p[0]["code"] = []
	if len(p) == 3:
		p[0]["code"] += p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] += p[2]["code"] + p[3]["code"]
		operator = p[3]["operator"]
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == "==":
			p[0]["code"] += [["ifgoto","beq",p[2]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "!=":
			p[0]["code"] += [["ifgoto","bne",p[2]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]	
		elif operator == "===":
			if p[2]["type"] != p[3]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","beq",p[2]["place"],p[3]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	
		elif operator == "!==":
			if p[2]["type"] == p[3]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","bne",p[2]["place"],p[3]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	
	generate_output(p.slice)


def p_equalityExpressionNoIn(p):
	'''equalityExpressionNoIn : relationalExpressionNoIn
							| equalityExpressionNoIn OP_EQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_UNIVEQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_NOTEQUAL relationalExpressionNoIn
							| equalityExpressionNoIn OP_NOTUNIVEQUAL relationalExpressionNoIn'''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] += p[1]["code"] + p[3]["code"]
		operator = p[2]
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == "==":
			p[0]["code"] += [["ifgoto","beq",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "!=":
			p[0]["code"] += [["ifgoto","bne",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]	
		elif operator == "===":
			if p[1]["type"] != p[3]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","beq",p[1]["place"],p[3]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	
		elif operator == "!==":
			if p[1]["type"] == p[3]["type"]:
				p[0]["code"] += [["=",p[0]["place"],0]]
			else:
				p[0]["code"] += [["ifgoto","bne",p[1]["place"],p[3]["place"],"false"+label]]
				p[0]["code"] += [["=",p[0]["place"],1]]
				p[0]["code"] += [["goto","after"+label]]
				p[0]["code"] += [["label","false"+label]]
				p[0]["code"] += [["=",p[0]["place"],0]]
				p[0]["code"] += [["label","after"+label]]	
	generate_output(p.slice)


def p_equalityOperator(p):
	'''equalityOperator : OP_EQUAL
						| OP_UNIVEQUAL
						| OP_NOTEQUAL
						| OP_NOTUNIVEQUAL'''
	p[0] = p[1]
	generate_output(p.slice)

def p_relationalExpression(p):
	'''relationalExpression :  shiftExpression
							| relationalExpression OP_GREATER shiftExpression
							| relationalExpression OP_LESS shiftExpression
							| relationalExpression OP_GREATEREQUAL shiftExpression
							| relationalExpression OP_LESSEQUAL shiftExpression
							| relationalExpression INSTANCEOF shiftExpression
							| relationalExpression IN shiftExpression'''
	p[0] = {}
	p[0]["code"] = []
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[1]["code"] + p[3]["code"]
		operator = p[2]
		p[0]["place"] = tac.newTemp()
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == ">":
			p[0]["code"] += [["ifgoto","bgt",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "<":
			p[0]["code"] += [["ifgoto","blt",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == ">=":
			p[0]["code"] += [["ifgoto","bge",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "<=":
			p[0]["code"] += [["ifgoto","ble",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		
	generate_output(p.slice)


def p_relationalExpressionWithoutFunc(p):
	'''relationalExpressionWithoutFunc :  shiftExpressionWithoutFunc
							| relationalExpressionWithoutFunc OP_GREATER shiftExpression
							| relationalExpressionWithoutFunc OP_LESS shiftExpression
							| relationalExpressionWithoutFunc OP_GREATEREQUAL shiftExpression
							| relationalExpressionWithoutFunc OP_LESSEQUAL shiftExpression
							| relationalExpressionWithoutFunc INSTANCEOF shiftExpression
							| relationalExpressionWithoutFunc IN shiftExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[1]["code"] + p[3]["code"]
		operator = p[2]
		p[0]["place"] = tac.newTemp()
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == ">":
			p[0]["code"] += [["ifgoto","bgt",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "<":
			p[0]["code"] += [["ifgoto","blt",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == ">=":
			p[0]["code"] += [["ifgoto","bge",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "<=":
			p[0]["code"] += [["ifgoto","ble",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
	generate_output(p.slice)

def p_relationalExpressionNoIn(p):
	'''relationalExpressionNoIn : shiftExpression
							| relationalExpressionNoIn OP_GREATER shiftExpression
							| relationalExpressionNoIn OP_LESS shiftExpression
							| relationalExpressionNoIn OP_GREATEREQUAL shiftExpression
							| relationalExpressionNoIn OP_LESSEQUAL shiftExpression
							| relationalExpressionNoIn INSTANCEOF shiftExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[1]["code"] + p[3]["code"]
		operator = p[2]
		p[0]["place"] = tac.newTemp()
		p[0]["type"] = "boolean"
		label = tac.newLabel()
		if operator == ">":
			p[0]["code"] += [["ifgoto","bgt",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "<":
			p[0]["code"] += [["ifgoto","blt",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == ">=":
			p[0]["code"] += [["ifgoto","bge",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]
		elif operator == "<=":
			p[0]["code"] += [["ifgoto","ble",p[1]["place"],p[3]["place"],"false"+label]]
			p[0]["code"] += [["=",p[0]["place"],1]]
			p[0]["code"] += [["goto","after"+label]]
			p[0]["code"] += [["label","false"+label]]
			p[0]["code"] += [["=",p[0]["place"],0]]
			p[0]["code"] += [["label","after"+label]]	
	generate_output(p.slice)


def p_shiftExpression(p):
	'''shiftExpression : additiveExpression
						| additiveExpression tempShiftExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		operator = p[2]["operator"]
		p[0]["place"] = tac.newTemp()
		p[0]["type"] = "number"
		p[0]["code"] += [[operator,p[0]["place"],p[1]["place"],p[2]["place"]]]
	generate_output(p.slice)


def p_shiftExpressionWithoutFunc(p):
	'''shiftExpressionWithoutFunc : additiveExpressionWithoutFunc
						| additiveExpressionWithoutFunc tempShiftExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		operator = p[2]["operator"]
		p[0]["place"] = tac.newTemp()
		p[0]["type"] = "number"
		p[0]["code"] += [[operator,p[0]["place"],p[1]["place"],p[2]["place"]]]
	generate_output(p.slice)


def p_tempShiftExpression(p):
	'''tempShiftExpression : shiftOperator additiveExpression
							| shiftOperator additiveExpression tempShiftExpression'''
	p[0] = {}
	p[0]["operator"] = p[1]
	if len(p) == 3:
		p[0]["code"] = p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
	else:
		p[0]["code"] = p[2]["code"] + p[3]["code"]
		operator = p[3]["operator"]
		p[0]["place"] = tac.newTemp()
		p[0]["type"] = "number"
		p[0]["code"] += [[operator,p[0]["place"],p[2]["place"],p[3]["place"]]]
	generate_output(p.slice)



def p_shiftOperator(p):
	'''shiftOperator : OP_LSHIFT
					| OP_RSHIFT'''
	p[0] = p[1]
	generate_output(p.slice)


def p_additiveExpression(p):
	'''additiveExpression  : multiplicativeExpression
 							| multiplicativeExpression tempAdditiveExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		temptype = getHigherPrecedence(p[1]["type"],p[2]["type"])
		if temptype== "string":
			pass
		elif temptype == "number":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]
			p[0]["type"] = "number"
		elif temptype == "boolean":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]		
			p[0]["type"] = "number"
	generate_output(p.slice)


def p_additiveExpressionWithoutFunc(p):
	'''additiveExpressionWithoutFunc  : multiplicativeExpressionWithoutFunc
 							| multiplicativeExpressionWithoutFunc tempAdditiveExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		temptype = getHigherPrecedence(p[1]["type"],p[2]["type"])
		if temptype== "string":
			pass
		elif temptype == "number":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]
			p[0]["type"] = "number"
		elif temptype == "boolean":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]		
			p[0]["type"] = "number"

	generate_output(p.slice)


def p_tempAdditiveExpression(p):
	'''tempAdditiveExpression : additiveOperator multiplicativeExpression
								| additiveOperator multiplicativeExpression tempAdditiveExpression'''
	p[0] = {}
	if len(p) == 3:
		p[0]["code"] = p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
		p[0]["operator"] = p[1]["operator"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] = p[2]["code"] + p[3]["code"]
		p[0]["operator"] = p[1]["operator"]
		temptype = getHigherPrecedence(p[2]["type"],p[3]["type"])
		if temptype== "string":
			pass
		elif temptype == "number":
			p[0]["code"] += [[p[3]["operator"],p[0]["place"],p[2]["place"],p[3]["place"]]]
			p[0]["type"] = "number"
		elif temptype == "boolean":
			p[0]["code"] += [[p[3]["operator"],p[0]["place"],p[2]["place"],p[3]["place"]]]		
			p[0]["type"] = "number"
	generate_output(p.slice)


def p_multiplicativeExpressionWithoutFunc(p):
	'''multiplicativeExpressionWithoutFunc : unaryExpressionWithoutFunc
								| unaryExpressionWithoutFunc tempMultiplicativeExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		temptype = getHigherPrecedence(p[1]["type"],p[2]["type"])
		if temptype== "string":
			pass
		elif temptype == "number":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]
			p[0]["type"] = "number"
		elif temptype == "boolean":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]		
			p[0]["type"] = "number"

	generate_output(p.slice)


def p_multiplicativeExpression(p):
	'''multiplicativeExpression : unaryExpression
	 							| unaryExpression tempMultiplicativeExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		temptype = getHigherPrecedence(p[1]["type"],p[2]["type"])
		if temptype== "string":
			pass
		elif temptype == "number":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]
			p[0]["type"] = "number"
		elif temptype == "boolean":
			p[0]["code"] += [[p[2]["operator"],p[0]["place"],p[1]["place"],p[2]["place"]]]		
			p[0]["type"] = "number"
	generate_output(p.slice)


def p_tempMultiplicativeExpression(p):
	'''tempMultiplicativeExpression : multiplicativeOperator unaryExpression
									| multiplicativeOperator unaryExpression tempMultiplicativeExpression'''
	p[0] = {}
	if len(p) == 3:
		p[0]["code"] = p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
		p[0]["operator"] = p[1]["operator"]
	else:
		p[0]["place"] = tac.newTemp()
		p[0]["code"] = p[2]["code"] + p[3]["code"]
		p[0]["operator"] = p[1]["operator"]
		temptype = getHigherPrecedence(p[2]["type"],p[3]["type"])
		if temptype== "string":
			pass
		elif temptype == "number":
			p[0]["code"] += [[p[3]["operator"],p[0]["place"],p[2]["place"],p[3]["place"]]]
			p[0]["type"] = "number"
		elif temptype == "boolean":
			p[0]["code"] += [[p[3]["operator"],p[0]["place"],p[2]["place"],p[3]["place"]]]		
			p[0]["type"] = "number"
	generate_output(p.slice)


def p_multiplicativeOperator(p):
	'''multiplicativeOperator : OP_MULT
								| OP_MODULUS
								| OP_DIVIDE'''
	p[0]={}
	p[0]["operator"] = p[1]
	generate_output(p.slice)


def p_additiveOperator(p):
	'''additiveOperator : OP_PLUS
						| OP_MINUS'''
	p[0] = {}
	p[0]["operator"] = p[1]
	generate_output(p.slice)

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
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)


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
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)


def p_postFixExpression(p):
	'''postFixExpression :  leftHandSideExpression
							| leftHandSideExpression OP_INCREMENT
							| leftHandSideExpression OP_DECREMENT'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)


def p_postFixExpressionWithoutFunc(p):
	'''postFixExpressionWithoutFunc :  leftHandSideExpressionWithoutFunc
							| leftHandSideExpressionWithoutFunc OP_INCREMENT
							| leftHandSideExpressionWithoutFunc OP_DECREMENT'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)



def p_leftHandSideExpression(p):
	'''leftHandSideExpression : newExpression
								| callExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)

def p_leftHandSideExpressionWithoutFunc(p):
	'''leftHandSideExpressionWithoutFunc : newExpressionWithoutFunc
								| callExpressionWithoutFunc'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)

def p_newExpression(p):
	'''newExpression : memberExpression
						| NEW newExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)

def p_newExpressionWithoutFunc(p):
	'''newExpressionWithoutFunc : memberExpressionWithoutFunc
						| NEW newExpression'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)

def p_memberExpression(p):
	'''memberExpression : functionExpression
							| primaryExpression
							| memberExpression LSQUARE expression RSQUARE
							| memberExpression DOT IDENTIFIER
							| NEW memberExpression arguements '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = []
		p[0]["type"] = "undefined"
		if p[2] == ".":
			if p[1]["place"] != "console":
				raise_error("Error "+p[1]["place"]+" is unknown")
			elif p[3] == "log":
				p[0]["place"] = "print"
			else:
				p[0]["place"] = p[1]["place"]+"."+p[3]
				
			
	generate_output(p.slice)

def p_memberExpressionWithoutFunc(p):
	'''memberExpressionWithoutFunc : primaryExpressionWithoutFunc
							| memberExpressionWithoutFunc LSQUARE expression RSQUARE
							| memberExpressionWithoutFunc DOT IDENTIFIER
							| NEW memberExpression arguements '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = []
		p[0]["type"] = "undefined"
		if p[2] == ".":
			if p[1]["place"] != "console":
				raise_error("Error "+p[1]["place"]+" is unknown")
			elif p[3] == "log":
				p[0]["place"] = "print"
			else:
				p[0]["place"] = p[1]["place"]+"."+p[3]
	generate_output(p.slice)

def p_expression(p):
	'''expression : assignmentExpression
					| expression COMMA assignmentExpression '''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass

	generate_output(p.slice)

def p_expressionWithoutFunc(p):
	'''expressionWithoutFunc : assignmentExpressionWithoutFunc
					| expressionWithoutFunc COMMA assignmentExpression '''
	p[0] = {}
	p[0]["code"] = []
	print "expression without func",p[1]
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)

def p_expressionNoIn(p):
	'''expressionNoIn : assignmentExpressionNoIn
					| assignmentExpressionNoIn tempExpressionNoIn'''
	generate_output(p.slice)

def p_tempExpressionNoIn(p):
	'''tempExpressionNoIn : COMMA assignmentExpressionNoIn
						| COMMA assignmentExpressionNoIn tempExpressionNoIn'''
	generate_output(p.slice)

def p_primaryExpression(p):
	'''primaryExpression : THIS
						 | objectLiteral
						 | LPAREN expression RPAREN
						 | IDENTIFIER
						 | literal
						 | arrayLiteral '''
	p[0] = {}
	if len(p) == 2:
		if p[1] == "console":
			p[0]["code"]=[]
			p[0]["place"] = p[1]
			p[0]["type"] = "undefined"
		else:
			lists = p.slice
			lists = lists[1]
			if isinstance(lists,lex.LexToken):
				value = lists.value
				type = lists.type
				if type == "IDENTIFIER":
					ident = symbTab.lookup(value)
					if ident == None:
						raise_error("Error: Variable '"+value+"' used before assignment")
					else:
						p[0]["code"] = []
						p[0]["type"] = ident[0]["identifierType"]
						p[0]["place"] = value
				else:
					pass	
			else:
				p[0]["code"] = p[1]["code"]
				p[0]["place"] = p[1]["place"]
				p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
		
	# print p[0]
	generate_output(p.slice)

def p_primaryExpressionWithoutFunc(p):
	'''primaryExpressionWithoutFunc : THIS
						 | LPAREN expression RPAREN
						 | IDENTIFIER
						 | literal
						 | arrayLiteral '''
	p[0] = {}
	if len(p) == 2:
		if p[1] == "console":
			p[0]["code"]=[]
			p[0]["place"] = p[1]
			p[0]["type"] = "undefined"
		else:
			lists = p.slice
			lists = lists[1]
			if isinstance(lists,lex.LexToken):
				value = lists.value
				type = lists.type
				if type == "IDENTIFIER":
					ident = symbTab.lookup(value)
					if ident == None:
						raise_error("Error: Variable '"+value+"' used before assignment")
					else:
						p[0]["code"] = []
						p[0]["type"] = ident[0]["identifierType"]
						p[0]["place"] = value
				else:
					pass	
			else:
				p[0]["code"] = p[1]["code"]
				p[0]["place"] = p[1]["place"]
				p[0]["type"] = p[1]["type"]
	else:
		p[0]["code"] = p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
	generate_output(p.slice)


def p_literal(p):
	'''literal : NUMBER
				| EXPO_NUMBER
				| OCTAL_NUMBER
				| HEXADECIMAL
				| STRING
				| NULL
				| TRUE
				| FALSE'''
	p[0] = {}
	p[0]["place"] = tac.newTemp()
	p[0]["code"] = []
	p[0]["type"] = "undefined"
	lists = p.slice
	type = lists[1].type
	value = lists[1].value
	if type == "NUMBER":
		p[0]["code"] += [["=",p[0]["place"],float(value),""]]
		p[0]["type"] = "number"
	elif type == "TRUE":
		p[0]["code"] += [["=",p[0]["place"],1,""]]
		p[0]["type"] = "boolean"
	elif type == "FALSE":
		p[0]["code"] += [["=",p[0]["place"],0,""]]
		p[0]["type"] = "boolean"
	elif type == "EXPO_NUMBER":
		p[0]["code"] += [["=",p[0]["place"],float(value),""]]
		p[0]["type"] = "exponumber"
	elif type == "STRING":
		p[0]["code"] += [["=",p[0]["place"],str(value),""]]
		p[0]["type"] = "string"
	else:
		pass
	# print p[0]
	generate_output(p.slice)


def p_arrayLiteral(p):
	'''arrayLiteral : LSQUARE RSQUARE
					| LSQUARE elison RSQUARE
					| LSQUARE elementList RSQUARE
					| LSQUARE elementList COMMA elison RSQUARE
					| LSQUARE elementList COMMA RSQUARE'''
	generate_output(p.slice)

def p_elementList(p):
	'''elementList : elison assignmentExpression
					| assignmentExpression
					| elementList COMMA elison assignmentExpression
					| elementList COMMA assignmentExpression'''
	generate_output(p.slice)

def p_elison(p):
	'''elison : COMMA
				| elison COMMA'''
	generate_output(p.slice)

def p_objectLiteral(p):
	'''objectLiteral : OPEN_BRACE CLOSE_BRACE
					| OPEN_BRACE propertyNameAndValueList CLOSE_BRACE'''
	generate_output(p.slice)

def p_propertyNameAndValueList(p):
	'''propertyNameAndValueList : propertyNameAndValue
								| propertyNameAndValue COMMA propertyNameAndValueList'''
	generate_output(p.slice)

def p_propertyNameAndValue(p):
	'''propertyNameAndValue : propertyName COLON assignmentExpression'''
	generate_output(p.slice)


def p_propertyName(p):
	'''propertyName : IDENTIFIER
					| STRING
					| NUMBER'''
	generate_output(p.slice)

def p_functionExpression(p):
	'''functionExpression : FUNCTION LPAREN RPAREN functionBody
							| FUNCTION IDENTIFIER LPAREN RPAREN functionBody
							| FUNCTION IDENTIFIER LPAREN formalParameterList RPAREN functionBody
							| FUNCTION LPAREN formalParameterList RPAREN functionBody'''
	generate_output(p.slice)

def p_arguements(p):
	'''arguements : LPAREN RPAREN
				| LPAREN arguementList RPAREN'''
	p[0] = {}
	if len(p) == 3:
		p[0]["code"] = []
	else:
		p[0]["code"] = p[2]["code"]
		p[0]["place"] = p[2]["place"]
		p[0]["type"] = p[2]["type"]
	generate_output(p.slice)

def p_arguementList(p):
	'''arguementList : assignmentExpression
					| assignmentExpression COMMA arguementList'''
	p[0] = {}
	if len(p) == 2:
		p[0]["code"] = p[1]["code"]
		p[0]["place"] = p[1]["place"]
		p[0]["type"] = p[1]["type"]
	else:
		pass
	generate_output(p.slice)

def p_callExpression(p):
	'''callExpression : memberExpression arguements
						| callExpression empty empty empty arguements
						| callExpression LSQUARE expression RSQUARE
						| callExpression DOT IDENTIFIER'''
	p[0] = {}
	if len(p) == 3:
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		if p[1]["place"] == "print":
			p[0]["code"] += [["print_intv",p[2]["place"]]]		
			p[0]["place"] = p[1]["place"]
			p[0]["type"] = p[1]["type"]
	generate_output(p.slice)

def p_callExpressionWithoutFunc(p):
	'''callExpressionWithoutFunc : memberExpressionWithoutFunc arguements
						| callExpressionWithoutFunc empty empty empty arguements
						| callExpressionWithoutFunc LSQUARE expression RSQUARE
						| callExpressionWithoutFunc DOT IDENTIFIER'''
	p[0] = {}
	if len(p) == 3:
		p[0]["code"] = p[1]["code"] + p[2]["code"]
		if p[1]["place"] == "print":
			p[0]["code"] += [["print_intv",p[2]["place"]]]
			p[0]["place"] = p[1]["place"]
			p[0]["type"] = p[1]["type"]

	generate_output(p.slice)

def p_error(p):
	tok = lexer.token()
	if not tok:
		print "End of File"
		return
	else:
		print "Syntax error at line " + str(p.lineno)
		while True:		
			tok = lexer.token()
			if not tok or tok.type == 'SEMI_COLON': 
				break
		parser.restart()


parser = yacc.yacc()
if __name__ == "__main__":
	file_input = sys.argv[1]
	file_name = file_input.split("/")[2]
	file_x = file_name.split(".")[0]
	file_name = file_name.split(".")[0]+"_temp.html"
	f = open(file_name,'w')
	program = open(file_input).read()
	parsed_code = parser.parse(program,lexer = lexer,debug = False)
	f.close()
	call_s = "tac "+file_name+" > "+file_x+".html"
	print symbTab.symbol
	subprocess.call(call_s,shell = True)
	call_s = "rm "+file_name
	subprocess.call(call_s,shell = True)
