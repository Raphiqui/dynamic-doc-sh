import hashlib
import os

from logging_config import logger


class HashHandler:
    """
    Hashing process similar to the `.lock` file in JavaScript
    or `.in` in python
    """

    def __init__(self, script_path: str, previous_hash_path: str = "previous_hash.txt"):
        self.script_path = script_path
        self.previous_hash_path = previous_hash_path

    def _get_current_target_hash(self, path: str) -> str:
        """
        Get the current file hash to potentially be stored as new one
        """

        if not os.path.exists(path):
            logger.error(f"The file {path} doesn't exist")
            return ""

        with open(path, "rb") as f:
            return str(hashlib.sha256(f.read()).hexdigest())

    def _get_previous_target_hash(self, path: str):
        """
        Get the previous hash, usually from `previous_hash.txt`
        """

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
        """
        Compare the 2 hashes to trigger or not the creation process.
        Basically it's not wanted to start the process if nothing changed
        """
        current_hash = self._get_current_target_hash(self.script_path)
        previous_hash = self._get_previous_target_hash(self.previous_hash_path)

        target_has_changed = current_hash != previous_hash

        if target_has_changed:
            self._write_new_target_hash()

        return target_has_changed
