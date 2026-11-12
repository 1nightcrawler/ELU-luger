from flask import render_template, redirect
from . import auth

@auth.before_app_request
def before_request():
    return

'''login view'''
@auth.route("/login")
def user_login():
    return render_template('auth/login.html')