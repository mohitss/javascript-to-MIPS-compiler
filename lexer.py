import ply.lex as lex
import sys

class MyLexer(object):
	dictionary = {}
	# Tokens that we are going to use in javascript
	reserved={
		'abstract' : 'ABSTRACT',
		'arguments' : 'ARGUMENTS',
		'boolean' : 'BOOLEAN',
		'break' : 'BREAK',
		'byte' : 'BYTE',
		'case' : 'CASE',
		'catch' : 'CATCH',
		'char' : 'CHAR',
		'class' : 'CLASS',
		'const' : 'CONST',
		'continue' : 'CONTINUE',
		'debugger' : 'DEBUGGER',
		'default' : 'DEFAULT',
		'delete' : 'DELETE',
		'do' : 'DO',
		'double' : 'DOUBLE',
		'else' : 'ELSE',
		'enum' : 'ENUM',
		'eval' : 'EVAL',
		'export' : 'EXPORT',
		'extends' : 'EXTENDS',
		'false' : 'FALSE',
		'final' : 'FINAL',
		'finally' : 'FINALLY',
		'float' : 'FLOAT',
		'for' : 'FOR',
		'function' : 'FUNCTION',
		'goto' : 'GOTO',
		'if' : 'IF',
		'implements' : 'IMPLEMENTS',
		'import' : 'IMPORT',
		'in' : 'IN',
		'instanceof' : 'INSTANCEOF',
		'int' : 'INT',
		'interface' : 'INTERFACE',
		'let' : 'LET',
		'long' : 'LONG',
		'native' : 'NATIVE',
		'new' : 'NEW',
		'null' : 'NULL',
		'package' : 'PACKAGE',
		'private' : 'PRIVATE',
		'protected' : 'PROTECTED',
		'public' : 'PUBLIC',
		'return' : 'RETURN',
		'short' : 'SHORT',
		'static' : 'STATIC',
		'super' : 'SUPER',
		'switch' : 'SWITCH',
		'synchronized' : 'SYNCHRONIZED',
		'this' : 'THIS',
		'throw' : 'THROW',
		'throws' : 'THROWS',
		'transient' : 'TRANSIENT',
		'true' : 'TRUE',
		'try' : 'TRY',
		'typeof' : 'TYPEOF',
		'var' : 'VAR',
		'void' : 'VOID',
		'volatile' : 'VOLATILE',
		'while' : 'WHILE',
		'with' : 'WITH',
		'yield' : 'YIELD',

	}
	tokens = (
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
	   'OP_EXPO',		#"**"
	   'OP_LSHIFT',	  #"<<"
	   'OP_RSHIFT',	  #">>"
	   'OP_AND',		 #"&&"
	   'OP_OR',		  #"||"

	   ### Javascript Literals 
	   'NUMBER',
	   'STRING',
	   'BOOL',
	   'ARRAY',
	   'OBJECT', 

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
	   'NEWLINE',
	   'EXPO_NUMBER',
	   'OCTAL_NUMBER',
	   'HEXADECIMAL',
	)
	tokens = list(tokens) + list(reserved.values())

	for token in tokens:
		dictionary[token] = [0,set([])]

	t_ignore=' \t'
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
	t_OP_EXPO		=	r'\*\*'
	t_OP_LSHIFT		=	r'<<'
	t_OP_RSHIFT		=	r'>>'
	t_OP_AND		=	r'&&'
	t_OP_OR		=	r'\|\|'
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
	t_NEWLINE	=	r'\n+'
	def t_COMMENT(self,t):
		r'(\/\*[\w\'\s\r\n\*]*\*\/)|(\/\/.*\n)|(\<![\-\-\s\w\>\/]*\>)'
		pass

	def t_IDENTIFIER(self,t):
		r'[a-zA-Z_][a-zA-Z_0-9]*'
		t.type = self.reserved.get(t.value,'IDENTIFIER')	# Check for reserved words
		return t


	def t_error(self,t):
		print("Illegal character '%s'" % t.value[0])
		t.lexer.skip(1)

	def t_NUMBER(self,t):           
		r'([1-9][0-9]*(\.[0-9]+)?)|0+'
		return t

	def t_EXPO_NUMBER(self,t):
		r'[1-9][0-9]*(\.[0-9]+)?e[+|-]?[0-9]+(\.[0-9]+)?'
		return t

	def t_OCTAL_NUMBER(self,t):
		r'0[0-7]+'
		return t

	def t_HEXADECIMAL(self,t):
		r'0[x|X][0-9a-fA-F]*'
		return t

	def t_STRING(self,t):
		r'(\'[^\']*\')|(\"[^\"]*\")'
		return t

	def build(self,**kwargs):	
		self.lexer = lex.lex(module=self, **kwargs)
	

	# Test it output
	def test(self,data):
		self.lexer.input(data)
		while True:
			 tok = self.lexer.token()
			 if not tok: 
				 break
			 # print(tok)
			 self.dictionary[tok.type][0] += 1
			 self.dictionary[tok.type][1] |= {tok.value} 
		for keys,values in self.dictionary.iteritems():
			if values[0]:
				print keys,self.dictionary[keys]

# Build the lexer and try it out

if __name__ == "__main__":
	m = MyLexer()
	m.build()
	file_name = sys.argv[1]		   # Build the lexer
	try:
		myfile = open(file_name,'r').read()
		m.test(myfile)
	except:
		print "Error"
	
