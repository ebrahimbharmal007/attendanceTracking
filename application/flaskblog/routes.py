import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm
from flaskblog.models import User, Classes, Enrollment, Attendance
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from calendar import monthrange

class studentdashboarddata:
  def __init__(self, classname, classid,instructorname,class_average_attendance):
    self.classname = classname
    self.classid = classid
    self.instructorname = instructorname
    self.class_average_attendance = class_average_attendance

  def __repr__(self):
      return f"studentdashboarddata('{self.classname}', '{self.classid}', '{self.instructorname}', '{self.class_average_attendance}')"

class teacherdashboarddata:
  def __init__(self, classname, classid,class_average_attendance):
    self.classname = classname
    self.classid = classid
    self.class_average_attendance = class_average_attendance

  def __repr__(self):
      return f"studentdashboarddata('{self.classname}', '{self.classid}','{self.class_average_attendance}')"


@app.route("/")
@app.route("/home")
@login_required
def home():
    if current_user.role == 'S':
        num_of_days_in_current_month = monthrange(datetime.utcnow().year,datetime.utcnow().month)[1]
        first_day_month = datetime.utcnow().date().replace(day=1)
        last_day_month = datetime.utcnow().date().replace(day=num_of_days_in_current_month)
        enrollment_info = Enrollment.query.filter_by(id=current_user.id).all()
        # print("Enrollment Info: ")
        # print(enrollment_info)
        classes_enrolled = [Classes.query.filter_by(class_id=enroll.class_id).first() for enroll in enrollment_info]
        # print("classes_enrolled Info: ")
        # print(classes_enrolled)
        class_instructors = [User.query.filter_by(id=clas.id).first() for clas in classes_enrolled]
        # print("class_instructors Info: ")
        # print(class_instructors)
        # print(len(classes_enrolled))
        Data = []
        for x in range(len(classes_enrolled)):
            class_attendance = round((Attendance.query.filter_by(id=current_user.id,class_id=classes_enrolled[x].class_id).filter(Attendance.date_attended.between(first_day_month,last_day_month)).count() / num_of_days_in_current_month)*100)
            temp = studentdashboarddata(classes_enrolled[x].name,classes_enrolled[x].class_id,class_instructors[x].name,class_attendance)
            Data.append(temp)
        Data = sorted(Data, key=lambda x: x.class_average_attendance,reverse=True)
        classes_attended_today = Attendance.query.filter_by(id=current_user.id,date_attended=datetime.utcnow().date()).all()
        classes_attended_today = [clas.class_id for clas in classes_attended_today]
        average_attendance = 0
        for d in Data:
            average_attendance += d.class_average_attendance
        average_attendance = average_attendance/len(Data)
        return render_template('home.html',classes=classes_enrolled,size=len(Data),attendance_info=classes_attended_today,data=Data,average_attendance=average_attendance)
    else:
        # teaching_classes_info = Classes.query.filter_by(id=current_user.id).all()
        # attendance_percentage = [round((Attendance.query.filter_by(class_id=x.class_id,date_attended=datetime.utcnow().date()).count()/Enrollment.query.filter_by(class_id=x.class_id).count())*100,1) for x in teaching_classes_info]
        teaching_classes = Classes.query.filter_by(id=current_user.id).all()
        number_of_classes = len(teaching_classes)
        total_students = 0
        Data = []
        for x in range(len(teaching_classes)):           
            num_students_class_attended = Attendance.query.filter_by(class_id=teaching_classes[x].class_id,date_attended=datetime.utcnow().date()).count()
            total_num_of_students_in_class = Enrollment.query.filter_by(class_id=teaching_classes[x].class_id).count()
            total_students += total_num_of_students_in_class
            class_attendance = round((num_students_class_attended/total_num_of_students_in_class)*100)
            temp = teacherdashboarddata(teaching_classes[x].name,teaching_classes[x].class_id,class_attendance)
            Data.append(temp)
        Data = sorted(Data, key=lambda x: x.class_average_attendance,reverse=True)
        average_attendance = 0
        for d in Data:
            average_attendance += d.class_average_attendance
        average_attendance = average_attendance/len(Data)

        return render_template('home.html',data = Data,number_of_classes = number_of_classes, total_students=total_students,size=len(Data),average_attendance=average_attendance)

    

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

@app.route("/students/<int:class_id>")
def students(class_id):
    # enrollment = Enrollment.query.filter_by(class_id=class_id).all()
    students_info = [User.query.filter_by(id=classinfo.id).first() for classinfo in Enrollment.query.filter_by(class_id=class_id).all()]


    return render_template('students.html', title='Info',students_info=students_info,size=len(students_info))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))