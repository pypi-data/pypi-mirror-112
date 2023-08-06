import typer
from .utils.aws import get_matching_s3_keys, s3resource
from humanize import naturalsize

app = typer.Typer(add_completion=False)
# TODO: enable verbose mode globally...

@app.command()
def count(bucket: str, prefix: str):
    # typer.echo(f"counting objects in {bucket} with prefix {prefix}...")
    count = 0
    for key in get_matching_s3_keys(bucket, prefix):
        count += 1
    typer.echo(f"{count}")
    # typer.echo(f"found {count} objects in {bucket} with prefix {prefix}")

@app.command()
def size(bucket: str, prefix: str):
    total_size = 0
    for obj in s3resource.Bucket(bucket).objects.filter(Prefix=prefix):
        total_size += obj.size
    typer.echo(f"{naturalsize(total_size)}")

@app.command()
def download(bucket: str, prefix: str, destination: str):
    typer.echo(f"download objects in {bucket} with prefix {prefix}...")

def cli():
  app()
