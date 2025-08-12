import argparse
import re
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from hash_handling import HashHandler


class DocGenerator:
    """ """

    def __init__(
        self,
    ) -> None:
        """
        For now just the .sh scripts are available
        Script path is basically where is the script you want to document
        Doc template path in case some other templates are available
        """

        self.parser = argparse.ArgumentParser(description="Documentation generator")

        self.parser.add_argument(
            "--script_path",
            type=str,
            default="test.sh",
            help="The default script to be documented",
        )
        self.parser.add_argument(
            "--doc_template_path",
            type=str,
            default="doc_template.md.j2",
            help="Jinja template to generate the documentation",
        )
        self.parser.add_argument(
            "--previous_hash_path",
            type=str,
            default="previous_hash.txt",
            help="Hahs of the previous documentation generated",
        )

        self.args = self.parser.parse_args()

        self.script_path = self.args.script_path
        self.doc_template_path = self.args.doc_template_path
        self.previous_hash_path = self.args.previous_hash_path
        self.sequences = []
        self._read_file()
        self._env = Environment(loader=FileSystemLoader("templates"))
        self._template = self._env.get_template(self.doc_template_path)
        self.hash_handler = HashHandler(self.script_path, self.previous_hash_path)

    def check_sequence(self, sequence: dict) -> bool:
        """
        Check that the current sequence has at least the required keys
        to be considered as a bare minimum sequence.
        """

        keys = sequence.keys()

        if "read" not in keys:
            return False

        if "doc" not in keys:
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
            sequence[key_name] = match.group(1).strip()

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
                    self._hydrate_sequence(sequence, r":(.*)", line, "doc")

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


if __name__ == "__main__":
    generator = DocGenerator()
    generator.generate()
