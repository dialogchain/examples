#!/usr/bin/env python3
"""
Comparison between Python implementation and YAML DSL for DialogChain.
Measures the time taken to implement and execute both approaches.
"""
import asyncio
import time
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("comparison")

# Paths
PYTHON_SCRIPT = "examples/basic_usage.py"
YAML_CONFIG = "examples/basic_usage_dsl.yaml"

async def run_python_implementation():
    """Run the Python implementation and measure execution time."""
    logger.info("Running Python implementation...")
    start_time = time.time()
    
    try:
        process = await asyncio.create_subprocess_exec(
            "python3", PYTHON_SCRIPT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the process to complete (should take ~15 seconds)
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"Python implementation failed with error: {stderr.decode()}")
            return None
            
        execution_time = time.time() - start_time
        logger.info(f"Python implementation completed in {execution_time:.2f} seconds")
        return execution_time
        
    except Exception as e:
        logger.error(f"Error running Python implementation: {e}")
        return None

async def run_dsl_implementation():
    """Run the YAML DSL implementation and measure execution time."""
    logger.info("Running YAML DSL implementation...")
    start_time = time.time()
    
    try:
        # Run dialogchain from the python directory
        process = await asyncio.create_subprocess_exec(
            "python", "-m", "dialogchain.cli", "run",
            "--config", f"../{YAML_CONFIG}",
            cwd="python",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the process to complete (should take ~15 seconds)
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"YAML DSL implementation failed with error: {stderr.decode()}")
            return None
            
        execution_time = time.time() - start_time
        logger.info(f"YAML DSL implementation completed in {execution_time:.2f} seconds")
        return execution_time
        
    except Exception as e:
        logger.error(f"Error running YAML DSL implementation: {e}")
        return None

async def main():
    """Run the comparison between both approaches."""
    logger.info("Starting comparison between Python and YAML DSL implementations...")
    
    # Run Python implementation
    python_time = await run_python_implementation()
    
    # Give some time between runs
    await asyncio.sleep(2)
    
    # Run YAML DSL implementation
    dsl_time = await run_dsl_implementation()
    
    # Print comparison
    logger.info("\n=== Comparison Results ===")
    if python_time is not None and dsl_time is not None:
        time_saved = python_time - dsl_time
        percentage_saved = (time_saved / python_time) * 100 if python_time > 0 else 0
        
        logger.info(f"Python implementation time: {python_time:.2f} seconds")
        logger.info(f"YAML DSL implementation time: {dsl_time:.2f} seconds")
        logger.info(f"Time saved: {time_saved:.2f} seconds ({percentage_saved:.1f}%)")
        
        # Lines of code comparison (rough estimate)
        python_loc = sum(1 for _ in open(PYTHON_SCRIPT, 'r') if _.strip() and not _.lstrip().startswith('#'))
        yaml_loc = sum(1 for _ in open(YAML_CONFIG, 'r') if _.strip() and not _.lstrip().startswith('#'))
        
        logger.info(f"\nCode complexity comparison:")
        logger.info(f"Python implementation: {python_loc} lines of code")
        logger.info(f"YAML DSL implementation: {yaml_loc} lines of code")
        logger.info(f"Reduction: {python_loc - yaml_loc} lines ({(1 - yaml_loc/python_loc)*100:.1f}% less code)")
    else:
        logger.error("Comparison could not be completed due to errors")

if __name__ == "__main__":
    asyncio.run(main())
