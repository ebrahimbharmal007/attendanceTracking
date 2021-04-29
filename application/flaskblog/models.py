from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.role}')"



class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Classes('{self.class_id}','{self.name}', '{self.id}')"

class Enrollment(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Enrollment('{self.enrollment_id}','{self.class_id}', '{self.id}')"

class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_attended = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Attendance('{self.attendance_id}','{self.class_id}', '{self.id}', '{self.date_attended}')"