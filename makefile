SHELL := /bin/bash

cmdPython := python3.12
venvDir := .venv
dataDir := .data
embeddingModelName := mxbai-embed-large
llmModelName := contextualized-assistant
modelFileName := contextualized_assistant.model
cmdVenvActivate := source $(venvDir)/bin/activate
cmdAppRun := $(cmdPython) -m streamlit run src/main.py

# Set the default target for the makefile.
default: run

# Clean the data folder.
clean:
	@if [ -d $(dataDir) ]; then rm -Rf $(dataDir); fi

# Perform first time setup.
setup: setup/model setup/model/embedding setup/env

# Configure the LLM model used by the application.
setup/model:
	-ollama rm $(llmModelName)
	ollama create $(llmModelName) -f $(modelFileName)

# Configure the embedding model used by the application.
setup/model/embedding:
	-ollama rm $(embeddingModelName)
	ollama pull $(embeddingModelName)

# Configure the virtual environment and dependencies.
setup/env:
	@( \
		if [ -d $(venvDir) ]; then rm -Rf $(venvDir); fi; \
		mkdir $(venvDir); \
		$(cmdPython) -m venv $(venvDir); \
		$(cmdVenvActivate); \
		pip install -e . 'llm-workbench[test]' --upgrade; \
    )

# Configure the fake server for API mocking.
setup/server:
	npm install

# Update dependencies.
setup/update:
	@( \
		$(cmdVenvActivate); \
		pip install --upgrade pip; \
		pip install -e . --upgrade; \
    )

# Start the application.
run:
	@( \
		$(cmdVenvActivate); \
		$(cmdAppRun); \
    )

# Start the fake server for API mocking.
run/server:
	npx json-server db.json

# Run tests.
test:
	@( \
		$(cmdVenvActivate); \
		$(cmdPython) -m pytest ./tests; \
    )