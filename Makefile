PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src

.PHONY: demo test compile check tree

demo:
	$(PYTHON) -m quant_learning.run_demo

lesson00:
	$(PYTHON) -m quant_learning.lessons 00

lesson01:
	$(PYTHON) -m quant_learning.lessons 01

lessons: lesson00 lesson01

test:
	$(PYTHON) -m unittest discover -s tests

compile:
	$(PYTHON) -m compileall -q src tests

check: compile test

tree:
	find . -maxdepth 3 -not -path './.git*' | sort
