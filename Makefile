POETRY=poetry
POETRY_RUN=$(POETRY) run

SOURCE_FILES=$(shell find . -path "./tafver_metars/*.py")
TEST_FILES=$(shell find . -path "./tests/*.py")
SOURCES_FOLDER=tafver_metars
TESTS_FOLDER=tests

BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

check_no_main:
ifeq ($(BRANCH),main)
	echo "You are good to go!"
else
	$(error You are not in the main branch)
endif

patch: check_no_main
	$(POETRY_RUN) bumpversion patch --verbose
	git push --follow-tags

minor: check_no_main
	$(POETRY_RUN) bumpversion minor --verbose
	git push --follow-tags

major: check_no_main
	$(POETRY_RUN) bumpversion major --verbose
	git push --follow-tags

style:
	$(POETRY_RUN) isort $(SOURCES_FOLDER)
	$(POETRY_RUN) isort $(TESTS_FOLDER)
	$(POETRY_RUN) black $(SOURCE_FILES)
	$(POETRY_RUN) black $(TEST_FILES)

lint:
	$(POETRY_RUN) isort $(SOURCES_FOLDER) --check-only
	$(POETRY_RUN) isort $(TESTS_FOLDER) --check-only
	$(POETRY_RUN) black $(SOURCE_FILES) --check
	$(POETRY_RUN) black $(TEST_FILES) --check

tests:
	PYTHONPATH=. $(POETRY_RUN) pytest -vv test