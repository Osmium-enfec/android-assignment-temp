"""
Test Configuration for Assignment 1

This file defines how pytest should be configured for running
Android layout validation tests.
"""

import os
import sys
from pathlib import Path

# Add submission path to Python path
SUBMISSION_DIR = Path('/app/submission')
if SUBMISSION_DIR.exists():
    sys.path.insert(0, str(SUBMISSION_DIR))

# Test markers
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "xml: mark test as XML validation test"
    )
    config.addinivalue_line(
        "markers", "layout: mark test as layout structure test"
    )
