import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from dynamic_doc_sh.logging_config import logger

import pytest

from dynamic_doc_sh.hash_handling import HashHandler


@pytest.fixture
def temp_files():
    """Create temporary files for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    hash_file = temp_dir / "previous_hash.txt"

    yield {
        "temp_dir": temp_dir,
        "hash_file": hash_file,
    }

    # Cleanup
    try:
        if os.path.exists(hash_file):
            os.remove(hash_file)
        shutil.rmtree(temp_dir)
    except OSError as e:
        logger.error(e)
        pass


@pytest.fixture
def hash_handler(temp_files):
    """Create HashHandler instance with temporary file"""
    return HashHandler(
        script_path=temp_files["script_file"],
        previous_hash_path=temp_files["hash_file"],
    )


@pytest.fixture
def generator(temp_files):
    """Create DocGenerator with custom template path as bash command line simulation"""

    test_args = [
        "generate_documentation.py",
        "--script_path",
        str(Path(__file__).parent / "default.sh"),
        "--previous_hash_path",
        str(Path(__file__).parent / "default_previous_hash_path.txt"),
        "--output_path",
        str(temp_files["temp_dir"] / "default"),
        "--debug",
        str(True),
    ]

    with patch.object(sys, "argv", test_args):
        from dynamic_doc_sh.generate_documentation import DocGenerator

        yield DocGenerator().generate()


@pytest.fixture
def default_hash():
    return "652adc8aec8bb70ee9ba3a822c575d713a8a1e037e886ce94b7980c0fc9321ea"
