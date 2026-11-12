from flask import jsonify
from . import api
from ..models import Book

@api.route('/book/<int:id>')
def get_book():
    return ""

@api.route('/book/content/<int:id>')
def get_book_content():
    return ""