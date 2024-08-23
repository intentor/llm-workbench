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

## Using the app

In the app page, you can:

1. Upload and index context files.
    - You can use set chunk size and overlap during uploading.
2. Use a prompt to retrive context from indexed files by starting it with `/context`.
    - You can use a number after `/context` to set the maximum number of context entries to return, e.g. `/context:2` will return at most 2 context entries.
    - You can use `?file="<full file name with extension>"` to filter the context only to a specific file, e.g. `/context?file="my file.pdf"` will perform the query only on chunks of `my file.pdf`.
3. Use a prompt to retrieve the response from an endpoint by using `/get:<url>`, e.g. `/get:http://localhost:3000/data/1`.
4. Use a prompt so the LLM can generate a response. The last response (which can e.g. be a context response) can be sent by adding the key `{response:last}` into the prompt.
5. Add labels to prompts so their responses can be referenced with `{response:label:<label>}`.
    - Add labels by starting a prompt with `:<label>`.
    - Labels should contain only lowercase alphanumeric characters and hyphens. E.g. `:label1` and`:my-label` are valid labels, but `:Label1` and `:My_Label` are not.
6. Replay a set of user prompts, either from the current prompt history or a text file.

All prompts and responses are displayed in the chat container in the page.

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
