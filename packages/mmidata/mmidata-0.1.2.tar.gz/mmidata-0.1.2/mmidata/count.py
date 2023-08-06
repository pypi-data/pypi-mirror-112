import typer
import os
import sys
from .utils.aws import get_matching_s3_keys

app = typer.Typer()

@app.command()
def impressions(path: str):
  """ counts number of impressions in a file """
  if os.path.isfile(path):
    count = sum(1 for line in open(path))
    typer.echo(f"{count}")
    return
  typer.echo(f"{path} is not valid")
  sys.exit(1)

@app.command()
def keys(bucket: str, prefix: str):
  """ counts number of keys in a bucket by prefix """
  count = 0
  for key in get_matching_s3_keys(bucket, prefix):
      count += 1
  typer.echo(f"{count}")
