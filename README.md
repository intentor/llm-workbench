# LLM Workbench

A RAG-enabled workbench to index files and chat with an LLM.

## How it works

![image](doc/app_flow.drawio.png)

## Setup

Download and install [Ollama](https://www.ollama.com), a framework to interact with LLMs.

After installation, run Ollama:

```bash
ollama serve
```

In order to configure the model and the application, in a new terminal, run:

```bash
make setup
```

## Running the app

```bash
make
```

A chat page to load context files and interact with the LLM will open in your browser.
