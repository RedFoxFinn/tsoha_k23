
from invoke import task


@task
def start(ctx):
    ctx.run("flask --app=app.py run")


@task
def format(ctx):
    ctx.run(
        "autopep8 $(git ls-files '**.py*') --in-place --exclude='./venv/*','app.py','tasks.py','.pylintrc'", pty=True)


@task
def lint(ctx):
    ctx.run("pylint -j 3 app.py tools routes", pty=True)