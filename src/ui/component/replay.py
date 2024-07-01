"""Replay management components module."""

from typing import Dict, List
import uuid
from io import StringIO
from logging import getLogger

import streamlit as st

from ui.component.base import OperationMode, OperationModeManager, UiComponent
from ui.component.chat import ChatComponent, ROLE_USER

PROMPT_DIVIDER = '{{PROMPT}}'

logger = getLogger()


class ReplayComponent(UiComponent):
    """Ällow management of replaying prompts."""

    def __init__(
            self,
            mode_manager: OperationModeManager,
            chat: ChatComponent
    ):
        super().__init__(mode_manager)
        self._chat = chat

        if 'prompts' not in st.session_state:
            st.session_state.prompts = ''
            self._reset_uploader_key()

    def load_prompts_from_history(self):
        """Load prompts from chat history."""
        history: List[Dict[str, str]] = self._chat.get_history(ROLE_USER)
        messages: List[str] = [msg['content'] for msg in history]
        self.load_prompts_from_list(messages)

    def load_prompts_from_list(self, messages: List[Dict[str, str]]):
        """Load prompts from a list of messages.

        Args:
            - messages: List of messages to load.
        """
        divider = f"{PROMPT_DIVIDER}\n"
        prompts = divider + f"\n\n{divider}".join(messages)
        self._set_prompts(prompts)

        logger.info('m=messages from=list size=%d', len(messages))

    def render(self):
        with st.container(border=True):
            prompts = st.text_area(
                'Prompts to replay',
                value=self._get_prompts(),
                height=375)

            col1, col2, col3, col4 = st.columns(
                [4, 0.8, 1.2, 1], vertical_alignment='center')

            with col1:
                uploaded_file = st.file_uploader(
                    f"Load prompts file - each prompt separated by {
                        PROMPT_DIVIDER}",
                    type='txt',
                    accept_multiple_files=False,
                    key=st.session_state.uploader_key)
                if uploaded_file is not None:
                    contents = StringIO(
                        uploaded_file.getvalue().decode("utf-8"))
                    self._set_prompts(contents.read())

                    logger.info('m=loaded file=%s', uploaded_file.name)
                    self._reset_uploader_key()
                    st.rerun()

            with col2:
                if st.button(
                    'Run',
                    help='Execute replay of the above prompts.'
                ):
                    logger.info('m=replay')
                    self._close()

            with col3:
                st.download_button(
                    label='Download',
                    help='Download a file containing the above prompts.',
                    data=prompts,
                    file_name="prompts.txt",
                    mime="text/plain",
                )

            with col4:
                if st.button(
                    'Cancel',
                    help='Close the replay manager.'
                ):
                    self._close()

    def _close(self):
        """Close the replay mode."""
        self._mode_manager.set_mode(OperationMode.CHAT)
        st.rerun()

    def _reset_uploader_key(self):
        """Reset the key used in the upload component through 
        st.session_state.upload_key. This is a hack to allow the file uploader
        to reset after being loaded.
        """
        st.session_state.uploader_key = f"uploader_{str(uuid.uuid4())}"

    def _set_prompts(self, prompts: str):
        """Set the prompts in the session so it can be later retrieved.

        Args:
            - prompts: Prompts to be saved.
        """
        st.session_state.prompts = prompts

    def _get_prompts(self) -> str:
        """Get saved prompts.

        Returns:
            Prompts in the session.
        """
        return st.session_state.prompts
