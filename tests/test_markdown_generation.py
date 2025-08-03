import hashlib


class TestMarkdownGenerator:

    def test_script_hash(self, temp_files: dict, test_script_hash: str):

        with open(temp_files["script_file"], "rb") as file:
            current_hash = str(hashlib.sha256(file.read()).hexdigest())
            assert current_hash == test_script_hash, "Test script has changed somehow"

    def test_markdown_file(self, temp_files: dict, markdown_temp_file_hash: str):

        with open(temp_files["markdown_file"], "rb") as file:
            current_hash = str(hashlib.sha256(file.read()).hexdigest())
            assert (
                current_hash == markdown_temp_file_hash
            ), "Markdown file hash has changed"
