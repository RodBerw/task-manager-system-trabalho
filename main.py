# from flask import render_template, redirect, url_for, request
# from config import app
# from models import User, Task

# @app.route("/")
# def home():
#     return render_template('index.html')

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     return render_template('register.html')

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     value = request.args.get('value')
#     return render_template('login.html', value=value)

# if __name__ == '__main__':
#     app.run(debug=True)