#!/usr/bin/env python3
"""
Run DialogChain examples with proper Python path and dependencies.
"""
import os
import sys
import argparse
from pathlib import Path

def setup_environment():
    """Set up the Python environment for running examples."""
    # Add the dialogchain source directory to the Python path
    dialogchain_src = Path(__file__).parent.parent.parent / "python" / "src"
    if str(dialogchain_src) not in sys.path:
        sys.path.insert(0, str(dialogchain_src))
    
    # Ensure we have the required dependencies
    try:
        import dialogchain
        print(f"Using DialogChain from: {dialogchain.__file__}")
    except ImportError as e:
        print(f"Error importing dialogchain: {e}")
        print("Make sure you have installed all required dependencies.")
        print("Try running: pip install -e ../../python")
        sys.exit(1)

def run_example(config_path):
    """Run a DialogChain example from a YAML config file."""
    from dialogchain.cli import run as run_cli
    
    # Convert to absolute path
    config_path = Path(config_path).absolute()
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    
    print(f"Running example: {config_path.name}")
    print("-" * 50)
    
    # Run the example
    try:
        run_cli(["--config", str(config_path)])
    except KeyboardInterrupt:
        print("\nExample stopped by user")
    except Exception as e:
        print(f"Error running example: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run DialogChain examples")
    parser.add_argument(
        "config",
        nargs="?",
        default="timer_to_log.yaml",
        help="Path to the YAML config file (default: timer_to_log.yaml)",
    )
    args = parser.parse_args()
    
    # Set up the environment
    setup_environment()
    
    # Run the specified example
    run_example(args.config)

if __name__ == "__main__":
    main()
