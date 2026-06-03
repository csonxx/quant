PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src

.PHONY: demo lesson00 lesson01 lessons test compile linkcheck notebookcheck check tree

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

linkcheck:
	$(PYTHON) scripts/check_markdown_links.py

notebookcheck:
	$(PYTHON) scripts/check_notebook_boundaries.py

check: compile test linkcheck notebookcheck

tree:
	find . -maxdepth 3 -not -path './.git*' | sort
