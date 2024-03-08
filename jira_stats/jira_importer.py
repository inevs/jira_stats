import json
import yaml
from typing import Any, Dict, List

from jira_stats import SUCCESS, JSON_ERROR, READ_ERROR, T_TYPES, UNDEFINED


class IssueStateTransition:
    def __init__(self, timestamp: str, from_state: str, to_state: str, transition_type: str = "not defined"):
        self.transition_type = transition_type
        self.to_state = to_state
        self.from_state = from_state
        self.timestamp = timestamp


class JiraIssue:
    def __init__(self, key: str, type: str, created: str, resolved: str, status: str,
                 transitions: [IssueStateTransition]):
        self.key = key
        self.type = type
        self.created = created
        self.resolved = resolved
        self.status = status
        self.transitions = transitions


class ImportData:
    def __init__(self, issues: List[JiraIssue], error: int):
        self.error = error
        self.issues = issues


class Importer:

    def __init__(self, config = Dict):
        try:
            with open('config.yaml') as f:
                self._config = yaml.load(f, Loader=yaml.FullLoader)
        except OSError:
            self._config = config

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

    def get_transition_type_for(self, status_change) -> str:
        to_state = status_change["toString"]
        for t in T_TYPES:
            if t == T_TYPES[UNDEFINED]:
                continue
            transition_states = self._config[T_TYPES[t]]
            if transition_states.count(to_state) > 0:
                return T_TYPES[t]
        return T_TYPES[UNDEFINED]

    def convert_issue(self, issue: Dict[str, Any]) -> JiraIssue:
        transitions = []
        changelog_histories = issue["changelog"]["histories"]
        for changelog_history in changelog_histories:
            created = changelog_history["created"]
            status_changes = list(filter(lambda item: item["field"] == "status", changelog_history["items"]))
            if len(status_changes) > 0:
                for status_change in status_changes:
                    transitions.append(self.convert_transition(created, status_change))
        return JiraIssue(
            key=issue["key"],
            type=issue["fields"]["issuetype"]["name"],
            created=issue["fields"]["created"],
            resolved=issue["fields"]["resolutiondate"],
            status=issue["fields"]["status"]["name"],
            transitions=transitions
        )

    def convert_transition(self, created, status_change):
        transition = IssueStateTransition(timestamp=created, from_state=status_change["fromString"],
                                          to_state=status_change["toString"],
                                          transition_type=self.get_transition_type_for(status_change))
        return transition

