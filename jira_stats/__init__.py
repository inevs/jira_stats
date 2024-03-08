__app_name__ = "jira_stats"
__version__ = "0.1.0"


(
    SUCCESS,
    READ_ERROR,
    JSON_ERROR,
    DB_WRITE_ERROR,
    DB_READ_ERROR,
) = range(5)


ERRORS = {
    READ_ERROR: "file read error",
    JSON_ERROR: "json related error",
    DB_WRITE_ERROR: "error writing to database",
    DB_READ_ERROR: "error reading from database"
}

(
    OPEN,
    PROGRESS,
    DONE,
    UNDEFINED
) = range(4)

T_TYPES = {
    OPEN: "open",
    PROGRESS: "in progress",
    DONE: "done",
    UNDEFINED: "not defined"
}