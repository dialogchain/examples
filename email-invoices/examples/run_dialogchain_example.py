"""
Example script demonstrating how to use DialogChain flows from a YAML configuration file.
"""

import os
import json
import yaml
from pathlib import Path
from dialogchain.engine import DialogChainEngine

# Load the DialogChain configuration
config_path = Path(__file__).parent / 'dialogchain_example.yaml'
with open(config_path, 'r') as f:
    dialog_config = yaml.safe_load(f)

# Initialize the DialogChain engine
engine = DialogChainEngine(config=dialog_config)

def process_invoice_example():
    """Example of processing an invoice using the invoice_processing flow."""
    # Sample invoice text (in a real application, this would come from OCR or other sources)
    invoice_text = """
    INVOICE #INV-2023-0042
    
    Vendor: Tech Solutions Inc.
    Tax ID: PL1234567890
    Date: 2023-11-15
    Due Date: 2023-12-15
    
    BILL TO:
    Acme Corp
    123 Business St
    Warsaw, 00-001
    
    DESCRIPTION                QTY   UNIT PRICE   TOTAL
    ------------------------------------------------
    Laptop XYZ                2      $1,200.00   $2,400.00
    Extended Warranty (1 yr)  2      $120.00      $240.00
    
    SUBTOTAL:                $2,640.00
    TAX (23%):               $607.20
    TOTAL:                   $3,247.20
    
    Payment Terms: Net 30
    Payment Method: Bank Transfer
    
    Thank you for your business!
    """
    
    # Run the invoice processing flow
    result = engine.process(
        flow_name="invoice_processing",
        variables={"invoice_text": invoice_text}
    )
    
    print("=== Invoice Processing Results ===")
    print(json.dumps(result, indent=2))
    return result

def validate_invoice_example(invoice_data):
    """Example of validating invoice data using the validate_invoice flow."""
    result = engine.process(
        flow_name="validate_invoice",
        variables={"invoice_data": invoice_data}
    )
    
    print("\n=== Invoice Validation Results ===")
    print(json.dumps(result, indent=2))
    return result

def classify_document_example():
    """Example of classifying a document using the classify_document flow."""
    # Sample document text
    document_text = """
    RECEIPT #RCPT-2023-4567
    
    Merchant: Office Supplies Co.
    Date: 2023-11-20 14:30:22
    
    ITEMS:
    1x Notebooks (pack of 3)      $12.99
    2x Pens (black)               $3.98
    1x Sticky Notes (yellow)      $4.50
    
    SUBTOTAL: $21.47
    TAX:      $1.72
    TOTAL:    $23.19
    
    Payment Method: Credit Card (VISA)
    Card ending in: 1234
    
    Thank you for your purchase!
    """
    
    result = engine.process(
        flow_name="classify_document",
        variables={"document_text": document_text}
    )
    
    print("\n=== Document Classification Results ===")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    # Run the invoice processing example
    processed_data = process_invoice_example()
    
    # Use the processed data for validation
    if processed_data and isinstance(processed_data, dict):
        validate_invoice_example(processed_data)
    
    # Run the document classification example
    classify_document_example()
