import json
import os.path
from dataclasses import asdict

import config


class JSONFileWriter:
    """
    Utility class for writing data to a JSON file.

    Attributes:
        file_name (str): The name of the JSON file.
    """

    def __init__(self, file_name: str) -> None:
        """
        Initializes a JSONFileWriter instance.

        Args:
            file_name (str): The name of the JSON file.
        """
        self.file_name = file_name

    def _get_path_to_file(self) -> str:
        """
        Constructs the path to the JSON file.

        Returns:
            str: The path to the JSON file.
        """
        return os.path.join(config.FILE_PATH, self.file_name)

    def write_in_json_file(self, data: list) -> None:
        """
        Writes data to the JSON file.

        Args:
            data (list): The data to write to the JSON file.
        """
        data_as_dicts = [asdict(record) for record in data]

        with open(self._get_path_to_file(), "w", encoding="utf-8") as file:
            json.dump(data_as_dicts, file, ensure_ascii=False, indent=4)
