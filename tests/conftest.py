import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from generate_documentation import DocGenerator
from hash_handling import HashHandler


@pytest.fixture
def temp_files():
    """Create temporary files for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    script_file = temp_dir / "test_script.sh"
    markdown_file = temp_dir / "markdown_file.md"
    hash_file = temp_dir / "previous_hash.txt"

    # Create a test script file with content
    script_content = """
        #!/bin/bash

        set -e

        # @doc: Developer settings are used in development mode, don't use it if you deploy in production
        # @default: yes
        read -e -i yes -p "Use Developer Settings [YES/no]" developer_settings
        echo "Developer Settings: $developer_settings"
    """

    script_file.write_text(script_content)

    markdown_content = """
    # Documentation for test.sh

    Developer settings are used in development mode, don't use it if you deploy in production
    - Use Developer Settings [YES/no]:yes
    """

    markdown_file.write_text(markdown_content)

    yield {
        "temp_dir": temp_dir,
        "script_file": script_file,
        "hash_file": hash_file,
        "markdown_file": markdown_file,
    }

    # Cleanup
    try:
        if os.path.exists(script_file):
            os.remove(script_file)
        if os.path.exists(markdown_file):
            os.remove(markdown_file)
        if os.path.exists(hash_file):
            os.remove(hash_file)
        os.rmdir(temp_dir)
    except OSError:
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
