"""Small, repeatable demo data for local development."""

from . import db
from .models import Book, BookContent


EXAMPLE_TITLE = "A Seed for Mia"
EXAMPLE_AUTHOR = "ELU demo"
EXAMPLE_TEXT = """Mia has a little seed.
She puts it in a cup of soil.
She gives it water.
The sun shines on the cup.
A green stem comes up.
Mia smiles. The seed is growing."""


def seed_example_book():
    """Create the example book and text if they do not already exist.

    Returns:
        (book, book_created, content_created)
    """
    try:
        book = Book.query.filter_by(
            title=EXAMPLE_TITLE,
            author=EXAMPLE_AUTHOR,
        ).first()

        book_created = book is None
        if book_created:
            book = Book(
                title=EXAMPLE_TITLE,
                author=EXAMPLE_AUTHOR,
                pages=1,
                is_available=True,
            )
            db.session.add(book)
            db.session.flush()

        content_created = book.content is None
        if content_created:
            book.content = BookContent(content=EXAMPLE_TEXT)

        db.session.commit()
        return book, book_created, content_created
    except Exception:
        db.session.rollback()
        raise