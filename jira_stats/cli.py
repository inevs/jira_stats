from pathlib import Path
from typing import List

import typer

from jira_stats import ERRORS
from jira_stats.analyser import Analyser
from jira_stats.database import DatabaseHandler, DEFAULT_DB_FILE_PATH
from jira_stats.jira_importer import Importer


app = typer.Typer()


def make_unique(combined_issues) -> List:
    unique_issues = []
    for issue in combined_issues:
        if issue not in unique_issues:
            unique_issues.append(issue)
    return unique_issues


def get_database():
    return DatabaseHandler(Path(DEFAULT_DB_FILE_PATH))


@app.command()
def load(
        file: str,
        append: bool = typer.Option(False, "--append", "-a")
):
    """load data from jira export"""
    importer = Importer()
    fileImport = importer.load_data(file)
    if fileImport.error:
        typer.secho(f"error loading file {str}", fg=typer.colors.RED)
        typer.Exit(1)

    typer.echo(f"Imported {len(fileImport.issues)} issues")

    # save issues in database
    database = get_database()

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

    typer.echo(f"cleaning database in {get_database()._db_path}")
    database = DatabaseHandler(Path(DEFAULT_DB_FILE_PATH))
    result = database.write_issues([])
    if result.error:
        typer.secho(f"Error cleaning database {ERRORS[result.error]}")


@app.command()
def stats():
    """show some statistics in the data"""
    data = get_database().read_issues()
    if data.error:
        typer.secho(f"Error reading database: {ERRORS[data.error]}")

    analyser = Analyser(issues=data.issues)
    stats = analyser.get_basic_stats()
    typer.echo(f"{stats.issue_count} issues")


@app.command()
def blocks():
    data = get_database().read_issues()
    if data.error:
        typer.secho(f"Error reading database: {ERRORS[data.error]}")
    issues = data.issues
    for issue in issues:
        blockers = issue["blockers"]
        for blocker in blockers:
            reason = blocker["reason"]
            typer.echo(reason)

@app.command()
def config():
    importer = Importer()
    importer.foo()  # type: ignore