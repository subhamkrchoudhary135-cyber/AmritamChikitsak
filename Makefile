.PHONY: pipeline ingest clean-data validate features split fairness reports drift test lint

PYTHON := .venv/Scripts/python.exe

pipeline:
	$(PYTHON) -m src.data.pipeline --stage all

ingest:
	$(PYTHON) -m src.data.pipeline --stage ingest

clean-data:
	$(PYTHON) -m src.data.pipeline --stage clean

validate:
	$(PYTHON) -m src.data.pipeline --stage validate

features:
	$(PYTHON) -m src.data.pipeline --stage features

split:
	$(PYTHON) -m src.data.pipeline --stage split

fairness:
	$(PYTHON) -m src.data.pipeline --stage fairness

reports:
	$(PYTHON) -m src.data.pipeline --stage reports

drift:
	$(PYTHON) -m src.data.pipeline --stage drift

test:
	$(PYTHON) -m pytest tests/test_data_pipeline.py -v --cov=src.data --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check src/data
