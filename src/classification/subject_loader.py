import json
from pathlib import Path
from typing import Dict


class SubjectLoader:

    @staticmethod
    def load(config_path: str = None) -> Dict[str, str]:

        if config_path is None:

            config_path = str(
                Path(__file__).resolve().parent.parent.parent
                / "config"
                / "medical_subjects.json"
            )

        path = Path(config_path)

        if not path.exists():

            raise FileNotFoundError(
                f"Category configuration file not found: "
                f"{path.resolve()}"
            )

        with open(path, "r") as f:

            categories: Dict[str, str] = json.load(f)

        return categories
