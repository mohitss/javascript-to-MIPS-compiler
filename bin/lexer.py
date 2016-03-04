import ply.lex as lex
import sys

dictionary = {}
# Tokens that we are going to use in javascript
reserved={
	'break' : 'BREAK',
	'case' : 'CASE',
	'catch' : 'CATCH',
	'continue' : 'CONTINUE',
	'default' : 'DEFAULT',
	'delete' : 'DELETE',
	'do' : 'DO',
	'else' : 'ELSE',
	'false' : 'FALSE',	
	'finally' : 'FINALLY',
	'for' : 'FOR',
	'function' : 'FUNCTION',
	'if' : 'IF',
	'in' : 'IN',
	'instanceof' : 'INSTANCEOF',
	'new' : 'NEW',
	'null' : 'NULL',
	'return' : 'RETURN',
	'switch' : 'SWITCH',
	'this' : 'THIS',
	'throw' : 'THROW',
	'true' : 'TRUE',
	'try' : 'TRY',
	'typeof' : 'TYPEOF',
	'var' : 'VAR',
	'void' : 'VOID',
	'while' : 'WHILE',
	'with' : 'WITH'
}
tokens_l = (
   "IDENTIFIER",

   ### arithmetic operators
   'OP_PLUS',
   'OP_MINUS',
   'OP_MULT',
   'OP_DIVIDE',
   'OP_MODULUS',
   'OP_INCREMENT',   # "++"
   'OP_DECREMENT',	# "--"
   'OP_ASSIGNMENT',   #"="
   'OP_PLUSEQUAL',   #"+="
   'OP_MINUSEQUAL',   #"-="
   'OP_MULTEQUAL',   #"*="
   'OP_DIVEQUAL',   #"/="
   'OP_MODEQUAL',   #"%="
   'OP_EQUAL',	  #"=="
   'OP_UNIVEQUAL',  #"==="
   'OP_NOTEQUAL',   #"!="
   'OP_NOTUNIVEQUAL',  #"!=="
   'OP_GREATER',   #">"
   'OP_LESS',   #"<"
   'OP_GREATEREQUAL',   #">="
   'OP_LESSEQUAL',   #"<="
   'OP_TERNARY',	 #"?aa"
   'OP_NOT',		 #"!"
   # 'OP_EXPO',		#"**"
   'OP_LSHIFT',	  #"<<"
   'OP_RSHIFT',	  #">>"
   'OP_AND',		 #"&&"
   'OP_OR',		  #"||"

   ### Javascript Literals 
   'NUMBER',
   'STRING',
   # 'BOOL',
   # 'ARRAY',
   # 'OBJECT', 

   ###	BRACKETS
   'LPAREN',
   'RPAREN',
   'OPEN_BRACE',	#"{"
   'CLOSE_BRACE',   #"}"
   'LSQUARE',	   #"["
   'RSQUARE',	   #"]"

   ### MISC
   'COMMA',
   'COLON',
   'SEMI_COLON',
   'DOT',   
   'COMMENT',
   # 'NEWLINE',
   'EXPO_NUMBER',
   'OCTAL_NUMBER',
   'HEXADECIMAL',

   ###BITWISE OPERATORS
   'BITWISE_AND',
   'BITWISE_OR',
   'BITWISE_NOT',
   'BITWISE_XOR',
)
tokens = list(tokens_l) + list(reserved.values())

for token in tokens:
	dictionary[token] = [0,set([])]

def t_ignore_COMMENT(t):
	r'(\/\*[\w\'\s\r\n\*]*\*\/)|(\/\/.*\n)|(\<![\-\-\s\w\>\/]*\>)'
	pass

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

t_ignore_WHITESPACE = r"\s"

t_OP_PLUS		=	r'\+'
t_OP_MINUS		=	r'-'
t_OP_MULT		=	r'\*'
t_OP_DIVIDE		=	r'/'
t_OP_MODULUS		=	r'%'
t_OP_INCREMENT		=	r'\+\+'
t_OP_DECREMENT		=	r'--'
t_OP_ASSIGNMENT		=	r'='
t_OP_PLUSEQUAL		=	r'\+='
t_OP_MINUSEQUAL		=	r'\-='
t_OP_MULTEQUAL		=	r'\*='
t_OP_DIVEQUAL		=	r'/='
t_OP_MODEQUAL		=	r'%='
t_OP_EQUAL		=	r'=='
t_OP_UNIVEQUAL		=	r'==='
t_OP_NOTEQUAL		=	r'!='
t_OP_NOTUNIVEQUAL		=	r'!=='
t_OP_GREATER		=	r'>'
t_OP_LESS		=	r'<'
t_OP_GREATEREQUAL		=	r'>='
t_OP_LESSEQUAL		=	r'<='
t_OP_TERNARY		=	r'\?'
t_OP_NOT		=	r'!'
# t_OP_EXPO		=	r'\*\*'
t_OP_LSHIFT		=	r'<<'
t_OP_RSHIFT		=	r'>>'
t_OP_AND		=	r'&&'
t_OP_OR		=	r'\|\|'

t_BITWISE_AND = r'&'
t_BITWISE_OR = r'\|'
t_BITWISE_NOT = r'~'
t_BITWISE_XOR = r'\^'



t_LPAREN	=	r'\('
t_RPAREN	= 	r'\)'

t_OPEN_BRACE	=	r'{'
t_CLOSE_BRACE	=   r'}'
t_LSQUARE		=	   r'\['
t_RSQUARE		=	   r'\]'
t_COMMA		=	r','
t_COLON     =	r':'
t_SEMI_COLON	=	r';'
t_DOT       =	r'\.'   



def t_IDENTIFIER(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'IDENTIFIER')	# Check for reserved words
	return t

def t_NUMBER(t):           
	r'([1-9][0-9]*(\.[0-9]+)?)|0+'
	return t

def t_EXPO_NUMBER(t):
	r'[1-9][0-9]*(\.[0-9]+)?e[+|-]?[0-9]+(\.[0-9]+)?'
	return t

def t_OCTAL_NUMBER(t):
	r'0[0-7]+'
	return t

def t_HEXADECIMAL(t):
	r'0[x|X][0-9a-fA-F]*'
	return t

def t_STRING(t):
	r'(\'[^\']*\')|(\"[^\"]*\")'
	return t

def t_error(t):
	print("Illegal characte is'%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()



# Test it output
def test(data):
	lexer.input(data)
	while True:
		tok = lexer.token()
		if not tok: 
			break
		dictionary[tok.type][0] += 1
		dictionary[tok.type][1] |= {tok.value} 
	for keys,values in dictionary.iteritems():
		if values[0]:
			print keys,dictionary[keys]

# Build the lexer and try it out

# temp = MyLexer()
# temp.build()
# lexer = temp.lexer
# tokens = temp.tokens

if __name__ == "__main__":
	file_name = sys.argv[1]		   # Build the lexer
	myfile = open(file_name,'r').read()
	test(myfile)
	
