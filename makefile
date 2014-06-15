PROG = Szymanski

all : run clean

run:
	python main.py

rune: example clean

example:
	python main.py example.txt

clean: 
	rm -f *.pyc parser.out parsetab.py *~
