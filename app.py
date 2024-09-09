from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import app, db, bcrypt, login_manager
from models import User, Task

# USER

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tasks'))
        else:
            flash('Login falhou. Verifique suas credenciais.', 'danger')
    return render_template('login.html')

# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route("/tasks")
# @login_required
# def tasks():
#     user_tasks = Task.query.filter_by(owner=current_user)
#     return render_template('tasks.html', tasks=user_tasks)

# TASKS

@app.route("/create_task", methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        task = Task(title=title, content=content, owner=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tasks'))
    return render_template('create_task.html')

@app.route("/update_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.content = request.form['content']
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('tasks'))
    return render_template('update_task.html', task=task)

@app.route("/delete_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa deletada com sucesso!', 'success')
    return redirect(url_for('tasks'))
