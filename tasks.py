
from invoke import task

@task
def start(ctx):
  ctx.run("flask run")

@task
def format(ctx):
  ctx.run("autopep8 $(git ls-files '**.py*') --in-place --exclude='./venv/*'", pty=True)

@task
def lint(ctx):
  ctx.run("pylint app.py", pty=True)
  ctx.run("pylint tools", pty=True)
  ctx.run("pylint routes", pty=True)
  ctx.run("pylint modules", pty=True)