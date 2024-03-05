import json
from pathlib import Path
from typing import List, Dict, Any, NamedTuple

from jira_stats import SUCCESS, DB_WRITE_ERROR, JSON_ERROR, DB_READ_ERROR
from jira_stats.jira_importer import JiraIssue

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + "issue_db.json"
)


class DBResponse(NamedTuple):
    issues: List[JiraIssue]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def write_issues(self, issues: List[JiraIssue]) -> DBResponse:
        print("writing issues to database " + str(self._db_path))
        try:
            with self._db_path.open("w") as db:
                json.dump(issues, db, indent=4, default=vars)
            return DBResponse(issues, SUCCESS)
        except OSError:
            return DBResponse(issues, DB_WRITE_ERROR)

    def read_issues(self) -> DBResponse:
        print("reading issues from database " + str(self._db_path))
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
