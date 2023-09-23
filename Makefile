# Install and cache poetry
.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

# Cache poetry dependencies
.PHONY: cache-poetry
cache-poetry:
	actions/cache@v3 \
		--path=$$HOME/.cache/pypoetry/virtualenvs \
		--key=${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }} \
		--restore-keys=${{ runner.os }}-poetry-

# Install dependencies with poetry
.PHONY: install-dependencies
install-dependencies:
	poetry install
	env POETRY_VIRTUALENVS_IN_PROJECT=true

# Lint with flake8
.PHONY: lint-flake8
lint-flake8:
	poetry run flake8 --ignore=E123,E126,E203,E402,E501,F401 .

# Lint with ruff
.PHONY: lint-ruff
lint-ruff:
	poetry run ruff --ignore=F401,F841,E402,E501,E999 .

# Cache mypy dependencies
.PHONY: cache-mypy
cache-mypy:
	actions/cache@v3 \
		--path=$$HOME/.cache/mypy \
		--key=${{ runner.os }}-mypy-${{ hashFiles('**/mypy.ini') }} \
		--restore-keys=${{ runner.os }}-mypy-

# Static type checks with mypy
.PHONY: static-type-checks
static-type-checks:
	poetry run mypy src/ --exclude '/site-packages/'

# Wily build and rank
.PHONY: wily-build-and-rank
wily-build-and-rank:
	poetry run wily build src
	poetry run wily rank src

# Lint YAML
.PHONY: lint-yaml
lint-yaml:
	ibiqlik/action-yamllint@v3 \
		--file_or_dir=. \
		--config_file=.yamllint.yml

# Spellcheck README
.PHONY: spellcheck-readme
spellcheck-readme:
	rojopolis/spellcheck-github-actions@0.33.1 \
		--config_path=config/.spellcheck.yml \
		--source_files=README.md \
		--task_name=Markdown

# Run unit tests and make coverage report
.PHONY: run-tests-and-coverage
run-tests-and-coverage:
	poetry run pytest --cov=./ --cov-report xml:cov.xml

# Upload coverage reports to Codecov
.PHONY: upload-coverage
upload-coverage:
	codecov/codecov-action@v3 \
		--files=./cov.xml \
		--verbose=true

# Qualify code target
.PHONY: qualify-code
qualify-code: install-poetry cache-poetry install-dependencies lint-flake8 lint-ruff \
	cache-mypy static-type-checks wily-build-and-rank lint-yaml spellcheck-readme run-tests-and-coverage upload-coverage
