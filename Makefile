# Command variables
MANAGE_CMD = /usr/bin/env python manage.py
PIP_INSTALL_CMD = /usr/bin/env pip install --exists-action=w

# Helper functions to display messagse
ECHO_BLUE = @echo "\033[33;34m $1\033[0m"
ECHO_RED = @echo "\033[33;31m $1\033[0m"

# The default server host local development
HOST ?= 0:8002

# By default, run all test cases in the expo_services test directory,
# however if $TESTS are defined, only run those
TEST_CASES := {{ project_name }}
ifdef TESTS
	TEST_CASES := $(TESTS)
endif

# The default branch to deploy
BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)


clean :
# Remove all *.pyc, .DS_Store and temp files from the project
	$(call ECHO_BLUE,removing .pyc files...)
	@find . -name '*.pyc' -exec rm -f {} \;
	$(call ECHO_BLUE,removing static files...)
	@rm -rf {{ project_name }}/_static/
	$(call ECHO_BLUE,removing temp files...)
	@rm -rf {{ project_name }}/_tmp/
	$(call ECHO_BLUE,removing .DS_Store files...)
	@find . -name '.DS_Store' -exec rm {} \;

develop :
# Set up the project for development
	$(PIP_INSTALL_CMD) -r requirements/development.txt
	$(PIP_INSTALL_CMD) -r requirements/testing.txt
	$(MANAGE_CMD) migrate --noinput

test :
# Run the test cases
	$(MANAGE_CMD) test --settings={{ project_name }}.settings.testing $(TEST_CASES)

server :
# Run a local web server
	$(MANAGE_CMD) migrate
	$(MANAGE_CMD) runserver_plus $(HOST)

shell :
# Run a local shell for debugging
	$(MANAGE_CMD) migrate
	$(MANAGE_CMD) shell_plus
