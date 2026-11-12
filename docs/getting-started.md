# Getting started

This guide sets up the Flask prototype for local development. Commands assume the repository root is the current directory unless noted. The checked-in migration repository is at the root. The root `.flaskenv` file configures Flask to load `run.py` and use the development configuration.

## Prerequisites

- Git
- Python 3.11 (the current development environment uses Python 3.11.5)
- PowerShell on Windows, or a POSIX-compatible shell on macOS/Linux

Use a virtual environment so project packages do not change your system Python.

## Clone the repository

```shell
git clone <repository-url>
cd ELU-luger
```

Replace `<repository-url>` with the repository URL provided by the project team.

## Create and install the environment

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, run the environment's Python directly instead:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### macOS/Linux

```shell
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `myenv/` environment used by one developer is local to that machine. Create your own `.venv/`; do not copy or commit a virtual environment.

## Initialize or update the local database

The repository already contains a Flask-Migrate repository in `migrations/` and an initial schema revision. For a fresh clone, apply the committed migrations:

```shell
flask db upgrade
flask db current
```

Run these from the repository root with the virtual environment active. Flask reads `FLASK_APP=run.py` from `.flaskenv`. Do **not** run `db init` for the normal setup: that command creates a new migration repository, and this project already has one. The development configuration uses `DEV_DATABASE_URL` when it is set; otherwise it uses the SQLite file `data-dev.sqlite` at the repository root. The test configuration similarly accepts `TEST_DATABASE_URL` and otherwise uses `data-test.sqlite` at the repository root.

The database file is local state and is ignored by Git. Keep important local data backed up separately; migrations reproduce the schema, not the contents of a developer's database. There is currently no seed-data command, so a fresh database starts without book records, user accounts, classrooms, or assessment records.

For more detail about tables, relationships, and current limitations, see [Database model](database.md).

## Run the web application

From the repository root, with the virtual environment active, start the development server:

```shell
flask run
```

The installed `python-dotenv` package lets Flask CLI load `.flaskenv` automatically. That file points Flask to `run.py`, enables debug mode, and selects the development configuration, so you do not need to pass `--app` or `--debug` manually. Open <http://127.0.0.1:5000/> in your browser. The current application is an early prototype; the active route renders the landing page, while much of the database model describes functionality that does not yet have complete application routes or workflows.

Stop the development server with `Ctrl+C`.

## Run the tests

With the virtual environment active and the repository root as the current directory, run the test suite through the Flask CLI:

```shell
flask test
```

This project uses Python's built-in `unittest` framework; the `test` command discovers and runs tests in `tests/`. The tests use the testing configuration (`TESTING=True`) and create/drop their tables during each test. By default, this configuration uses `data-test.sqlite` at the repository root; set `TEST_DATABASE_URL` to use a different test database. Do not point it at a development or production database.

## Change the database schema

When a model change alters the schema, generate a migration, inspect it, then apply it:

```shell
flask db migrate -m "describe the schema change"
# Review the new file under migrations/versions/ before applying it.
flask db upgrade
```

Commit both the model change and the generated migration. Autogeneration is a draft: check that it includes the intended columns, constraints, indexes, and foreign keys. Do not edit the database manually or use `db.create_all()` as a replacement for migrations.

Only run this once if creating a brand-new migration repository (not needed for the normal clone workflow):

```shell
flask db init
```

If a migration or upgrade fails, stop and inspect the error and generated revision before trying another migration. Do not delete the local SQLite database as a generic fix; that destroys its data.

## Project layout

```text
run.py               Flask CLI entry point and test command
config.py            development, testing, and production settings
.flaskenv             local Flask CLI configuration
app/
  __init__.py         application factory and SQLAlchemy extension
  models.py           SQLAlchemy models and enums
  api/                API blueprint
  main/               main web blueprint and views
  templates/          Jinja templates
migrations/
  versions/           committed Alembic/Flask-Migrate revisions
tests/
  test_basics.py      unittest tests for app setup
docs/
  getting-started.md  this guide
  database.md         data model reference
requirements.txt      Python dependencies
```

## Troubleshooting

- **Flask cannot find the app or a CLI command:** make sure the virtual environment is active, dependencies are installed, and the current directory is the repository root so Flask can load `.flaskenv`.
- **Import or migration errors:** review the full traceback and verify that models import successfully before generating migrations. Do not apply a partial or hand-edited schema as a workaround.
- **Database and model differ:** run `flask db current` and inspect the revisions under `migrations/versions/`. Create and review a migration for model changes, then run `flask db upgrade`.
