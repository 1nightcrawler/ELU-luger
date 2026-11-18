from flask import render_template, Response, jsonify
from . import main
from ..models import Book, BookContent

'''book view should go here'''
@main.route("/")
def index():
    return render_template('index.html')

@main.route("/book/info/<int:book_id>")
def book_info(book_id):
    return render_template('book_info.html', book_id=book_id)

@main.route("/book/content/<int:book_id>")
def book_content(book_id):
    return render_template('book_content.html', book_id=book_id)

@main.route("/statistics")
def statistics():
    return render_template('statistics.html')

@main.route("/settings")
def settings():
    return render_template('settings.html')

@main.route("/leaderboard")
def leaderboard():
    return render_template('leaderboard.html')
