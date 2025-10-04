from dynamic_doc_sh.logging_config import logger
import re
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from importlib.resources import files

from dynamic_doc_sh.hash_handling import HashHandler


class DocGenerator:
    """
    Main class of this project used to generate the documentation according to what have been specified as arguments.
    """

    def __init__(
        self,
        script_path: str,
        previous_hash_path: str,
        output_path: str,
        debug: bool,
        script_language: str = "bash",
    ) -> None:
        """
        For now just the .sh scripts are available
        Script path is basically where is the script you want to document
        Doc template path in case some other templates are available
        """
        self.j2_templates_mapping = {"bash": "doc_template.md.j2"}
        self.script_path = script_path
        self.script_language = script_language
        self.previous_hash_path = previous_hash_path
        self.output_path = output_path
        self.sequences = []
        self._read_file()
        self.debug = debug
        self._template = self._build_template()
        self.hash_handler = HashHandler(
            self.script_path, self.previous_hash_path, self.debug
        )

    def _build_template(self):
        """
        Build template according to specified language, bash, python, JavaScript, ...
        """

        try:
            doc_template_path = self.j2_templates_mapping[self.script_language]
        except Exception as e:
            logger.error(f"Template for language {self.script_language} doesn't exist")
            raise

        template_path = files("dynamic_doc_sh") / "templates"
        environment = Environment(loader=FileSystemLoader(str(template_path)))
        return environment.get_template(doc_template_path)

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

        try:
            with open(f"{self.output_path}-doc.md", "w") as file:
                file.write(output)
        except Exception as e:
            logger.error(e)
