import os
import re
import hashlib
import logging

from jinja2 import Environment, FileSystemLoader
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class HashHandler:
    """
    """

    def __init__(self, script_path: str, previous_hash_path: str = "previous_hash.txt"):
        self.script_path = script_path
        self.previous_hash_path = previous_hash_path

    def _get_current_target_hash(self, path: str) -> str:
        if not os.path.exists(path):
            logger.error(f"The file {path} doesn't exist")
            return ""

        with open(path, "rb") as f:
            return str(hashlib.sha256(f.read()).hexdigest())

    def _get_previous_target_hash(self, path: str):
        previous_hash = ""
        if not os.path.exists(path):
            logger.error(f"The file {path} doesn't exist")
            return previous_hash

        with open(path, "rb") as file:
            lines = file.readlines()
            for line in lines:
                previous_hash += line.decode("utf-8")

            return previous_hash

    def _write_new_target_hash(self) -> None:
        try:
            os.remove(self.previous_hash_path)
        except Exception as e:
            logger.error(f"Error while removing the file: {e}")

        with open(self.previous_hash_path, "w") as file:
            file.write(self._get_current_target_hash(self.script_path))

    @property
    def target_hash_changed(self) -> bool:
        current_hash = self._get_current_target_hash(self.script_path)
        previous_hash = self._get_previous_target_hash(self.previous_hash_path)

        target_has_changed = current_hash != previous_hash

        if target_has_changed:
            self._write_new_target_hash()

        return target_has_changed


class DocGenerator:
    """ """

    def __init__(
        self,
        script_path: str,
        doc_template_path: str = "doc_template.md.j2",
        previous_hash_path: str = "previous_hash.txt",
    ) -> None:
        self.script_path = script_path
        self.doc_template_path = doc_template_path
        self.previous_hash_path = previous_hash_path
        self.sequences = []
        self._read_file()
        self._env = Environment(loader=FileSystemLoader("templates"))
        self._template = self._env.get_template(self.doc_template_path)
        self.hash_handler = HashHandler(script_path, previous_hash_path)

    def check_sequence(self, sequence: dict) -> bool:
        """
        Check that the current sequence has at least the required keys
        to be considered as a bare minimum sequence
        """

        keys = sequence.keys()

        if "read" not in keys:
            return False

        if "default" not in keys:
            return False

        return True

    def _hydrate_sequence(
        self, sequence: dict, pattern: str, line: str, key_name: str
    ) -> None:
        """
        Update the sequence with tags found in the script
        """

        match = re.search(pattern, line)
        if match and key_name not in sequence:
            sequence[key_name] = match.group(1)

    def _read_file(self) -> None:
        """
        Simple file reader to read the .sh file and
        possibly parse it or gather the reading inputs found

        Let's assume we have some decorators in the same model of swagger
        So, there is a #question decorator, which is for now a comment but whatever
        in the .sh file, whatever comes after must be
        processed as the question until reaching ...
        """

        with open(self.script_path, "r") as file:
            lines = file.readlines()
            sequence = {}

            for line in lines:
                if "@doc" in line:
                    # pattern = r"\"(.*?)\""
                    self._hydrate_sequence(sequence, r":(.*)", line, "question")

                if "@default" in line:
                    self._hydrate_sequence(sequence, r":(.*)", line, "default")

                if "read" in line:
                    self._hydrate_sequence(sequence, r'"(.*?)"', line, "read")

                is_sequence_valid = self.check_sequence(sequence)

                if is_sequence_valid:
                    self.sequences.append(sequence)
                    sequence = {}

    def generate(self) -> None:

        if not self.hash_handler.target_hash_changed:
            return

        output = self._template.render(
            script_name=self.script_path,
            prompts=self.sequences,
            metadata={"timestamp": datetime.now().isoformat()},
        )

        with open(f"{self.script_path}-doc.md", "w") as file:
            file.write(output)


generator = DocGenerator("test.sh")
generator.generate()
