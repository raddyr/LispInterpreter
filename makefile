
all : run clean

rune: example clean

runt: tests clean

run:
	python main.py

example:
	python main.py example.txt

tests:
	python main.py test.txt

clean: 
	rm -f *.pyc parser.out parsetab.py *~
