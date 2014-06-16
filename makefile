
all : run clean

rune: example clean

run:
	python main.py

example:
	python main.py example.txt

clean: 
	rm -f *.pyc parser.out parsetab.py *~
