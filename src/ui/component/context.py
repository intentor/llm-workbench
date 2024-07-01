"""Context management components module."""

import time
import traceback
from logging import getLogger

import streamlit as st

from ui.component.base import OperationModeManager, UiComponent
import ui.component.icon as icon

logger = getLogger()


class ContextCompoonent(UiComponent):
    """Manages context UI operations."""

    def __init__(self, mode_manager: OperationModeManager):
        super().__init__(mode_manager)
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
                            time.sleep(2)
                            st.success('Files uploaded', icon=icon.SUCCESS)
                            st.rerun()
                    except Exception as e:
                        tb = traceback.format_exc()
                        logger.error(tb)
                        st.error(f"Error: {e}")
                        st.stop()

    def _render_list_context(self):
        """Render the listing of components for the context module."""
        with st.container(border=True):
            st.write(f"Indexed files ( {len(st.session_state.files)})")
            for file in st.session_state.files:
                st.caption(file.name)

    def _has_files(self) -> bool:
        """Indicates whether the session has files."""
        return len(st.session_state.files) > 0