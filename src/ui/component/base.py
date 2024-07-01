"""Base components module."""

from abc import abstractmethod
from enum import Enum
from logging import getLogger

import streamlit as st

from llm.operator import LlmOperator

logger = getLogger()


class OperationMode(Enum):
    """Mode the UI is operating on."""
    CHAT = 1
    REPLAY = 2


class OperationModeManager():
    """Manages the mode the app is."""

    def __init__(
        self,
        initial_mode: OperationMode = OperationMode.CHAT
    ):
        if 'mode' not in st.session_state:
            st.session_state.mode = initial_mode

    def get_mode(self) -> OperationMode:
        """Get the current operation mode."""
        return st.session_state.mode

    def set_mode(self, mode: OperationMode):
        """Set the current operation mode."""
        st.session_state.mode = mode
        logger.info('m=set mode=%s', mode)


class UiComponent():
    """Define a base UI component."""

    def __init__(
        self,
        mode_manager: OperationModeManager,
        operator: LlmOperator
    ):
        self._mode_manager = mode_manager
        self._operator = operator

    @ abstractmethod
    def render(self):
        """Render the component."""
        return
