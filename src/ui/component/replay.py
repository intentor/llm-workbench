"""Replay management components module.

Sessions:
    - prompts: List of prompts to replay.
    - uploader_key: Key for the uploader component. This is a hack to allow 
        the file uploader to reset after being loaded.
"""

import uuid
from io import StringIO
from logging import getLogger

import streamlit as st

from core.prompting.history import PromptHistory
from ui.component.base import OperationMode, OperationModeManager, UiComponent
from ui.component.chat import ChatComponent

PROMPT_DIVIDER_KEY = '{{PROMPT}}'
PROMPT_DIVIDER = f"{PROMPT_DIVIDER_KEY}\n"

logger = getLogger()


class ReplayComponent(UiComponent):
    """Ällow management of replaying prompts."""

    def __init__(
            self,
            mode_manager: OperationModeManager,
            history: PromptHistory,
            chat: ChatComponent
    ):
        super().__init__(mode_manager)
        self._history = history
        self._chat = chat

        if 'prompts' not in st.session_state:
            st.session_state.prompts = ''
            self._reset_uploader_key()

    def load_prompts_from_history(self):
        """Load prompts from chat history."""
        prompts_in_history: list[str] = self._history.get_prompts()
        prompts = PROMPT_DIVIDER + \
            f"\n\n{PROMPT_DIVIDER}".join(prompts_in_history)
        self._set_prompts(prompts)

        logger.info('m=messages from=list size=%d', len(prompts))

    def render(self):
        with st.container(border=True):
            prompts = st.text_area(
                'Prompts to replay',
                value=self._get_prompts_as_str(),
                height=375)
            self._set_prompts(prompts)

            col1, col2, col3, col4 = st.columns(
                [4, 0.8, 1.2, 1], vertical_alignment='center')

            with col1:
                uploaded_file = st.file_uploader(
                    'Load prompts file',
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
                    help='Execute replay of the entered prompts.'
                ):
                    prompts_to_replay = self._get_prompts_as_list()
                    self._chat.replay(prompts_to_replay)
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
        self._mode_manager.set_mode(OperationMode.CHAT)
        st.rerun()

    def _reset_uploader_key(self):
        st.session_state.uploader_key = f"uploader_{str(uuid.uuid4())}"

    def _set_prompts(self, prompts: str):
        st.session_state.prompts = prompts

    def _get_prompts_as_str(self) -> str:
        return st.session_state.prompts

    def _get_prompts_as_list(self) -> list[str]:
        prompts_str = self._get_prompts_as_str()
        prompts = prompts_str.split(f"{PROMPT_DIVIDER}")
        return [p.rstrip() for p in prompts if p != '']
