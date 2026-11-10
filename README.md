# Lugemisseade

A prototype device that supports the development of functional reading
skills for students with special educational needs. Students read texts
matched to their level and answer reading comprehension questions;
teachers can follow their progress.

A Tallinn University ELU project.
**Status:** early prototype, in development.

## Text import

The planned input formats are `.json`, `.txt`, `.epub` and `.docx`; the import and conversion workflow is not yet complete in the current prototype. PDF support is not planned for now. The goal is to convert texts into a single JSON format, so they are easier to use with questions and reading features.

## Technologies

Python + Flask (backend), HTML/CSS/JS (frontend), SQLite (database).
Target hardware: Raspberry Pi 400 with a touchscreen.

## Documentation

- [Setting up and running the development environment](docs/getting-started.md)
- [Database model](docs/database.md)

Instructions for running the app, migrations and the development workflow are in the getting-started guide.

## Project structure

- `app/` – Flask application, models and templates
- `migrations/` – database migrations
- `docs/` – development and database documentation
- `content/texts/` – planned location for reading texts; not yet created in the prototype

## Development workflow

- `main` must always work: the app starts and migrations apply.
- Every change is made on its own short-lived branch and merged into `main` through a pull request (PR).
- Branch names follow the commit prefixes: `feat/…`, `fix/…`, `docs/…`, `chore/…`, `refactor/…` (e.g. `feat/txt-import`).
- Documentation for a feature goes on the same branch as its code. Small documentation fixes (e.g. typos) may go directly to `main`; code changes never do.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): imperative mood, subject line of at most 50 characters, e.g. `feat: add TXT import script`.
- Only one branch at a time changes the database schema (`app/models.py`). Tell the group, and merge the branch before anyone else changes the schema. Otherwise Alembic ends up with two heads and `db upgrade` fails.
- Before merging, check that the app starts and that `db upgrade` works on an empty database.
- Never commit database files, virtual environments or student voice recordings (see `.gitignore`).
