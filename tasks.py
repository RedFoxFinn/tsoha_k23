
from invoke import task

@task
def start(ctx):
  ctx.run("flask --app=src/app.py run")

@task
def format(ctx):
  ctx.run("autopep8 --in-place --exclude='./venv/*'", pty=True)

@task
def lint(ctx):
  ctx.run("pylint src/app.py", pty=True)
  ctx.run("pylint src/tools", pty=True)
  ctx.run("pylint src/routes", pty=True)
  ctx.run("pylint src/modules", pty=True)