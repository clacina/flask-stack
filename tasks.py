"""
tasks.py is for creating python invoke tasks for convenience.

Normally for flowroute projects, we use flowdeploy to run
invoke tasks (flowdeploy is a wrapper around invoke and is able
to run any custom tasks written to tasks.py files).  However,
I prefer to start projects using only invoke to keep
flowdeploy from feeling like a black box.

When finalizing a project, the redundant commands can be removed.
For example, build, coverage, down, init, release, show-tag, test,
and up are all defined by default in flowdeploy. If we wanted to
use custom versions with flowdeploy, we can override them in flowdeploy.yml.

Some libraries are imported within functions so they don't break
flowdeploy if someone is building this without requests.
"""
import invoke
import os


CONTAINER_NAME = "dataprocess"


# changes working directory to root of project so tasks can be triggered from subdirs
cwd = os.getcwd()
while not os.path.isfile("tasks.py") and cwd != "/":
    os.chdir(cwd + "/..")
    cwd = os.getcwd()


@invoke.task
def help(ctx):
    """Prints how to use invoke's help argument. ;) """
    print(
        (
            "Use `inv -l` to list tasks and `inv -h <task>` to see "
            "the help information about a specific task.  For help "
            "with invoke commands, use `inv -h` or `inv --help`"
        )
    )


@invoke.task
def bup(ctx, logs=False):
    """Runs docker build and docker-compose up -d and optionally follows logs."""
    log = " && docker-compose logs --follow" if logs else ""
    ctx.run("docker build -t {}:latest . && docker-compose up -d{}".format(CONTAINER_NAME, log))


@invoke.task
def sh(ctx, container="develop"):
    """executes 'docker-compose exec <container> bash'"""
    ctx.run("docker-compose exec {} bash".format(container), pty=True)


@invoke.task
def bash(ctx, container="develop"):
    """executes 'docker-compose exec <container> bash'"""
    ctx.run("docker-compose exec {} bash".format(container), pty=True)


@invoke.task
def python(ctx, container="develop"):
    """executes 'docker-compose exec develop python'"""
    ctx.run("docker-compose exec {} python".format(container), pty=True)


@invoke.task
def lint(ctx):
    """executes 'docker-compose exec develop flake8 <container>'"""
    ctx.run("docker-compose exec develop flake8 {}".format(CONTAINER_NAME), pty=True)


@invoke.task
def logs(ctx, container=""):
    """executes 'docker-compose logs --follow [--container NAME]'"""
    ctx.run("docker-compose logs --follow {}".format(container))


@invoke.task
def psql(ctx, user=False):
    """Connects to the projects PostgreSQL Container with flowroute or the appuser."""
    user = CONTAINER_NAME if user else "lacinaslair"
    ctx.run("docker-compose exec flowroutedb psql -U {} -d test_flowroute".format(user), pty=True)


@invoke.task
def rs(ctx, container=CONTAINER_NAME):
    """Restarts the service container."""
    ctx.run("docker-compose restart {}".format(container))


@invoke.task
def wip(ctx, debug=False, args=""):
    """Run tests marked with @pytest.mark.wip and fail early.

    Add any extra arguments with "-a".
    Example:
        inv wip -a '-vv --log-level="DEBUG"'
    """
    ctx.run(
        "flowdeploy py.test -s{} -t ' -x -m wip --hypothesis-explain {}'".format(
            "d" if debug else "", args
        ),
        pty=True,
    )


@invoke.task
def missing(ctx, args=""):
    """Run pytest coverage and show missing tests."""
    ctx.run(
        "flowdeploy py.test -t "
        "' --cov={} --cov-config=setup.cfg --cov-report=term-missing {}'".format(
            CONTAINER_NAME, args
        ),
        pty=True,
    )


@invoke.task
def fail(ctx, verbose=False):
    """Run tests and fail early."""
    v = " -vv" if verbose else ""
    ctx.run("flowdeploy py.test -t ' -x'{}".format(v), pty=True)


@invoke.task(
    help={
        "hide": (
            "What output to hide, if any. One of {'out', 'err', 'both'}. "
            "Defaults to None, hiding nothing."
        )
    }
)
def openapi(ctx, hide=None):
    """Creates and saves $PWD/openapi.json from FastAPI's generated schema."""
    with open("openapi.json", "w") as f:
        f.write(
            ctx.run(
                "docker-compose exec develop python -Bq scripts/openapi.py > openapi.json",
                pty=True,
                hide=hide,
            ).stdout
        )


@invoke.task
def pip_freeze(ctx):
    """Creates and saves $PWD/pip-freeze.txt from `pip freeze --all`."""
    with open("pip-freeze.txt", "w") as f:
        f.write(
            ctx.run(
                "docker-compose exec develop pip freeze --all",
                pty=True,
            ).stdout
        )
