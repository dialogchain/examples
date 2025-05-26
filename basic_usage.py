#!/usr/bin/env python3
"""
Basic usage example for DialogChain.
This example demonstrates how to create a simple DialogChain application
with a timer source and a logging destination.
"""
import asyncio
import logging
from datetime import datetime

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def timer_source(interval_seconds=3):
    """A simple timer source that yields messages at regular intervals."""
    while True:
        try:
            # Create a message with the current time
            message = {
                'timestamp': datetime.now().isoformat(),
                'message': 'Hello from Timer Source!'
            }
            yield message
            await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            logger.info("Timer source cancelled")
            break
        except Exception as e:
            logger.error(f"Error in timer source: {e}")
            await asyncio.sleep(1)  # Prevent tight loop on errors

async def log_destination(message):
    """A simple logging destination."""
    try:
        logger.info(f"Received message: {message}")
    except Exception as e:
        logger.error(f"Error in log destination: {e}")

async def main():
    """Main function to run the example."""
    logger.info("Starting DialogChain example...")
    
    # Create an async task for the timer source
    timer_task = asyncio.create_task(
        process_messages(timer_source(3), log_destination)
    )
    
    try:
        # Run for 15 seconds
        await asyncio.sleep(15)
        
        # Cancel the timer task
        timer_task.cancel()
        try:
            await timer_task
        except asyncio.CancelledError:
            pass
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        timer_task.cancel()
        try:
            await timer_task
        except asyncio.CancelledError:
            pass

async def process_messages(source, destination):
    """Process messages from source and send to destination."""
    try:
        async for message in source:
            await destination(message)
    except asyncio.CancelledError:
        logger.info("Message processing cancelled")
        raise
    except Exception as e:
        logger.error(f"Error in message processing: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
