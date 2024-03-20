import json
import yaml
import re
from typing import Any, Dict, List

from jira_stats import SUCCESS, JSON_ERROR, READ_ERROR, T_TYPES, UNDEFINED


class IssueStateTransition:
    def __init__(self, timestamp: str, from_state: str, to_state: str, transition_type: str = "not defined"):
        self.transition_type = transition_type
        self.to_state = to_state
        self.from_state = from_state
        self.timestamp = timestamp


class IssueBlockedComment:

    def __init__(self, reason: str, created_date: str, is_unblocker: bool = False):
        self.reason = reason
        self.created_date = created_date
        self.is_unblocker = is_unblocker


class JiraIssue:
    def __init__(self, key: str, issue_type: str, created: str, resolved: str, status: str,
                 transitions=None, blockers=None):
        if blockers is None:
            blockers = []
        if transitions is None:
            transitions = []
        self.blockers = blockers
        self.key = key
        self.issue_type = issue_type
        self.created = created
        self.resolved = resolved
        self.status = status
        self.transitions = transitions


class ImportData:
    def __init__(self, issues: List[JiraIssue], error: int):
        self.error = error
        self.issues = issues


class Importer:

    def __init__(self, config=Dict):
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
        transitions = self.get_transitions(issue)
        blocker_comments = self.get_blockers(issue)
        return JiraIssue(
            key=issue["key"],
            issue_type=issue["fields"]["issuetype"]["name"],
            created=issue["fields"]["created"],
            resolved=issue["fields"]["resolutiondate"],
            status=issue["fields"]["status"]["name"],
            transitions=transitions,
            blockers=blocker_comments
        )

    def get_blockers(self, issue):
        blocker_comments = []
        comments = issue["fields"]["comment"]["comments"]
        for comment in comments:
            body: str = comment["body"]
            if body.startswith("(flag)"):
                reason = ''.join(body.splitlines()[2:])
                blocker_comment = IssueBlockedComment(reason=reason, created_date=comment["created"])
                blocker_comments.append(blocker_comment)
            if body.startswith("(flagoff)"):
                reason = ''.join(body.splitlines()[2:])
                blocker_comment = IssueBlockedComment(reason=reason, created_date=comment["created"], is_unblocker=True)
                blocker_comments.append(blocker_comment)
        return blocker_comments

    def get_transitions(self, issue):
        transitions = []
        changelog_histories = issue["changelog"]["histories"]
        for changelog_history in changelog_histories:
            created = changelog_history["created"]
            status_changes = list(filter(lambda item: item["field"] == "status", changelog_history["items"]))
            if len(status_changes) > 0:
                for status_change in status_changes:
                    transitions.append(self.convert_transition(created, status_change))
        return transitions

    def convert_transition(self, created, status_change):
        transition = IssueStateTransition(timestamp=created, from_state=status_change["fromString"],
                                          to_state=status_change["toString"],
                                          transition_type=self.get_transition_type_for(status_change))
        return transition
