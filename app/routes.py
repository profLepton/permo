from email.errors import FirstHeaderLineIsContinuationDefect
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, Config
from app.forms import (
    LoginForm, ProfessorRegistrationForm, 
    StudentRegistrationForm, EditProfileForm, ResetPasswordForm, AddClassesForm,
    MakeRequestForm, EmptyForm, AddPermissionNumbers
    )
from app.models import User, CollegeCourse, pn_requests, PermissionNumbers
from datetime import datetime
from app.forms import ResetPasswordRequestForm
from app.emails import send_password_reset_email


@app.route('/')
@app.route('/index')
@login_required
def index():
    p_requests = []
    if not current_user.is_professor:
        p_requests = pn_requests.query.filter_by(student_id= current_user.id)
    classes = CollegeCourse.query.filter_by(professor_id=current_user.id)
    return render_template('index.html', title='Home', classes= classes, p_requests = p_requests)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
        firstName=form.firstName.data, lastName=form.lastName.data, is_professor=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered student!')
        return redirect(url_for('login'))
    return render_template('register_student.html', title='Register', form=form)

@app.route('/register_professor', methods=['GET', 'POST'])
def register_professor():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ProfessorRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
        firstName=form.firstName.data, lastName=form.lastName.data, is_professor=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user, Professor!')
        return redirect(url_for('login'))
    return render_template('register_professor.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    courses  = CollegeCourse.query.filter_by(professor_id = user.id)
    return render_template('user.html', user=user, courses = courses)

#Runs before every request.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
    return render_template('edit_profile.html', title='Edit Profile', form = form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/add_class/', methods=['GET', 'POST'])
def add_class():
    if current_user.is_professor:
        form = AddClassesForm()
        if form.validate_on_submit():
            collegeclass = CollegeCourse(course_name=form.class_name.data, professor_id= current_user.id)
            db.session.add(collegeclass)
            db.session.commit()
            flash('Class has been added.')
            return redirect(url_for('index'))
    return render_template('add_class.html', form=form)



@app.route('/manage_class/<class_id>', methods=['GET', 'POST'])
def manage_class(class_id):
    permission_numbers = PermissionNumbers.query.filter_by(course_id=class_id).all()
    permission_numbers_available = PermissionNumbers.query.filter_by(course_id=class_id, 
                                                assigned=False).all()

    permission_stats = [len(permission_numbers_available), len(permission_numbers)]

    form = EmptyForm()
    form1 = AddPermissionNumbers()
    prequests = pn_requests.query.filter_by(course_id = class_id).all()
    student_names = []
    student_usernames = []
    for prequest in prequests:
        student = User.query.filter_by(id = prequest.student_id).first()
        student_names.append(f"{student.firstName} {student.lastName}")
        student_usernames.append(student.username)
    for i in range(len(prequests)):
        prequests[i] = (student_names[i], prequests[i], student.username)
    return render_template('manage_class.html', form=form, form1= form1, pn_requests=prequests,
        permisison_numbers = permission_numbers, stats = permission_stats, class_id = class_id)



@app.route('/make_request/<class_id>', methods=[ 'GET', 'POST'])
def make_request(class_id):
    if current_user.is_professor:
        return redirect(url_for('index'))
    else:
        print("here")
        form = MakeRequestForm()
        prequests = pn_requests.query.filter_by(student_id= current_user.id, course_id = class_id).all()
        if form.validate_on_submit():
            print("here also")
            
            
            course = CollegeCourse.query.filter_by(id=class_id).first()
            prof_id = course.professor_id
            stud_id = current_user.id
            
            newRequest = pn_requests(message = form.message.data, 
                professor_id = prof_id, student_id = stud_id,
                course_id = class_id, 
                class_name = course.course_name
            )

            db.session.add(newRequest)
            db.session.commit()

            flash('You request has been made!')
            return redirect(url_for('index'))
            
        return render_template('make_request.html', form=form, pn_requests = prequests)

@app.route('/request_approve/<request_id>', methods=['POST'])
@login_required
def request_approve(request_id):
    form = EmptyForm()
    if form.validate_on_submit():
        pn_request = pn_requests.query.filter_by(id= request_id)[0]
        pn_request.status = True
        class_id = pn_request.course_id
        pn = PermissionNumbers.query.filter_by(course_id=class_id).first()
        pn_request.permission_number = pn.permission_number
        pn.assigned = True
        pn.request_id = request_id
        db.session.commit()
        flash('Request has been approved!')
        return redirect(url_for('manage_class', class_id = class_id))   

@app.route('/request_decline/<request_id>', methods=['POST'])
@login_required
def request_decline(request_id):
    form = EmptyForm()
    if form.validate_on_submit():
        pn_request = pn_requests.query.filter_by(id= request_id)[0]
        deleted_request_class_id = pn_request.course_id
        pn_requests.query.filter_by(id = request_id).delete()
        db.session.commit()
        flash('Request has been declined.')
        return redirect(url_for('manage_class', class_id = deleted_request_class_id))  

@app.route('/add_numbers/<class_id>', methods=['POST'])
@login_required
def add_numbers(class_id):
    form = AddPermissionNumbers()
    if form.validate_on_submit():
        permission_string = form.permission_numbers.data
        permission_string = permission_string.replace(' ', '')
        permission_string = permission_string.replace('\n', '')
        permission_numbers_list = permission_string.split(',')
        permission_numbers_list = list(set(permission_numbers_list))
        
        course = CollegeCourse.query.filter_by(id = class_id).first()

        n_numbers = len(permission_numbers_list)

        for number in permission_numbers_list:
            newNum = PermissionNumbers(
                permission_number = number, 
                course_id = class_id,
                course_name = course.course_name,
                professor_id = course.professor_id,
            )

            db.session.add(newNum)
        
        db.session.commit()
        flash(f"{n_numbers} permission numbers have been added.")
        return redirect(url_for('manage_class', class_id = class_id)) 