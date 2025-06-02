"""
Email Invoice Processor

This module provides functionality to process emails, extract invoice attachments,
and save them in a structured format with optional AI-powered processing.
"""

import imaplib
import os
import logging
import json
import time
from datetime import datetime
from pathlib import Path
from email import message as email_message
from email import message_from_bytes
from typing import Dict, Any, Optional, List, Tuple

# Local imports
from .ai_processor import AIProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailProcessor:
    """
    A class to process emails and extract invoice attachments.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the EmailProcessor with configuration.

        Args:
            config: A dictionary containing configuration settings
        """
        self.config = config
        self.mail = None
        self._ensure_output_dirs()
        
        # Initialize AI processor if enabled
        self.ai_processor = AIProcessor(config)

    def _ensure_output_dirs(self) -> None:
        """Ensure that output directories exist."""
        os.makedirs(self.config.get('output_dir', 'output'), exist_ok=True)

    def _connect_email(self) -> None:
        """
        Connect to the email server using IMAP.

        Raises:
            RuntimeError: If connection to the email server fails
        """
        try:
            self.mail = imaplib.IMAP4_SSL(
                self.config['email']['server'],
                self.config['email']['port']
            )
            self.mail.login(
                self.config['email']['username'],
                self.config['email']['password']
            )
            logger.info("Successfully connected to email server")
        except Exception as e:
            logger.error(f"Failed to connect to email server: {e}")
            raise RuntimeError(f"Failed to connect to email server: {e}") from e

    def _save_attachment(self, part: email_message.Message, output_dir: str) -> Optional[str]:
        """
        Save an email attachment to disk.

        Args:
            part: The email part containing the attachment
            output_dir: Directory to save the attachment

        Returns:
            Path to the saved file or None if saving failed
        """
        filename = part.get_filename()
        if not filename:
            return None

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a safe filename
        safe_filename = "".join(c if c.isalnum() or c in ' .-_' else '_' for c in filename)
        filepath = os.path.join(output_dir, safe_filename)
        
        try:
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            logger.info(f"Saved attachment: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save attachment {filename}: {e}")
            return None
            
    def _process_attachment(self, part: email_message.Message) -> Dict[str, Any]:
        """
        Process an email attachment with optional AI processing.

        Args:
            part: The email part containing the attachment
            
        Returns:
            Dict containing processing results
        """
        # Create output directories
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(self.config.get('output_dir', 'output'), timestamp)
        original_dir = os.path.join(output_dir, 'original')
        processed_dir = os.path.join(output_dir, 'processed')
        
        # Save original attachment
        filepath = self._save_attachment(part, original_dir)
        if not filepath:
            return {"success": False, "error": "Failed to save attachment"}
            
        result = {
            "original_file": filepath,
            "timestamp": datetime.now().isoformat(),
            "ai_processing": {}
        }
        
        # Process with AI if enabled
        if self.ai_processor.is_enabled():
            try:
                # For now, just log that we would process with AI
                # In a real implementation, you would extract text and pass to AI
                logger.info(f"Processing with AI: {filepath}")
                # This is a placeholder - you would implement actual text extraction
                ai_result = self.ai_processor.process_invoice(
                    f"Invoice from attachment: {os.path.basename(filepath)}"
                )
                result["ai_processing"] = ai_result
                
                # Save AI results
                os.makedirs(processed_dir, exist_ok=True)
                result_file = os.path.join(processed_dir, f"{os.path.basename(filepath)}.json")
                with open(result_file, 'w') as f:
                    json.dump(ai_result, f, indent=2)
                    
            except Exception as e:
                logger.error(f"AI processing failed: {e}", exc_info=True)
                result["ai_processing"] = {
                    "success": False,
                    "error": str(e)
                }
        
        return result

    def process_emails(self) -> List[Dict[str, Any]]:
        """
        Process all emails in the configured folder.
        
        Returns:
            List of processing results for each email
        """
        if not self.mail:
            raise RuntimeError("Not connected to email server. Call _connect_email() first.")

        results = []
        
        try:
            # Select the folder to process
            folder = self.config['email'].get('folder', 'INBOX')
            logger.info(f"Processing emails from folder: {folder}")
            status, _ = self.mail.select(folder)
            
            if status != 'OK':
                raise RuntimeError(f"Failed to select folder: {folder}")
            
            # Search for all unseen emails
            status, messages = self.mail.search(None, 'UNSEEN')
            if status != 'OK':
                logger.error("Failed to search emails")
                return results
                
            message_ids = messages[0].split()
            logger.info(f"Found {len(message_ids)} new messages to process")
            
            if not message_ids:
                logger.info("No new messages to process")
                return results

            # Process each email
            for msg_id in message_ids:
                try:
                    # Mark as seen to avoid reprocessing
                    self.mail.store(msg_id, '+FLAGS', r'\Seen')
                    
                    # Fetch the email
                    status, data = self.mail.fetch(msg_id, '(RFC822)')
                    if status != 'OK':
                        logger.error(f"Failed to fetch email {msg_id.decode()}")
                        continue

                    raw_email = data[0][1]
                    email_msg = message_from_bytes(raw_email)
                    
                    # Process each attachment
                    for part in email_msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                            
                        if part.get('Content-Disposition') is None:
                            continue
                            
                        # Process the attachment
                        result = self._process_attachment(part)
                        if result:
                            results.append(result)
                            
                except Exception as e:
                    logger.error(f"Error processing email {msg_id}: {e}", exc_info=True)
                    
        except Exception as e:
            logger.error(f"Error in process_emails: {e}", exc_info=True)
            raise
            
        return results

    def _move_to_processed(self, msg_id: str, processed_folder: str) -> bool:
        """
        Move an email to the processed folder.
        
        Args:
            msg_id: The ID of the message to move
            processed_folder: Name of the folder to move the message to
            
        Returns:
            True if the message was moved successfully, False otherwise
        """
        try:
            # Copy the message to the processed folder
            result = self.mail.copy(msg_id, processed_folder)
            if result[0] != 'OK':
                logger.error(f"Failed to copy message {msg_id} to {processed_folder}")
                return False
                
            # Mark the original message as deleted
            self.mail.store(msg_id, '+FLAGS', '\\Deleted')
            self.mail.expunge()
            return True
            
        except Exception as e:
            logger.error(f"Error moving message {msg_id} to {processed_folder}: {e}")
            return False

    def run(self) -> None:
        """
        Run the email processing pipeline.
        """
        try:
            self._connect_email()
            self.process_emails()
        except Exception as e:
            logger.error(f"Error in email processing pipeline: {e}")
            raise
        finally:
            if self.mail:
                try:
                    self.mail.close()
                    self.mail.logout()
                except Exception as e:
                    logger.error(f"Error closing email connection: {e}")


def main():
    """Main entry point for the email processor."""
    import argparse
    import yaml
    
    parser = argparse.ArgumentParser(description='Process email invoices.')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Path to configuration file')
    
    args = parser.parse_args()
    
    try:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
        
        processor = EmailProcessor(config)
        processor.run()
        
    except Exception as e:
        logger.error(f"Failed to run email processor: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
