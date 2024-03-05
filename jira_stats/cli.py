import typer

app = typer.Typer()


@app.command()
def load(
        file: str,
        append: bool = typer.Option(False, "--append", "-a")
):
    """load data from jira export"""
    # issues = loadFile(str)
    # save issues in file
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
