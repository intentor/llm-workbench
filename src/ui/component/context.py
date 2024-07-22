"""Context management components module.

Sessions:
    - id: Session ID
    - files: List of the uploaded files.
"""

import os
import traceback
from logging import getLogger

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from config import SESSION_PATH
from core.indexer import ContextIndexer
from ui.component.base import OperationModeManager, UiComponent
import ui.component.icon as icon

logger = getLogger()


class ContextCompoonent(UiComponent):
    """Manages context UI operations."""

    def __init__(
            self,
            mode_manager: OperationModeManager,
            indexer: ContextIndexer
    ):
        super().__init__(mode_manager)
        self._indexer = indexer
        if 'files' not in st.session_state:
            st.session_state.files = []

    def render(self):
        st.header('Context management', divider='orange')

        if not self._has_files():
            self._render_upload_context()
        else:
            self._render_list_context()

    def _render_upload_context(self):
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

            chunk_size = st.number_input(
                label='Chunk size',
                value=1024,
                min_value=128,
                max_value=2048,
                step=128,
                help='Size when splitting documents. The smaller, the more precise.'
            )

            chunk_overlap = st.number_input(
                label='Chunk overlap',
                value=20,
                min_value=5,
                max_value=100,
                step=5,
                help='Amount of overlap when splitting documents into chunk_size.'
            )

            if st.form_submit_button('Index'):
                if uploaded_files:
                    try:
                        with st.spinner('Indexing files...'):
                            files_path = self._save_files(uploaded_files)
                            self._indexer.index_files(
                                files_path,
                                chunk_size,
                                chunk_overlap)
                            st.session_state.files = files_path
                            st.success('Files indexed', icon=icon.SUCCESS)
                            st.rerun()
                    except Exception as e:
                        tb = traceback.format_exc()
                        logger.error(tb)
                        st.error(f"Error: {e}")

    def _save_files(
            self,
            files: list[UploadedFile]
    ) -> list[str]:
        files_info: list[str] = []
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
        with st.container(border=True):
            st.write(f"Indexed files ({len(st.session_state.files)})")
            for file in st.session_state.files:
                st.code(os.path.basename(file))

    def _has_files(self) -> bool:
        return len(st.session_state.files) > 0
