"""
Unit tests for the EmailProcessor class.
"""

import imaplib
import os
import pytest
from unittest.mock import MagicMock, patch
from email_processor.process_invoices import EmailProcessor


class TestEmailProcessor:
    """Test cases for the EmailProcessor class."""

    @pytest.fixture
    def sample_config(self, tmp_path):
        """Return a sample configuration dictionary for testing."""
        output_dir = tmp_path / "output"
        return {
            'email': {
                'server': 'imap.example.com',  # Changed from 'host' to 'server'
                'port': 993,
                'username': 'user@example.com',
                'password': 'password',
                'folder': 'INBOX',
            },
            'output_dir': str(output_dir),
            'file_extensions': ['.pdf', '.jpg', '.png'],
        }

    def test_init_creates_output_dir(self, sample_config, tmp_path):
        """Test that __init__ creates the output directory if it doesn't exist."""
        output_dir = tmp_path / "new_output"
        sample_config['output_dir'] = str(output_dir)
        
        # Directory shouldn't exist before initialization
        assert not output_dir.exists()
        
        # Initialize the processor
        processor = EmailProcessor(sample_config)
        
        # Directory should exist after initialization
        assert output_dir.exists()
        assert output_dir.is_dir()

    @patch('imaplib.IMAP4_SSL')
    def test_connect_email_success(self, mock_imap, sample_config):
        """Test successful email connection."""
        # Setup mock
        mock_imap.return_value.login.return_value = ('OK', [b'Success'])
        mock_imap.return_value.select.return_value = ('OK', [b'1'])
        
        # Test
        processor = EmailProcessor(sample_config)
        processor._connect_email()
        
        # Verify
        assert processor.mail is not None
        mock_imap.return_value.login.assert_called_once_with(
            sample_config['email']['username'],
            sample_config['email']['password']
        )
        # Note: The actual implementation doesn't call select in _connect_email
        # So we don't expect it to be called here

    @patch('imaplib.IMAP4_SSL')
    def test_connect_email_login_failure(self, mock_imap, sample_config):
        """Test email connection failure during login."""
        # Setup mock to fail login
        mock_imap.return_value.login.side_effect = imaplib.IMAP4.error("Login failed")
        
        # Test and verify
        processor = EmailProcessor(sample_config)
        with pytest.raises(RuntimeError, match="Failed to connect to email server"):
            processor._connect_email()

    def test_process_attachment_skips_non_attachments(self, sample_config):
        """Test that non-attachment parts are skipped."""
        # Setup
        processor = EmailProcessor(sample_config)
        part = MagicMock()
        part.get_filename.return_value = None
        
        # Test
        processor._process_attachment(part)
        
        # Verify no file was written
        part.get_payload.assert_not_called()

    @patch('builtins.open')
    @patch('email_processor.process_invoices.datetime')
    @patch('os.makedirs')
    def test_process_attachment_saves_file(self, mock_makedirs, mock_datetime, mock_open, sample_config, tmp_path):
        """Test that attachments are saved correctly in timestamped directory."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "20250602_123456"
        processor = EmailProcessor(sample_config)
        part = MagicMock()
        part.get_filename.return_value = "test.pdf"
        part.get_payload.return_value = b"test content"
        
        # Test
        processor._process_attachment(part)
        
        # Verify the file was opened with the correct path
        expected_dir = os.path.join(sample_config['output_dir'], "20250602_123456", "original")
        expected_path = os.path.join(expected_dir, "test.pdf")
        part.get_payload.assert_called_once_with(decode=True)
        mock_open.assert_called_once_with(expected_path, 'wb')
        
        # Verify the original directory was created
        expected_dir_path = os.path.join(sample_config['output_dir'], "20250602_123456")
        expected_original_dir = os.path.join(expected_dir_path, "original")
        
        # Check that makedirs was called for the original directory
        mock_makedirs.assert_called_with(expected_original_dir, exist_ok=True)
    
    @patch('builtins.open')
    @patch('email_processor.process_invoices.datetime')
    @patch('os.makedirs')
    @patch('email_processor.process_invoices.AIProcessor.is_enabled')
    def test_process_attachment_with_ai_creates_processed_dir(self, mock_ai_enabled, mock_makedirs, 
                                                             mock_datetime, mock_open, sample_config, tmp_path):
        """Test that processed directory is created when AI processing is enabled."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "20250602_123456"
        mock_ai_enabled.return_value = True  # Enable AI processing
        
        processor = EmailProcessor(sample_config)
        part = MagicMock()
        part.get_filename.return_value = "test.pdf"
        part.get_payload.return_value = b"test content"
        
        # Mock the AI processor's process_invoice method
        mock_ai_processor = MagicMock()
        mock_ai_processor.is_enabled.return_value = True
        mock_ai_processor.process_invoice.return_value = {"status": "processed"}
        processor.ai_processor = mock_ai_processor
        
        # Test
        processor._process_attachment(part)
        
        # Verify the processed directory was created
        expected_dir_path = os.path.join(sample_config['output_dir'], "20250602_123456")
        expected_processed_dir = os.path.join(expected_dir_path, "processed")
        
        # Check that makedirs was called for the processed directory
        mock_makedirs.assert_any_call(expected_processed_dir, exist_ok=True)
