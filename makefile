PROG = Szymanski

all : run clean

run:
	python main.py

clean: 
	rm -f *.pyc parser.out parsetab.py *~
