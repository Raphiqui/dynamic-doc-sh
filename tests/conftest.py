import os
import tempfile
from pathlib import Path

import pytest

from hash_handling import HashHandler


@pytest.fixture
def temp_files():
    """Create temporary files for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    script_file = temp_dir / "test_script.sh"
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

    yield {"temp_dir": temp_dir, "script_file": script_file, "hash_file": hash_file}

    # Cleanup
    try:
        if os.path.exists(script_file):
            os.remove(script_file)
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
def previous_test_script_hash():

    return "a0bc2965e137ce31edfc97a9ab8faaa44119d6edaa27747135028a2da8250afd"
