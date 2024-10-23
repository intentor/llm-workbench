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
- Prompt tools to assist with prompt construction, context gathering, and response generation.
- Replaying of a set of prompts, either from the current prompt history or a text file.
- Displaying of all prompts and responses in the chat container.
- Download of all or only the last chat messages in text or HTML files.

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
| `/template`                                 | Get the last response as JSON and apply it to a [Jinja based template](https://jinja.palletsprojects.com/en/3.1.x/templates/), allowing the custom formatting of response without relying on the LLM. The JSON data is available in the `context` variable. Refer to the **Template usage** section for details. |

## Prompt construction

```text
:<label> /<tool> <prompt text, can contain {response:*} for replacement>
```

## Template usage

Given a previous JSON response, it's possible to use the `/template` tool to create a template that will be processed using the JSON data.

Using the following JSON as the last response in the prompt history:

```json
{
    "name": "User"
}
```

The prompt below will generate a response using the JSON as input data in the `context` variable:

```text
/template Name: {{context.name}}
```

The response to the prompt will be:

```text
Name: User
```

### Quick Cheat Sheet

#### Setting a variable

```text
{% set variable_name = context %}
```

#### Date/time format (from ISO 8601)

```text
{{context.field_date|parse_date|format_date("%d/%m/%y %H:%M:%S")}}
```

#### Conditional

```text
{% if context.field_boolean %}
Value if True
{% else %}
Value if False
{% endif %})
```

#### Loop

```text
 {% for item in context.list %}
 {{item.field}}
 {% endfor %}
```

#### Documentation

Please refer to [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) and [jinja2_iso8601](https://pypi.org/project/jinja2_iso8601/1.0.0/#description) documentations for more details on templating.

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

## Changing the model

By default, the workbench uses the LLM model [Llama3.1](https://ollama.com/library/llama3.1).

To change the LLM model used by the workbench, update the `FROM` parameter in [contextualized_assistant.model](contextualized_assistant.model) file by a model available in the [Ollama library](https://ollama.com/library).

## Using OpenRouter for generation

It's possible to use [OpenRuter](https://openrouter.ai) for requesting LLM generation from prompts, which replaces the default Ollama generator.

To setup OpenRouter, update the [config.py](./src/config.py) settings below:

- `OPEN_ROUTER_KEY`: Enter your [OpenRouter API key](https://openrouter.ai/docs/api-keys).
- `MODEL_GENERATOR`: Change to `OPENROUTER`.
- `MODEL_LLM`: Enter the model name from OpenRouter.

> [!NOTE]  
> The embebbding model still requires Ollama.

## Known issues

1. The buttons in the screen are not always disabled during operations. Please be aware that clicking on different buttons during actions may lead to unintended consequences.
2. The download of chat history may not work during first attempt.
3. Complex Excel/.xlsx files may not be loadable due to format incompatibility with `openpyxl`.
4. During replay, the scrolling may not be automatic.
