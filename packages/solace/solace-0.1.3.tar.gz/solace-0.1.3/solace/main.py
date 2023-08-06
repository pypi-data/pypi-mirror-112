import typer
from .new import app as new
from .run import app as run

app = typer.Typer(add_completion=False)
app.add_typer(new, name="new")
app.add_typer(run, name="run")

def cli():
  app()
