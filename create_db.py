from config import app, db
from models import User, Task

with app.app_context():
    db.drop_all()
    db.create_all()