"""Interactive chat application for LLMs.
"""

import logging
import uuid
from logging import getLogger

import streamlit as st

from config import (
    LOG_FORMAT,
    MODEL_NAME,
    OLLAMA_HOST,
    OLLAMA_REQUEST_TIMEOUT
)
from ui.component.chat import ChatComponent
from ui.component.context import ContextCompoonent

logger = getLogger()


def config_logger():
    """Configure the logger output settings."""
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(ch)


# Initial setup.
if 'id' not in st.session_state:
    config_logger()
    st.session_state.id = str(uuid.uuid4())

chat = ChatComponent()
context = ContextCompoonent()

with st.sidebar:
    context.render_context()
    st.caption(f"Session {st.session_state.id}")

col_header, col_buttons = st.columns([6, 1], vertical_alignment='bottom')
with col_header:
    st.header(
        'LLM Workbench',
        help="""
- Use `/context` to query context
- Add `{previous_response}` to append the previous response
- Use `Ctrl + ENTER` for new line
              """
    )
with col_buttons:
    st.button('Clear', on_click=chat.clear_history)

chat.render_history()
chat.render_prompt()
