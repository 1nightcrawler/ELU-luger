from flask import render_template
from . import main

'''book view should go here'''
@main.route("/")
def index():
    return render_template('index.html')

@main.route("/book/info/<int:id>")
def user_book():
    return render_template('book.html')

@main.route("/book/content/<int:id>")
def book_content():
    return render_template('book_content.html')