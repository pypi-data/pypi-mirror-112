import typer
import os
import sys
import importlib
from solace import DevelopmentServer

app = typer.Typer()

@app.command()
def dev(
    host: str = typer.Option("127.0.0.1", help="the interface the development server will bind to"),
    port: int = typer.Option(5000, help="the port the development server will listen on")
):
  """ starts a local development server. Do not use this for production. """
  sys.path.append(os.getcwd())
  api = importlib.import_module("src.api")
  DevelopmentServer(api.api, host=host, port=port).start()
