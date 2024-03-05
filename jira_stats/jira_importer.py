import json
from typing import Any, Dict, List, NamedTuple

from jira_stats import SUCCESS, JSON_ERROR, READ_ERROR


class IssueStateTransition:
    def __init__(self, timestamp: str, from_state: str, to_state: str):
        self.to_state = to_state
        self.from_state = from_state
        self.timestamp = timestamp

class JiraIssue:
    def __init__(self, key: str, type: str, created: str, resolved: str, status: str, transitions: [IssueStateTransition]):
        self.key = key
        self.type = type
        self.created = created
        self.resolved = resolved
        self.status = status
        self.transitions = transitions

    def __eq__(self, other):
        if not isinstance(other, JiraIssue):
            return NotImplemented
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

class ImportData:
    def __init__(self, issues: List[JiraIssue], error: int):
        self.error = error
        self.issues = issues


class Importer:

    def __init__(self):
        pass

    def load_data(self, file: str) -> ImportData:
        try:
            with open(file) as json_data:
                try:
                    issues = json.load(json_data)["issues"]
                    converted_issues = list(map(self.convert_issue, issues))
                    return ImportData(converted_issues, SUCCESS)
                except json.JSONDecodeError:
                    return ImportData([], JSON_ERROR)
        except OSError:
            return ImportData([], READ_ERROR)

    @staticmethod
    def convert_issue(issue: Dict[str, Any]) -> JiraIssue:
        transitions = []
        changelog_histories = issue["changelog"]["histories"]
        for changelog_history in changelog_histories:
            created = changelog_history["created"]
            status_changes = list(filter(lambda item: item["field"] == "status", changelog_history["items"]))
            if len(status_changes) > 0:
                for status_change in status_changes:
                    transitions.append(IssueStateTransition(
                        timestamp=created,
                        from_state=status_change["fromString"],
                        to_state=status_change["toString"]
                    ))
        return JiraIssue(
            key=issue["key"],
            type=issue["fields"]["issuetype"]["name"],
            created=issue["fields"]["created"],
            resolved=issue["fields"]["resolutiondate"],
            status=issue["fields"]["status"]["name"],
            transitions=transitions
        )
