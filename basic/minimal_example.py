#!/usr/bin/env python3
"""
Minimal DialogChain Example

This script demonstrates a basic DialogChain setup with:
- A timer source that emits events every 2 seconds
- A simple processor that transforms the message
- A console logger as the destination
"""

import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dialogchain_example")

async def timer_source(interval=2):
    """A simple timer that yields messages at regular intervals."""
    counter = 0
    while True:
        try:
            counter += 1
            message = {
                'id': counter,
                'type': 'timer_tick',
                'timestamp': datetime.utcnow().isoformat(),
                'message': f'Timer event #{counter}'
            }
            yield message
            await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logger.info("Timer source cancelled")
            break
        except Exception as e:
            logger.error(f"Error in timer source: {e}")
            await asyncio.sleep(1)  # Prevent tight loop on errors

async def process_message(message):
    """Process and transform the message."""
    try:
        # Add processing timestamp and transform the message
        processed = {
            **message,
            'processed_at': datetime.utcnow().isoformat(),
            'transformed': True,
            'original_message': message['message']
        }
        return processed
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return None

async def log_destination(message):
    """Log the message to the console."""
    try:
        logger.info(f"Processed message: {message}")
    except Exception as e:
        logger.error(f"Error in log destination: {e}")

async def main():
    """Main function to run the example."""
    logger.info("Starting DialogChain example...")
    
    # Create the timer source
    source = timer_source(interval=2)
    
    try:
        # Process messages
        async for message in source:
            processed = await process_message(message)
            if processed:
                await log_destination(processed)
                
    except asyncio.CancelledError:
        logger.info("Main loop cancelled")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Shutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Example stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
