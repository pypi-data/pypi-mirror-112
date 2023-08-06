import typer
import os
import sys
from .utils.aws import get_matching_s3_keys, s3resource
from humanize import naturalsize
from tabulate import tabulate

app = typer.Typer()

@app.command()
def keys(bucket: str, prefix: str):
  """ return size of each key in bucket """
  table = []
  for obj in s3resource.Bucket(bucket).objects.filter(Prefix=prefix):
    idx = len(obj.key.split('/')) - 2
    if idx >= 0:
      idx = 3
    key = "/".join(obj.key.split('/')[-idx:])
    table.append([key, naturalsize(obj.size)])
  typer.echo(tabulate(table, headers=["Key", "Size"]))

@app.command()
def total(bucket: str, prefix: str):
  """ get the total size of all keys by prefix """
  total_size = 0
  for obj in s3resource.Bucket(bucket).objects.filter(Prefix=prefix):
      total_size += obj.size
  typer.echo(f"{naturalsize(total_size)}")
