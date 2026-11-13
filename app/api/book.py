from flask import jsonify
from . import api
from ..models import Book, BookContent

@api.route('/books')
def get_books():
    books = Book.query.all()
    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "year": b.year,
            "pages": b.pages,
            "is_available": b.is_available
        }
        for b in books
    ])

@api.route('/book/<int:id>')
def get_book(id):
    book = Book.query.filter_by(id = id).first_or_404()
    return jsonify(
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "pages": book.pages,
            "is_available": book.is_available            
        }
    )

@api.route('/book/content/<int:book_id>')
def get_book_content(book_id):
    book_content = BookContent.query.filter_by(book_id = book_id).first_or_404()
    return jsonify(
        {
            "id": book_content.id,
            "book_id": book_content.book_id,
            "content": book_content.content
        }
    )