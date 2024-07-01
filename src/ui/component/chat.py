"""Chat management components module."""

import gc
import time
from logging import getLogger
from typing import Dict, List

import streamlit as st

from ui.component.base import OperationModeManager, UiComponent

ROLE_BOT = 'assistant'
ROLE_USER = 'user'

logger = getLogger()


class ChatComponent(UiComponent):
    """Manages chat messages."""

    def __init__(self, mode_manager: OperationModeManager):
        super().__init__(mode_manager)
        if 'messages' not in st.session_state:
            self.clear_history()

    def render(self):
        self._render_history()
        self._render_prompt()

    def get_history(self, role: str = '') -> List[Dict[str, str]]:
        """Get messages from the chat history.

        Args:
            - role: Role from which the messages should be retrieved.

        Returns:
            List of messages.
        """
        messages = st.session_state.messages
        if role == '':
            return messages
        else:
            return [msg for msg in messages if msg['role'] == role]

    def clear_history(self):
        """Clear all chat messages."""
        st.session_state.messages = []
        gc.collect()

    def _render_message(self, role: str, message: str):
        """Render a message in the chat area, also saving it to the session."""
        with st.chat_message(role):
            st.markdown(message)

    def _render_history(self):
        """Render all messages in the history."""
        for message in st.session_state.messages:
            self._render_message(message['role'], message['content'])

    def _render_prompt(self):
        """Render the chat prompt."""
        if prompt := st.chat_input('Prompt to the LLM '):
            self._render_message(ROLE_USER, prompt)
            self._save_message(ROLE_USER, prompt)

            with st.spinner("Thinking..."):
                time.sleep(2)
                response = f"Response: {prompt}"
                self._render_message(ROLE_BOT, response)
                self._save_message(ROLE_BOT, response)

    def _save_message(self, role: str, message: str):
        """Save a message to the session."""
        st.session_state.messages.append({'role': role, 'content': message})
