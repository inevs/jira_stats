from typing import List
from jira_stats.jira_importer import JiraIssue

import pandas as pd

class BasicStats:
    def __init__(self, issue_count: int):
        self.issue_count = issue_count


class Analyser:

    def __init__(self, issues: List[JiraIssue]):
        self.issues = issues
        self.pd_issues = pd.DataFrame(self.issues)


    def get_basic_stats(self) -> BasicStats:
        _issue_count = self.pd_issues.count("rows")
        print(self.pd_issues["status"].value_counts())

        return BasicStats(issue_count=0)