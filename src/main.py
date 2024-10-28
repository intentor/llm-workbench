"""Interactive chat application for LLMs.
"""

import logging
import uuid
from logging import getLogger

import streamlit as st
import ollama

from config import get_settings
from core.prompting.base import PromptExecutor
from core.prompting.generator.model import ModelResponseGenerator
from core.prompting.indexer import ContextIndexer
from core.prompting.generator.context import ContextResponseGenerator
from core.prompting.generator.echo import EchoResponseGenerator
from core.prompting.generator.endpoint import EndpointResponseGenerator
from core.prompting.generator.rag import RagResponseGenerator
from core.prompting.generator.template import TemplateResponseGenerator
from core.prompting.history import PromptHistory
from core.prompting.provider.ollama import OllamaModelProvider
from core.prompting.provider.openrouter import OpenRouterModelProvider
from ui.component.base import OperationMode, OperationModeManager, UiComponent
from ui.component.chat import ChatComponent
from ui.component.context import ContextCompoonent
from ui.component.replay import ReplayComponent

logger = getLogger()
settings = get_settings()

# Initial setup.
if 'id' not in st.session_state:
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(settings.log_format))
        logger.addHandler(ch)
    st.session_state.id = str(uuid.uuid4())
    st.session_state.history = PromptHistory()

ollama_client = ollama.Client(
    host=settings.ollama_host,
    timeout=settings.ollama_request_timeout
)
indexer = ContextIndexer(
    ollama_client,
    settings.vector_db_path,
    st.session_state.id,
    settings.model_embeddings
)
context_generator = ContextResponseGenerator(
    st.session_state.history,
    indexer
)

if settings.model_provider == 'OPENROUTER':
    model_provider = OpenRouterModelProvider(
        settings.open_router_host,
        settings.open_router_key,
        settings.open_router_request_timeout,
        settings.open_router_model
    )
else:
    model_provider = OllamaModelProvider(
        ollama_client,
        settings.ollama_model
    )

model_generator = ModelResponseGenerator(
    st.session_state.history,
    model_provider
)

prompt_executor = PromptExecutor(
    [
        model_generator,
        context_generator,
        RagResponseGenerator(
            st.session_state.history,
            model_generator,
            context_generator
        ),
        EndpointResponseGenerator(
            st.session_state.history
        ),
        EchoResponseGenerator(
            st.session_state.history
        ),
        TemplateResponseGenerator(
            st.session_state.history
        )
    ]
)

mode_manager = OperationModeManager(OperationMode.CHAT)
chat = ChatComponent(
    mode_manager,
    prompt_executor,
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


@st.dialog('Save chat history')
def save_chat_history(history: str):
    st.download_button(
        label='Save as text',
        help='Download contents as text.',
        data=history,
        file_name='chat.txt',
        mime='text/plain',
    )

    st.download_button(
        label='Save as HTML',
        help='Download contents as HTML.',
        data=history,
        file_name='chat.html',
        mime='text/html',
    )


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
    st.button(
        label='Save all',
        help='Download the chat history.',
        on_click=save_chat_history,
        args=(str(st.session_state.history),)
    )

with col_button3:
    st.button(
        label='Save last',
        help='Download the last chat history message',
        on_click=save_chat_history,
        args=(st.session_state.history.get_last_response(),)
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
