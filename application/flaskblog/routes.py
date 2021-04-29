import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm
from flaskblog.models import User, Classes, Enrollment, Attendance
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from calendar import monthrange

num_classes = 0
tot_stu = 0

class studentdashboarddata:
  def __init__(self, classname, classid,instructorname,class_average_attendance):
    self.classname = classname
    self.classid = classid
    self.instructorname = instructorname
    self.class_average_attendance = class_average_attendance

  def __repr__(self):
      return f"studentdashboarddata('{self.classname}', '{self.classid}', '{self.instructorname}', '{self.class_average_attendance}')"

class teacherdashboarddata:
  def __init__(self, classname, classid,class_average_attendance,num_students):
    self.classname = classname
    self.classid = classid
    self.class_average_attendance = class_average_attendance
    self.num_students = num_students

  def __repr__(self):
      return f"studentdashboarddata('{self.classname}', '{self.classid}','{self.class_average_attendance}','{self.num_students}')"

class displaystudent:
  def __init__(self, studentname, studentid,class_attendance):
    self.studentname = studentname
    self.studentid = studentid
    self.class_attendance = class_attendance

  def __repr__(self):
      return f"studentdashboarddata('{self.studentname}', '{self.studentid}', '{self.class_attendance}', '{self.overall_attendance}')"


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
        global num_classes
        global tot_stu
        num_classes = len(teaching_classes)
        tot_stu = 0
        
        Data = []
        for x in range(len(teaching_classes)):           
            num_students_class_attended = Attendance.query.filter_by(class_id=teaching_classes[x].class_id,date_attended=datetime.utcnow().date()).count()
            total_num_of_students_in_class = Enrollment.query.filter_by(class_id=teaching_classes[x].class_id).count()
            tot_stu += total_num_of_students_in_class
            class_attendance = round((num_students_class_attended/total_num_of_students_in_class)*100)
            temp = teacherdashboarddata(teaching_classes[x].name,teaching_classes[x].class_id,class_attendance,total_num_of_students_in_class)
            Data.append(temp)
        Data = sorted(Data, key=lambda x: x.class_average_attendance,reverse=True)
        average_attendance = 0
        for d in Data:
            average_attendance += d.class_average_attendance
        average_attendance = average_attendance/len(Data)

        return render_template('home.html',data = Data,number_of_classes = num_classes, total_students=tot_stu,size=len(Data),average_attendance=average_attendance)

    

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
@login_required
def mark_attendance(class_id):
    exists = bool(Attendance.query.filter_by(class_id=class_id,id=current_user.id,date_attended=datetime.utcnow().date()).first())
    if not exists:
        attendance = Attendance(class_id=class_id,id=current_user.id,date_attended=datetime.utcnow().date())
        db.session.add(attendance)
        db.session.commit()
    else:
        flash('Attendance has already been marked', 'danger')
        return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route("/students/<int:class_id>")
@login_required
def students(class_id):
    num_of_days_in_current_month = monthrange(datetime.utcnow().year,datetime.utcnow().month)[1]
    first_day_month = datetime.utcnow().date().replace(day=1)
    last_day_month = datetime.utcnow().date().replace(day=num_of_days_in_current_month)
    students_info = [User.query.filter_by(id=classinfo.id).first() for classinfo in Enrollment.query.filter_by(class_id=class_id).all()]
    Data = []
    for x in range(len(students_info)):
        class_attendance = round((Attendance.query.filter_by(id=students_info[x].id,class_id=class_id).filter(Attendance.date_attended.between(first_day_month,last_day_month)).count() / num_of_days_in_current_month)*100)
        temp=displaystudent(students_info[x].name,students_info[x].id,class_attendance)
        Data.append(temp)
    Data = sorted(Data, key=lambda x: x.class_attendance,reverse=True)
    return render_template('students.html', title='Info',data=Data,size=len(Data),number_of_classes = num_classes, total_students=tot_stu)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))