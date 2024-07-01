"""Interactive chat application for LLMs.
"""

import logging
from typing import Dict
import uuid
from logging import getLogger

import streamlit as st

from config import (
    LOG_FORMAT,
    MODEL_NAME,
    OLLAMA_HOST,
    OLLAMA_REQUEST_TIMEOUT
)
from ui.component.base import OperationMode, OperationModeManager, UiComponent
from ui.component.chat import ChatComponent
from ui.component.context import ContextCompoonent
from ui.component.replay import ReplayComponent


logger = getLogger()

mode_manager = OperationModeManager(OperationMode.CHAT)
chat = ChatComponent(mode_manager)
context = ContextCompoonent(mode_manager)
replay = ReplayComponent(mode_manager, chat)

modes: Dict[OperationMode, UiComponent] = {
    OperationMode.CHAT: chat,
    OperationMode.REPLAY: replay
}


def config_logger():
    """Configure the logger output settings."""
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(ch)


def open_replay():
    """Start the replay mode."""
    replay.load_prompts_from_history()
    mode_manager.set_mode(OperationMode.REPLAY)


# Initial setup.
if 'id' not in st.session_state:
    config_logger()
    st.session_state.id = str(uuid.uuid4())

with st.sidebar:
    context.render()
    st.caption(f"Session {st.session_state.id}")

col_header, col_button1, col_button2 = st.columns(
    [6, 1, 1], vertical_alignment='bottom')

with col_header:
    st.header(
        'LLM Workbench',
        help="""
- Use `/context` to query context
- Add `{previous_response}` to append the previous response
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
        'Clear',
        help='Clean the chat history.',
        on_click=chat.clear_history
    )

current_mode = mode_manager.get_mode()
logger.info('m=render mode=%s', current_mode)
modes[current_mode].render()
