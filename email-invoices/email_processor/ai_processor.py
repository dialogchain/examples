"""
AI Processing Module for Email Invoice Processor

This module provides AI-powered processing of invoice data using DialogChain.
"""

import logging
from typing import Dict, Any, Optional
import json
import os

from dialogchain.engine import DialogChainEngine as DialogChain
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

class AIProcessor:
    """Handles AI processing of invoice data using DialogChain."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the AI processor with configuration.
        
        Args:
            config: Configuration dictionary with DialogChain settings
        """
        self.config = config.get("dialogchain", {})
        self.enabled = self.config.get("enabled", False)
        
        if not self.enabled:
            logger.info("DialogChain processing is disabled in configuration")
            return
            
        # Initialize DialogChain with configuration
        try:
            self.chain = DialogChain(
                model_name=self.config.get("model", "gpt-3.5-turbo"),
                api_key=os.getenv("OPENAI_API_KEY") or self.config.get("api_key"),
                temperature=float(self.config.get("temperature", 0.7)),
                max_tokens=int(self.config.get("max_tokens", 1000)),
            )
            
            # Set up system prompt
            self.system_prompt = self.config.get(
                "system_prompt",
                "You are an AI assistant that helps process and extract information from invoices."
                " Extract key information such as invoice number, date, total amount, vendor name,"
                " and line items. Return the data in a structured JSON format."
            )
            
            logger.info("DialogChain processor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize DialogChain: {e}")
            self.enabled = False

    def process_invoice(self, text_content: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Process invoice text using DialogChain.
        
        Args:
            text_content: Extracted text from the invoice
            file_path: Optional path to the original file
            
        Returns:
            Dict containing processed invoice data
        """
        if not self.enabled:
            logger.debug("DialogChain processing is disabled, returning empty result")
            return {}
            
        try:
            # Prepare the prompt
            prompt = f"""Extract structured information from the following invoice text. 
            Include invoice number, date, total amount, vendor name, and line items.
            
            Invoice text:
            {text_content}
            
            Return the data as a JSON object with the following structure:
            {{
                "invoice_number": "string",
                "date": "YYYY-MM-DD",
                "total_amount": float,
                "currency": "string",
                "vendor_name": "string",
                "line_items": [
                    {{
                        "description": "string",
                        "quantity": float,
                        "unit_price": float,
                        "total": float
                    }}
                ]
            }}"""
            
            # Process with DialogChain
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            logger.debug("Sending request to DialogChain...")
            response = self.chain.invoke(messages)
            
            # Try to parse the response as JSON
            try:
                if isinstance(response, str):
                    result = json.loads(response)
                else:
                    result = response
                
                logger.info("Successfully processed invoice with AI")
                return {"success": True, "data": result}
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                return {
                    "success": False, 
                    "error": f"Failed to parse AI response: {str(e)}",
                    "raw_response": str(response)
                }
                
        except Exception as e:
            error_msg = f"Error processing invoice with AI: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"success": False, "error": error_msg}
            
    def is_enabled(self) -> bool:
        """Check if AI processing is enabled."""
        return self.enabled
