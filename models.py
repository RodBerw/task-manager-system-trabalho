from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from config import db, login_manager
from datetime import datetime


@login_manager.user_loader
def load_task(task_id):
    return Task.query.get(int(task_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #created_at = db.Column(db.String(20), nullable=False, default=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    status = db.Column(db.String(20), nullable=False, default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 #   assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
