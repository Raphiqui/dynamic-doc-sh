import os
import re
import hashlib

from jinja2 import Environment, FileSystemLoader
from datetime import datetime

SCRIPT_NAME = "test.sh"

class DocGenerator:
    """
    Point is to check that the target file specified (the `.sh` script)
    has somehow changed using the hash of the file.

    If it did then perform the creation of a new one. Just delete if exists
    already or create. Then, read it and create the prompts lines. Then use the template
    from jinja2 to generate the documentation.
    """

    def __init__(self) -> None:
        self.sequences = []
        self._read_file()
        self._env = Environment(loader=FileSystemLoader("templates"))
        self._template = self._env.get_template("doc_template.md.j2")

    def check_sequence(self, sequence: dict) -> bool:
        """
        Check that the current sequence has the correct values or at least the one required 
        if not just erase it due to some and print a log
        """

        return "echo" in sequence.keys()

    def _hydrate_sequence(self, sequence: dict, pattern: str, line: str, key_name: str) -> None:
        
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

    def generate(self) -> None:

        output = self._template.render(
            script_name=SCRIPT_NAME,
            prompts=self.sequences,
            metadata={"timestamp": datetime.now().isoformat()},
        )

        with open(f"{SCRIPT_NAME}-doc.md", "w") as file:
            file.write(output)

generator = DocGenerator()
generator.generate()

"""
    def _get_hash(self) -> hashlib.sha256:

        try:
            os.path.exists(path)
        except Exception as e:
            print(e)

        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()


        print(os.path.exists("test.sh"))
        print(hash_file_content("test.sh"))
"""

