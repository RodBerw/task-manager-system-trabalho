<<<<<<< HEAD
from flask import render_template, redirect, url_for, request
from config import app, db
from models import User, Task
=======
# from flask import render_template, redirect, url_for, request
# from config import app
# from models import User, Task
>>>>>>> 3ebb4824dbcd913a0910b3f86f1699c53ce8add5

# @app.route("/")
# def home():
#     return render_template('index.html')

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     return render_template('register.html')

<<<<<<< HEAD
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

with app.app_context():
    db.create_all()
=======
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     value = request.args.get('value')
#     return render_template('login.html', value=value)
>>>>>>> 3ebb4824dbcd913a0910b3f86f1699c53ce8add5

# if __name__ == '__main__':
#     app.run(debug=True)