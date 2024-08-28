"""Chat management components module.

Sessions:
    - messages: Chat message history. 
    - replay: User prompts to replay.
"""

import gc
import time
from logging import getLogger

import streamlit as st

from core.generator import ResponseGenerator
from core.prompt import Prompt, PromptHistory
from ui.component.base import OperationModeManager, UiComponent

CHAT_CSS = """
<style>
    .st-emotion-cache-183lzff {
        white-space: pre-wrap !important;
    }
</style>
"""
ROLE_BOT = 'assistant'
ROLE_USER = 'user'

logger = getLogger()


class ChatComponent(UiComponent):
    """Manages chat messages."""

    def __init__(
            self,
            mode_manager: OperationModeManager,
            generator: ResponseGenerator,
            history: PromptHistory):
        super().__init__(mode_manager)
        self._generator = generator
        self._history = history
        if 'replay' not in st.session_state:
            self._reset_replay()

    def render(self):
        self._render_history()

        st.markdown(CHAT_CSS, unsafe_allow_html=True)

        start = time.time()

        if self._has_replay():
            self._render_replay()
        else:
            self._render_input()

        end = time.time()
        execution_time = end - start
        st.text(f"Execution time: {execution_time:,.2f}s")
        logger.info('m=render elapsed=%d', end - start)

    def replay(self, prompts: list[str]):
        """Replay a list of prompts.

        Args:
            - prompts: Prompts to be sent to the core.
        """
        self.clear_history()
        st.session_state.replay = prompts

    def download_history(self):
        """Download all chat messages."""

    def clear_history(self):
        """Clear all chat messages."""
        self._history.clear()
        gc.collect()

    def _reset_replay(self):
        st.session_state.replay = []

    def _has_replay(self) -> bool:
        return len(st.session_state.replay) > 0

    def _render_message(self, role: str, message: str):
        with st.chat_message(role):
            # The replacement is to ensure all \n are treated as new lines.
            st.text(message.replace('\n', '  \n'))

    def _render_history(self):
        for entry in self._history:
            self._render_message(ROLE_USER, entry.prompt)
            if entry.response:
                self._render_message(ROLE_BOT, entry.response)

    def _render_replay(self):
        for prompt in st.session_state.replay:
            self._render_send_prompt(prompt)

        self._reset_replay()
        st.rerun()

    def _render_input(self):
        if prompt := st.chat_input('Prompt to the LLM '):
            self._render_send_prompt(prompt)

    def _render_send_prompt(self, prompt: str):
        self._render_message(ROLE_USER, prompt)

        with st.spinner("Thinking..."):
            response = self._generator.generate(Prompt(prompt))
            self._render_message(ROLE_BOT, response)
