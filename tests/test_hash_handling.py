from hash_handling import HashHandler
import hashlib


class TestHashHandler:

    def test_instance_is_valid(self, hash_handler: HashHandler):
        assert hash_handler.script_path is not None, "script_path must not be empty"
        assert (
            hash_handler.previous_hash_path is not None
        ), "previous_hash_path must not be empty"


class TestGenerator:

    def test_script(self, temp_files, test_script_hash):

        with open(temp_files["script_file"], "rb") as file:
            current_hash = str(hashlib.sha256(file.read()).hexdigest())
            assert current_hash == test_script_hash, "Test script has changed somehow"
