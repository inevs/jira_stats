from pathlib import Path
from typing import List

import typer

from jira_stats import ERRORS
from jira_stats.database import DatabaseHandler, DEFAULT_DB_FILE_PATH
from jira_stats.jira_importer import Importer, JiraIssue

app = typer.Typer()


def make_unique(combined_issues) -> List:
    unique_issues = []
    for issue in combined_issues:
        if issue not in unique_issues:
            unique_issues.append(issue)
    return unique_issues


@app.command()
def load(
        file: str,
        append: bool = typer.Option(False, "--append", "-a")
):
    """load data from jira export"""
    viewer = Importer()
    fileImport = viewer.load_data(file)
    if fileImport.error:
        typer.secho(f"error loading file {str}", fg=typer.colors.RED)
        typer.Exit(1)

    typer.echo(f"Imported {len(fileImport.issues)} issues")

    # save issues in database
    database = DatabaseHandler(Path(DEFAULT_DB_FILE_PATH))

    if append:
        read = database.read_issues()
        if read.error:
            typer.secho("Could not read old issues from db.")
        fileImport.issues.extend(read.issues)

    result = database.write_issues(fileImport.issues)
    if result.error:
        typer.secho(f"Error writing to database {ERRORS[result.error]}")
        typer.Exit(1)


@app.command()
def clean(force: bool = typer.Option(False, "--force", "-f", prompt="Are you sure you want to clean all data?")):
    """clean previously loaded data"""
    if not force:
        return

    database = DatabaseHandler(Path(DEFAULT_DB_FILE_PATH))
    result = database.write_issues([])
    if result.error:
        typer.secho(f"Error cleaning database {ERRORS[result.error]}")


@app.command()
def stats():
    """show some statistics in the data"""
    issues = [JiraIssue(key="1235", type="Bug", status="Done", created="", resolved="", transitions=[])]
    issue2 = JiraIssue(key="1235", type="Story", status="Done", created="", resolved="", transitions=[])

    if issue2 not in issues:
        typer.secho(f"issue2 not in issues", fg=typer.colors.GREEN)
    else:
        typer.secho(f"issue2 in issues", fg=typer.colors.RED)

@app.command()
def version():
    pass
