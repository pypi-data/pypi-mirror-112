import typer
from .utils.aws import get_matching_s3_keys

app = typer.Typer(add_completion=False)

@app.command()
def count(bucket: str, prefix: str):
    # TODO: enable verbose mode globally...
    # typer.echo(f"counting objects in {bucket} with prefix {prefix}...")
    count = 0
    for obj in get_matching_s3_keys(bucket, prefix):
        count += 1
    typer.echo(f"{count}")
    # typer.echo(f"found {count} objects in {bucket} with prefix {prefix}")

@app.command()
def download(bucket: str, prefix: str, destination: str):
    typer.echo(f"download objects in {bucket} with prefix {prefix}...")



def cli():
  app()
