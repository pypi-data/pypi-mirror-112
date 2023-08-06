import typer

app = typer.Typer()

@app.command()
def prefix(
    bucket: str = typer.Option(None, help="the bucket you wish to scan"),
    prefix: int = typer.Option(None, help="the prefix you wish to use")
):
  """ scans data from a bucket """
  print("scan")