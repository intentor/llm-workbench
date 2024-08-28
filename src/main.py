"""Interactive chat application for LLMs.
"""

import logging
import uuid
from logging import getLogger

import streamlit as st
import ollama

from config import (
    LOG_FORMAT,
    MODEL_EMBEDDINGS,
    MODEL_LLM,
    OLLAMA_HOST,
    OLLAMA_REQUEST_TIMEOUT,
    VECTOR_DB_PATH
)
from core.indexer import ContextIndexer
from core.generator import (
    ContextResponseGenerator,
    EchoResponseGenerator,
    EndpointResponseGenerator,
    OllamaResponseGenerator,
    PromptTypeResponseGenerator,
    TemplateResponseGenerator
)
from core.prompt import PromptHistory, PromptType
from ui.component.base import OperationMode, OperationModeManager, UiComponent
from ui.component.chat import ChatComponent
from ui.component.context import ContextCompoonent
from ui.component.replay import ReplayComponent

logger = getLogger()

# Initial setup.
if 'id' not in st.session_state:
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(ch)
    st.session_state.id = str(uuid.uuid4())
    st.session_state.history = PromptHistory()

ollama = ollama.Client(
    host=OLLAMA_HOST,
    timeout=OLLAMA_REQUEST_TIMEOUT
)
indexer = ContextIndexer(
    ollama,
    VECTOR_DB_PATH,
    st.session_state.id,
    MODEL_EMBEDDINGS
)
generator = PromptTypeResponseGenerator(
    {
        PromptType.GENERATE: OllamaResponseGenerator(
            st.session_state.history,
            ollama,
            MODEL_LLM
        ),
        PromptType.CONTEXT: ContextResponseGenerator(
            st.session_state.history,
            indexer
        ),
        PromptType.ENDPOINT: EndpointResponseGenerator(
            st.session_state.history
        ),
        PromptType.ECHO: EchoResponseGenerator(
            st.session_state.history
        ),
        PromptType.TEMPLATE: TemplateResponseGenerator(
            st.session_state.history
        )
    }
)

mode_manager = OperationModeManager(OperationMode.CHAT)
chat = ChatComponent(
    mode_manager,
    generator,
    st.session_state.history
)
context = ContextCompoonent(
    mode_manager,
    indexer
)
replay = ReplayComponent(
    mode_manager,
    st.session_state.history,
    chat
)

modes: dict[OperationMode, UiComponent] = {
    OperationMode.CHAT: chat,
    OperationMode.REPLAY: replay
}


def open_replay():
    """Start the replay mode."""
    replay.load_prompts_from_history()
    mode_manager.set_mode(OperationMode.REPLAY)


with st.sidebar:
    context.render()
    st.caption(f"Session {st.session_state.id}")

col_header, col_button1, col_button2, col_button3, col_button4 = st.columns(
    [3, 0.8, 0.86, 0.9, 0.8], vertical_alignment='bottom')

with col_header:
    st.header(
        'LLM Workbench',
        help="""
- Use `/context` to query context returning up to 4 entries.
- Use `/context:<number>` to query context specifying the number of entries to return (e.g. `/context:2` will return up to to 2 entries).
- Use `/context?file="<full file name with extension>"` to query context for a specific file (e.g. `/context?file="my file.pdf"` will perform the query only on chunks of `my file.pdf`).
0 Use `/get:<url>` to retrieve the response from and endpoint (e.g. `/get:http://localhost:3000/data/1`)
- Start a prompt with `:<label>` to add a label, so its response can be referenced in subsequent prompts.
- Add `{response:last}` to append the last response.
- Add `{response:label:<label>}` to append a previous labeled response.
- Use `Ctrl + ENTER` for new line
"""
    )

with col_button1:
    st.button(
        'Replay',
        help='Perform running of a set of user prompts from history or a file.',
        on_click=open_replay
    )

with col_button2:
    st.download_button(
        label='Save all',
        help='Download the chat history as a text file.',
        data=st.session_state.history.get_as_string(),
        file_name="chat.txt",
        mime="text/plain",
    )

with col_button3:
    st.download_button(
        label='Save last',
        help='Download the last chat history message as a text file.',
        data=st.session_state.history.get_last_response(),
        file_name="chat.txt",
        mime="text/plain",
    )

with col_button4:
    st.button(
        'Clear',
        help='Clean the chat history.',
        on_click=chat.clear_history
    )

current_mode = mode_manager.get_mode()
logger.info('m=render mode=%s', current_mode)
modes[current_mode].render()
