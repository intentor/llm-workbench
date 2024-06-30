venvDir := .venv
modelName := contextualized_assistant_llama3
modelFileName := contextualized_assistant.model
cmdVenvActivate := source $(venvDir)/bin/activate
cmdAppRun := python3 -m streamlit run src/main.py

# Set the default target for the makefile.
default: run

# Perform first time setup.
setup: setup/model setup/env

# Configure the model used by the application.
setup/model:
	-ollama rm $(modelName)
	ollama create $(modelName) -f $(modelFileName)

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