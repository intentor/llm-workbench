"""Chat management components module.

Sessions:
    - messages: Chat message history. 
    - replay: User prompts to replay.
"""

import gc
from logging import getLogger
from typing import Dict, List

import streamlit as st

from llm.operator import LlmOperator
from ui.component.base import OperationModeManager, UiComponent

ROLE_BOT = 'assistant'
ROLE_USER = 'user'

logger = getLogger()


class ChatComponent(UiComponent):
    """Manages chat messages."""

    def __init__(
            self,
            mode_manager: OperationModeManager,
            operator: LlmOperator):
        super().__init__(mode_manager, operator)
        if 'messages' not in st.session_state:
            self.clear_history()
        if 'replay' not in st.session_state:
            self._reset_replay()

    def render(self):
        self._render_history()

        if self._has_replay():
            self._render_replay()
        else:
            self._render_input()

    def replay(self, prompts: List[str]):
        """Replay a list of prompts.

        Args:
            - prompts: Prompts to be sent to the LLM.
        """
        self.clear_history()
        st.session_state.replay = prompts

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

    def _reset_replay(self):
        """Reset replay data."""
        st.session_state.replay = []

    def _has_replay(self) -> bool:
        """Get whether there are replay data."""
        return len(st.session_state.replay) > 0

    def _render_message(self, role: str, message: str):
        """Render a message in the chat area, also saving it to the session."""
        with st.chat_message(role):
            # The replacement is to ensure all \n are treated as new lines.
            st.markdown(message.replace('\n', '  \n'))

    def _render_history(self):
        """Render all messages in the history."""
        for message in st.session_state.messages:
            self._render_message(message['role'], message['content'])

    def _render_replay(self):
        """Perform the replay of messages."""
        for prompt in st.session_state.replay:
            self._render_send_prompt(prompt)

        self._reset_replay()
        st.rerun()

    def _render_input(self):
        """Render the input of chat prompts."""
        if prompt := st.chat_input('Prompt to the LLM '):
            self._render_send_prompt(prompt)

    def _render_send_prompt(self, prompt: str):
        """Render and perform the sending of the prompt to the LLM.

        Args:
            - prompt: Prompt to be sent.
        """
        self._render_message(ROLE_USER, prompt)
        self._save_message(ROLE_USER, prompt)

        with st.spinner("Thinking..."):
            response = self._operator.generate(prompt)
            self._render_message(ROLE_BOT, response)
            self._save_message(ROLE_BOT, response)

    def _save_message(self, role: str, message: str):
        """Save a message to the session."""
        st.session_state.messages.append({'role': role, 'content': message})
