from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import app, db, bcrypt, login_manager
from models import User, Task
from forms import RegisterForm, LoginForm, TaskForm, UpdateTaskForm

@app.route("/")
def home():
    return render_template('index.html')

# USER

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tasks'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html', form=form)

# TASKS

@app.route("/tasks")
@login_required
def tasks():
    status_filter = request.args.get('status')
    if status_filter:
        user_tasks = Task.query.filter_by(status=status_filter).all()
    else:
        user_tasks = Task.query.all()
    users = User.query.all()  # Para carregar os usuários na modal
    return render_template('tasks.html', tasks=user_tasks, users=users)

@app.route("/create_task", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if request.method == 'POST':
        title = form.title.data
        content = form.content.data
        task = Task(title=title, content=content, owner=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task created with success!', 'success')
        return redirect(url_for('tasks'))
    return render_template('create_task.html', form=form)

@app.route("/update_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    form = UpdateTaskForm()
    if request.method == 'POST':
        title = form.title.data
        content = form.content.data
        status = form.status.data
        task.title = title
        task.content = content
        task.status = status
        db.session.commit()
        flash('Task updated with success!', 'success')
        return redirect(url_for('tasks'))
    form.title.data = task.title
    form.content.data = task.content
    form.status.data = task.status
    return render_template('update_task.html', form=form, task=task)

@app.route("/delete_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted with success!', 'success')
    return redirect(url_for('tasks'))

# Assign Task Route
@app.route("/assign_task", methods=['POST'])
@login_required
def assign_task():
    task_id = request.form.get('task_id')
    user_id = request.form.get('user_id')
    
    task = Task.query.get(task_id)
    user = User.query.get(user_id)
    
    if task and user:
        task.assigned_user_id = user.id  # Atribui a tarefa ao novo usuário
        db.session.commit()
        flash(f"Task: '{task.title}', assigned to {user.username} with success!", 'success')
    else:
        flash('Failed to assign task.', 'danger')

    return redirect(url_for('tasks'))

# Rota para carregar os usuários via JSON (para uso com modal AJAX, se necessário)
@app.route("/get_users", methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(users_list)
