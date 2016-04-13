all: parser.py ../test/test1.js
	python parser.py ../test/test1.js
	python codegen.py output.tac > a.out
clean: 
	rm -f *.pyc *.out parsetab.py *.png *.html *.dot *.txt
