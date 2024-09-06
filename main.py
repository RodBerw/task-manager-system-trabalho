from flask import render_template, redirect, url_for
from config import app

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')