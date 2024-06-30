"""Chat related components."""

import gc
import time
from logging import getLogger

import streamlit as st

ROLE_BOT = 'assistant'
ROLE_USER = 'user'

logger = getLogger()


class ChatComponent():
    """Manages chat messages."""

    def __init__(self):
        if 'messages' not in st.session_state:
            self.clear_history()

    def render_message(self, role: str, message: str):
        """Render a message in the chat area, also saving it to the session."""
        with st.chat_message(role):
            st.markdown(message)

    def render_history(self):
        """Render all messages in the history."""
        for message in st.session_state.messages:
            self.render_message(message['role'], message['content'])

    def render_prompt(self):
        """Render the chat prompt."""
        if prompt := st.chat_input('Prompt to the LLM '):
            self.render_message(ROLE_USER, prompt)
            self._save_message(ROLE_USER, prompt)

            with st.spinner("Thinking..."):
                time.sleep(2)
                self.render_message(ROLE_BOT, prompt)
                self._save_message(ROLE_BOT, prompt)

    def clear_history(self):
        """Clear all chat messages."""
        st.session_state.messages = []
        gc.collect()

    def _save_message(self, role: str, message: str):
        """Save a message to the session."""
        st.session_state.messages.append({'role': role, 'content': message})
