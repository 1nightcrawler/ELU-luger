import os
from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

@app.cli.command("test")
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not result.wasSuccessful():
        import sys
        sys.exit(1)

@app.cli.command("seed")
def seed():
    from app.seed import seed_example_book

    book, book_created, content_created = seed_example_book()

    if book_created and content_created:
        print(f"Created example book: {book.title}")
    elif content_created:
        print(f"Added text to existing book: {book.title}")
    else:
        print(f"Example book exists, seed not finished.")

