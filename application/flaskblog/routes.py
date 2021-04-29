import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm
from flaskblog.models import User, Classes, Enrollment, Attendance
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
@login_required
def home():
    attendance_info = Attendance.query.filter_by(id=current_user.id,date_attended=datetime.utcnow().date()).all()
    attendance_info = [x.class_id for x in attendance_info]
    enrollment_info = Enrollment.query.filter_by(id=current_user.id).all()
    enrollment_info = [x for x in enrollment_info if x.class_id not in attendance_info ]
    classes_info = [Classes.query.filter_by(class_id=x.class_id).first() for x in enrollment_info]
   
    if current_user.role == 'T':
        teaching_classes_info = Classes.query.filter_by(id=current_user.id).all()
        
        return render_template('home.html',user=current_user,teaching=teaching_classes_info,t_size=len(teaching_classes_info),classes=teaching_classes_info)
    return render_template('home.html',user=current_user,enrollment=enrollment_info,classes=classes_info,s_size=len(enrollment_info))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/mark_attendance/<int:class_id>")
def mark_attendance(class_id):
    attendance = Attendance(class_id=class_id,id=current_user.id,date_attended=datetime.utcnow().date())
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))