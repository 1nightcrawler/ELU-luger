from flask import render_template, Response, jsonify
from . import main
from ..models import Book, BookContent

'''book view should go here'''
@main.route("/")
def index():
    return render_template('index.html')

@main.route("/book/info/<int:id>")
def user_book():
    return render_template('book.html')

@main.route("/book/content/<int:book_id>")
def book_content(book_id):
    return render_template('book_content.html', book_id=book_id)

@main.route("/settings")
def settings():
    return render_template('settings.html')
