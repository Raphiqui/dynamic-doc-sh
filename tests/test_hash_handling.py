from hash_handling import HashHandler


class TestHashHandler:

    def test_instance_is_valid(self, hash_handler: HashHandler):
        assert hash_handler.script_path is not None, "script_path must not be empty"
        assert (
            hash_handler.previous_hash_path is not None
        ), "previous_hash_path must not be empty"
