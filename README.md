# LLM Workbench

A RAG-enabled workbench to index files and chat with an LLM about their contents.

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

A page to load context files and interact with the LLM will open in your browser.

## Features

- One-shot prompts to LLM.
- File indexing for context querying.
- Prompt tools to assist with prompt construction and context gathering.
- Replaying of a set of prompts, either from the current prompt history or a text file.
- Displaying of all prompts and responses in the chat container.

## Prompt tools

Tools are used directly in the chat message input box.

| Tool                                        | Usage                             |
| ------------------------------------------- | --------------------------------- |
| `:<label>`                                  | Add a label to a prompt for later reference. Labels should contain only lowercase alphanumeric characters and hyphens. |
| `{response:last}`                           | Replaced by the last response in the chat history. |
| `{response:label:<label>}`                  | Replaced by the labeled response in the chat history. |
| `/context`                                  | Query chunks from uploaded files. |
| `/context:<number>`                         | Set the number of chunks to return. |
| `/context?file="<file name with extension>` | Query chunks only from the specified file. |
| `/get:<url>`                                | Perform a `GET` to an endpoint URL. |
| `/echo`                                     | Echo the prompt without sending it to the LLM. Can have replacements `{response*}` can be used for replacements. |

## Prompt construction

```text
:<label> /<tool> <prompt text, can contain {response:*} for replacement>
```

## API mocking

In case you want to use API mocking to test context retrieval from endpoints, it's possible to use the [JSON Server](https://github.com/typicode/json-server) package for mocking.

Having Node.js/NPM installed, run the the following command to install dependencies:

```bash
make setup/server
```

Add the JSON you want to use as mock data in the [db.json](db.json) file and run the server in a new terminal with the command below:

```bash
make run/server
```

The server will be accessible in [http://localhost:3000/](http://localhost:3000/), with the root nodes of the JSON file as URL paths (e.g. in the demo [db.json file](db.json)) there's a `data` root node, which can be accessible through [http://localhost:3000/data](http://localhost:3000/data).

## Known issues

1. The buttons in the screen are not always disabled during operations. Please be aware that clicking on different buttons during actions may lead to unintended consequences.
2. The download of chat history may not work during first attempt.
3. Complex Excel/.xlsx files may not be loadable due to format incompatibility with `openpyxl`.
4. During replay, the scrolling may not be automatic.
