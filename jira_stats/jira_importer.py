import json
from typing import Any, Dict, List, NamedTuple

from jira_stats import SUCCESS, JSON_ERROR, READ_ERROR


class ImportData(NamedTuple):
    issues: List[Dict[str, Any]]
    error: int

class Importer:

    def __init__(self):
        pass


    def load_data(self, file: str) -> ImportData:
        try:
            with open(file) as json_data:
                try:
                    issues = json.load(json_data)["issues"]
                    return ImportData(issues, SUCCESS)
                except json.JSONDecodeError:
                    return ImportData([], JSON_ERROR)
        except OSError:
            return ImportData([], READ_ERROR)
