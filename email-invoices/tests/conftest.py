"""
Shared pytest fixtures for email processor tests.
"""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_imap_server():
    """Fixture providing a mock IMAP server."""
    mock_imap = MagicMock()
    mock_imap.login.return_value = ('OK', [b'Success'])
    mock_imap.select.return_value = ('OK', [b'1'])
    mock_imap.search.return_value = ('OK', [b'1 2 3'])
    return mock_imap
