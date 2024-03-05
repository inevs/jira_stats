__app_name__ = "jira_stats"
__version__ = "0.1.0"


(
    SUCCESS,
    READ_ERROR,
    JSON_ERROR,
) = range(3)


ERRORS = {
    READ_ERROR: "file read error",
    JSON_ERROR: "json related error",
}