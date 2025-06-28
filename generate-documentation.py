import os
import re
import hashlib

from jinja2 import Environment, FileSystemLoader
from datetime import datetime

SCRIPT_NAME = "test.sh"


class DocGenerator:
    """ """

    def __init__(self) -> None:
        self.sequences = []
        self._read_file()
        self._env = Environment(loader=FileSystemLoader("templates"))
        self._template = self._env.get_template("doc_template.md.j2")

    def check_sequence(self, sequence: dict) -> bool:
        """
        Check that the current sequence has at least the required keys
        to be considered as a bare minimum sequence
        """

        return "echo" in sequence.keys()

    def _hydrate_sequence(
        self, sequence: dict, pattern: str, line: str, key_name: str
    ) -> None:

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

        with open(SCRIPT_NAME, "r") as file:
            lines = file.readlines()
            sequence = {}

            for line in lines:
                if "@doc" in line:
                    # pattern = r"\"(.*?)\""
                    self._hydrate_sequence(sequence, r":(.*)", line, "question")

                if "@default" in line:
                    self._hydrate_sequence(sequence, r":(.*)", line, "default")

                if "echo" in line:
                    self._hydrate_sequence(sequence, r'"(.*?)"', line, "echo")

        is_sequence_valid = self.check_sequence(sequence)

        if is_sequence_valid:
            self.sequences.append(sequence)
        else:
            print(f"Please check this sequence, it might be wrong: {sequence}")

    def _get_current_target_hash(self, path: str) -> hashlib.sha256:
        try:
            os.path.exists(path)
        except Exception as e:
            raise e

        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _get_previous_target_hash(self, path: str):
        previous_hash = ""
        if not os.path.exists(path):
            return previous_hash

        with open(path, "rb") as file:
            lines = file.readlines()
            for line in lines:
                previous_hash += line.decode("utf-8")

            return previous_hash

    def _write_new_target_hash(self) -> None:
        try:
            os.remove("previous_hash.txt")
        except Exception as e:
            print(e)
            pass

        with open("previous_hash.txt", "w") as file:
            file.write(self._get_current_target_hash(SCRIPT_NAME))

    def _target_hash_changed(self) -> bool:
        current_hash = self._get_current_target_hash(SCRIPT_NAME)
        previous_hash = self._get_previous_target_hash("previous_hash.txt")

        target_has_changed = current_hash != previous_hash
        print(target_has_changed)

        if target_has_changed:
            self._write_new_target_hash()

        return target_has_changed

    def generate(self) -> None:

        if not self._target_hash_changed():
            return

        output = self._template.render(
            script_name=SCRIPT_NAME,
            prompts=self.sequences,
            metadata={"timestamp": datetime.now().isoformat()},
        )

        with open(f"{SCRIPT_NAME}-doc.md", "w") as file:
            file.write(output)


generator = DocGenerator()
generator.generate()
