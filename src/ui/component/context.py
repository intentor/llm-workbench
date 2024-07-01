"""Context management components module.

Sessions:
    - id: Session ID
    - files: List of the uploaded files.
"""

import os
import traceback
from logging import getLogger
from typing import List

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from config import SESSION_PATH
from llm.operator import LlmOperator
from ui.component.base import OperationModeManager, UiComponent
import ui.component.icon as icon

logger = getLogger()


class ContextCompoonent(UiComponent):
    """Manages context UI operations."""

    def __init__(
            self,
            mode_manager: OperationModeManager,
            operator: LlmOperator
    ):
        super().__init__(mode_manager, operator)
        if 'files' not in st.session_state:
            st.session_state.files = []

    def render(self):
        st.header('Context management', divider='orange')

        if not self._has_files():
            self._render_upload_context()
        else:
            self._render_list_context()

    def _render_upload_context(self):
        """Render the upload components for the context module."""
        st.info(
            'To use context data on prompts, you have to upload files '
            'so their content can be indexed and available for querying.',
            icon=icon.INFO
        )

        with st.form("files_form"):
            uploaded_files = st.file_uploader(
                "Choose context files",
                type=['pdf', 'docx', 'xlsx', 'txt'],
                accept_multiple_files=True)

            if st.form_submit_button('Index'):
                if uploaded_files:
                    try:
                        with st.spinner('Indexing files...'):
                            files_path = self._save_files(uploaded_files)
                            st.session_state.files = files_path
                            self._operator.index_files(files_path)
                            st.success('Files indexed', icon=icon.SUCCESS)
                            st.rerun()
                    except Exception as e:
                        tb = traceback.format_exc()
                        logger.error(tb)
                        st.error(f"Error: {e}")
                        st.stop()

    def _save_files(
            self,
            files: list[UploadedFile]
    ) -> List[str]:
        """Save a list of files in the disk.

        Args:
            files_path: Path where the files will be saved.
            files: Files to save.

        Returns:
            Path of the uploaded files.
        """
        files_info: List[str] = []
        session_dir = os.path.join(SESSION_PATH, st.session_state.id, 'files')
        os.makedirs(session_dir, exist_ok=True)
        for file_to_save in files:
            file_path = os.path.join(session_dir, file_to_save.name)
            logger.info('m=saving file=%s', file_path)

            with open(file_path, 'wb') as file_new:
                file_new.write(file_to_save.getvalue())
                files_info.append(file_path)

        return files_info

    def _render_list_context(self):
        """Render the listing of components for the context module."""
        with st.container(border=True):
            st.write(f"Indexed files ({len(st.session_state.files)})")
            for file in st.session_state.files:
                st.caption(os.path.basename(file))

    def _has_files(self) -> bool:
        """Indicates whether the session has files."""
        return len(st.session_state.files) > 0
