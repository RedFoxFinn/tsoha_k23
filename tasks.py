
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
    ctx.run("pylint */*.py | grep rated > tmp/pylint_score_line.txt", pty=True)
    ctx.run("python3 pylint_score.py", pty=True)