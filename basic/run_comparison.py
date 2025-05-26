#!/usr/bin/env python3
"""
Simple comparison between Python and YAML DSL implementations.
"""
import time
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the execution time."""
    start_time = time.time()
    try:
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        return time.time() - start_time
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return None

def main():
    # Paths
    base_dir = Path(__file__).parent
    python_script = base_dir / "basic_usage.py"
    yaml_config = base_dir / "basic_usage_dsl.yaml"
    python_dir = base_dir.parent / "python"
    
    print("=== DialogChain Implementation Comparison ===\n")
    
    # Run Python implementation
    print("1. Running Python implementation...")
    py_time = run_command([sys.executable, str(python_script)])
    if py_time is not None:
        print(f"   → Completed in {py_time:.2f} seconds\n")
    
    # Run YAML DSL implementation
    print("2. Running YAML DSL implementation...")
    dsl_time = run_command(
        [sys.executable, "-m", "dialogchain.cli", "run", "--config", str(yaml_config)],
        cwd=python_dir
    )
    if dsl_time is not None:
        print(f"   → Completed in {dsl_time:.2f} seconds\n")
    
    # Print comparison
    if py_time is not None and dsl_time is not None:
        print("\n=== Comparison Results ===")
        print(f"Python implementation: {py_time:.2f} seconds")
        print(f"YAML DSL implementation: {dsl_time:.2f} seconds")
        
        time_saved = py_time - dsl_time
        if time_saved > 0:
            print(f"\nTime saved with YAML DSL: {time_saved:.2f} seconds ({time_saved/py_time*100:.1f}% faster)")
        else:
            print(f"\nYAML DSL was {abs(time_saved):.2f} seconds slower than Python implementation")
        
        # Lines of code comparison
        py_loc = sum(1 for _ in open(python_script, 'r') if _.strip() and not _.lstrip().startswith('#'))
        yaml_loc = sum(1 for _ in open(yaml_config, 'r') if _.strip() and not _.lstrip().startswith('#'))
        
        print("\nCode complexity:")
        print(f"Python implementation: {py_loc} lines of code")
        print(f"YAML DSL implementation: {yaml_loc} lines of code")
        print(f"Reduction: {py_loc - yaml_loc} lines ({(1 - yaml_loc/py_loc)*100:.1f}% less code)")
    
    print("\nNote: The YAML DSL implementation includes the overhead of the DialogChain framework.")
    print("For simple examples, the Python implementation might be faster, but the YAML DSL")
    print("becomes more efficient as the complexity of the workflow increases.")

if __name__ == "__main__":
    main()
