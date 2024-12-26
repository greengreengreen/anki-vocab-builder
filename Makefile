.PHONY: format lint test clean

format:
	black . --exclude "venv/"
	isort . --skip venv

lint: format
	flake8 . --exclude=venv
	mypy anki_vocab_builder --exclude venv

test:
	pytest tests/ -v --cov=anki_vocab_builder

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 