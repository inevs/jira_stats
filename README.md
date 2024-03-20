# Load an export from Jira and show some flow metrics

run the app with

```
python -m jiraviewer --help
```

Export date from jira with:
i.e. find the sprints you want to export

```
project="YOUR_JIRA_PROJECT" and sprint in(2611,2612)
```
then export with
```
https://YOUR_JIRA_INSTANCE/rest/agile/1.0/board/YOUR_BOARD_ID/issue?expand=changelog&startAt=0&maxResults=1000&jql=YOUR_JQL_QUERY
```

```
python -m jira_stats load issue.json
```

If you need to split the export then you can append issues to the issue database

```
python -m jira_stats load issue-1.json -a
```

And if you want to restart from fresh you should clean the databse

```
python -m jira_stats clean
```
