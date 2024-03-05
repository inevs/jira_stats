from pathlib import Path

import typer

from jira_stats import ERRORS
from jira_stats.database import DatabaseHandler, DEFAULT_DB_FILE_PATH
from jira_stats.jira_importer import Importer

app = typer.Typer()


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
    result = database.write_issues(fileImport.issues)
    if result.error:
        typer.secho(f"Error writing to database {ERRORS[result.error]}")
        typer.Exit(1)

    # print how may issues are imported
    if append:
        print(f"Appending data from {file}")
    else:
        print(f"Loading data from {file}")


@app.command()
def clean(force: bool = typer.Option(False, "--force", "-f", prompt="Are you sure you want to clean all data?")):
    """clean previously loaded data"""
    if force:
        print("Cleaning all loaded data")
    else:
        print("do nothing")


@app.command()
def stats():
    """show some statistics in the data"""
    print("show some statistics in the data")



@app.command()
def version():
    pass
