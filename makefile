venvDir := .venv
dataDir := .data
embeddingModelName := nomic-embed-text
llmModelName := contextualized_assistant_llama3
modelFileName := contextualized_assistant.model
cmdVenvActivate := source $(venvDir)/bin/activate
cmdAppRun := python3 -m streamlit run src/main.py

# Set the default target for the makefile.
default: run

# Clean the data folder.
clean: 
	@if [ -d $(dataDir) ]; then rm -Rf $(dataDir); fi

# Perform first time setup.
setup: setup/model setup/env

# Configure the model used by the application.
setup/model:
	-ollama rm $(embeddingModelName)
	ollama pull $(embeddingModelName)

	-ollama rm $(llmModelName)
	ollama create $(llmModelName) -f $(modelFileName)

# Configure the virtual environment and dependencies.
setup/env:
	@( \
		if [ -d $(venvDir) ]; then rm -Rf $(venvDir); fi; \
		mkdir $(venvDir); \
		python3 -m venv $(venvDir); \
    	$(cmdVenvActivate); \
       	python3 -m pip install -e . --upgrade; \
    )

# Update dependencies.
setup/update:
	@( \
		python3 -m venv $(venvDir); \
       	python3 -m pip install -e . --upgrade; \
    )

# Start the application.
run:
	@( \
    	$(cmdVenvActivate); \
		$(cmdAppRun); \
    )