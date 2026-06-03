PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src

.PHONY: demo lesson00 lesson01 lesson05 lesson06 lessons test compile lint linkcheck notebookcheck check tree

demo:
	$(PYTHON) -m quant_learning.run_demo

lesson00:
	$(PYTHON) -m quant_learning.lessons 00

lesson01:
	$(PYTHON) -m quant_learning.lessons 01

lesson05:
	$(PYTHON) -m quant_learning.lessons 05

lesson06:
	$(PYTHON) -m quant_learning.lessons 06

lessons: lesson00 lesson01 lesson05 lesson06

test:
	$(PYTHON) -m unittest discover -s tests

compile:
	$(PYTHON) -m compileall -q src tests

lint:
	$(PYTHON) scripts/run_ruff.py

linkcheck:
	$(PYTHON) scripts/check_markdown_links.py

notebookcheck:
	$(PYTHON) scripts/check_notebook_boundaries.py

check: compile lint test linkcheck notebookcheck

tree:
	find . -maxdepth 3 -not -path './.git*' | sort
