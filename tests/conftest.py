import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from logging_config import logger

import pytest

from generate_documentation import DocGenerator
from hash_handling import HashHandler


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
    """Create DocGenerator with custom template path"""

    test_args = [
        "generate_documentation.py",
        "--script_path",
        str(Path(__file__).parent / "default.sh"),
        "--previous_hash_path",
        str(temp_files["hash_file"]),
        "--output_path",
        str(temp_files["temp_dir"]),
    ]

    with patch.object(sys, "argv", test_args):
        from generate_documentation import DocGenerator

        yield DocGenerator()


@pytest.fixture
def markdown_temp_file_hash():
    return "0083500972854b8b48528f35d79759a3991ef8209110197f787a53b58b5d1de7"


@pytest.fixture
def test_script_hash():
    return "a0bc2965e137ce31edfc97a9ab8faaa44119d6edaa27747135028a2da8250afd"
