#!/usr/bin/env python3
"""
Simple test runner for FIFO matching logic

Usage:
    python test/run_tests.py
    
    Or from project root:
    python -m test.run_tests
"""

import sys
import os

# Add parent directory to path to import from test package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from test.test_fifo_matching import run_all_tests

if __name__ == "__main__":
    passed, failed = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)
