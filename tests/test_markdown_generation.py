import subprocess
import hashlib
from dynamic_doc_sh.logging_config import logger
from dynamic_doc_sh.generate_documentation import DocGenerator


class TestMarkdownGenerator:

    def test_generator(
        self, temp_files: dict, generator: DocGenerator, default_hash: str
    ):
        """
        If the default script tested change then take the new hash generated and printed then update the `default_hash`.
        Be cautious to check that the content is the one expected.
        """

        target_dir = temp_files["temp_dir"]

        result = subprocess.run(["ls", target_dir], capture_output=True, text=True)

        assert result.returncode == 0
        files = result.stdout.strip().split("\n")

        logger.debug(f"Files in {target_dir}: {files}")

        with open(f"{target_dir}/{files[0]}", "rb") as file:
            content = file.read()
            file_hash = str(hashlib.sha256(content).hexdigest())
            logger.debug(f"Content of the file: {content}, hash is: {file_hash}")

            assert file_hash == default_hash
