# Getting started

This guide sets up the Flask prototype for local development. Commands assume the repository root is the current directory unless noted. The checked-in migration repository is at the root, and the Flask CLI is invoked with `app/app.py`.

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
python -m flask --app app/app.py db upgrade
python -m flask --app app/app.py db current
```

Run these from the repository root. Do **not** run `db init` for the normal setup: that command creates a new migration repository, and this project already has one. The configured SQLite URL is `sqlite:///database.db`; Flask-SQLAlchemy resolves this relative to the Flask instance directory, so the local file is normally `app/instance/database.db`.

The database file is local state and is ignored by Git. Keep important local data backed up separately; migrations reproduce the schema, not the contents of a developer's database. There is currently no seed-data command, so a fresh database starts without books, users, classrooms, or tests.

For more detail about tables, relationships, and current limitations, see [Database model](database.md).

## Run the web application

From the repository root, with the virtual environment active:

```shell
python -m flask --app app/app.py run --debug
```

Open <http://127.0.0.1:5000/>. The current application is an early prototype; the active route renders the landing page. Most of the database model describes planned functionality that does not yet have complete application routes or workflows.

Stop the development server with `Ctrl+C`.

## Change the database schema

When a model change alters the schema, generate a migration, inspect it, then apply it:

```shell
python -m flask --app app/app.py db migrate -m "describe the schema change"
# Review the new file under migrations/versions/ before applying it.
python -m flask --app app/app.py db upgrade
```

Commit both the model change and the generated migration. Autogeneration is a draft: check that it includes the intended columns, constraints, indexes, and foreign keys. Do not edit the database manually or use `db.create_all()` as a replacement for migrations.

Only run this once if creating a brand-new migration repository (not needed for the normal clone workflow):

```shell
python -m flask --app app/app.py db init
```

If a migration or upgrade fails, stop and inspect the error and generated revision before trying another migration. Do not delete the local SQLite database as a generic fix; that destroys its data.

## Project layout

```text
app/
  app.py             Flask application, configuration, and routes
  extensions.py      shared Flask-SQLAlchemy extension
  models.py          SQLAlchemy models and enums
  templates/         Jinja templates
migrations/
  versions/          committed Alembic/Flask-Migrate revisions
docs/
  getting-started.md this guide
  database.md        data model reference
requirements.txt     direct Python dependencies
```

## Troubleshooting

- **`ModuleNotFoundError: extensions` or `models`:** run the Flask commands from the repository root with `--app app/app.py` as shown above.
- **`No such command 'db'`:** install the requirements into the active environment, then use `python -m flask` so the command uses that environment's Flask installation.
- **Import or migration errors:** verify that all models import successfully before generating migrations. Review the full traceback; do not apply a partial or hand-edited schema as a workaround.
- **Database and model differ:** run `python -m flask --app app/app.py db current` and inspect the revisions under `migrations/versions/`. Create and review a migration for model changes, then run `db upgrade`.

There is no test or lint command configured in this repository yet. Add a test suite and document its command when one is introduced.
