"""
Configuration loader for the email invoice processor.
"""

import os
import logging
import yaml
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """
    Load configuration from YAML file and environment variables.
    
    Returns:
        Dictionary containing the configuration
    """
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Default configuration
    config = {
        'email': {
            'server': 'localhost',
            'port': 993,
            'username': '',
            'password': '',
            'folder': 'INBOX',
            'ssl': True,
            'processed_folder': 'Processed'
        },
        'processing': {
            'output_dir': 'output',
            'keep_original_attachments': True,
            'file_extensions': ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/email_processor.log'
        },
        'dialogchain': {
            'enabled': False,
            'model': 'gpt-3.5-turbo',
            'api_key': '',
            'max_tokens': 1000,
            'temperature': 0.7
        }
    }
    
    # Load from config file if it exists
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                # Deep merge with defaults
                for section, section_config in file_config.items():
                    if section in config and isinstance(config[section], dict):
                        config[section].update(section_config)
                    else:
                        config[section] = section_config
        except Exception as e:
            logger.warning(f"Failed to load config file {config_path}: {e}")
    
    # Override with environment variables
    for key, value in os.environ.items():
        key_lower = key.lower()
        
        # Handle email settings
        if key_lower.startswith('email_'):
            subkey = key_lower[6:]  # Remove 'email_'
            if subkey == 'port':
                try:
                    config['email'][subkey] = int(value)
                except ValueError:
                    logger.warning(f"Invalid port number: {value}")
            elif subkey in ['ssl', 'tls']:
                config['email'][subkey] = value.lower() in ('true', '1', 'yes')
            else:
                config['email'][subkey] = value
            
        # Handle processing settings
        elif key_lower.startswith('processing_'):
            subkey = key_lower[11:]  # Remove 'processing_'
            if subkey in ['keep_original_attachments']:
                config['processing'][subkey] = value.lower() in ('true', '1', 'yes')
            elif subkey == 'file_extensions':
                config['processing'][subkey] = [ext.strip() for ext in value.split(',')]
            else:
                config['processing'][subkey] = value
            
        # Handle DialogChain settings
        elif key_lower.startswith('dialogchain_'):
            subkey = key_lower[12:]  # Remove 'dialogchain_'
            if subkey == 'enabled':
                config['dialogchain']['enabled'] = value.lower() in ('true', '1', 'yes')
            elif subkey in ('max_tokens', 'temperature'):
                try:
                    config['dialogchain'][subkey] = float(value)
                except ValueError:
                    logger.warning(f"Invalid value for {key}: {value}")
            else:
                config['dialogchain'][subkey] = value
    
    return config

def setup_logging(config: Dict[str, Any]) -> None:
    """
    Set up logging configuration.
    
    Args:
        config: Configuration dictionary
    """
    log_level = getattr(logging, config.get('logging', {}).get('level', 'INFO').upper())
    log_file = config.get('logging', {}).get('file')
    
    # Clear any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.root.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)
    
    # Set log level
    logging.root.setLevel(log_level)
