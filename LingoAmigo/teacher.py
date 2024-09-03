from LingoAmigo import app
from LingoAmigo import Blueprint

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify,current_app
from flask_hashing import Hashing
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date, time
import os
import re
from . import connect
from .database import get_cursor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from decimal import Decimal


teacher = Blueprint("teacher", __name__, static_folder="static", 
                       template_folder="templates")

hashing = Hashing(app)

app.config['flash_messages'] = {}


@teacher.route('/')
def teacher_dashboard():
    if 'loggedin' in session: # Ensuring the user is a logged-in teacher
        user_role = session.get('role', None)
        user_id = session.get('id', None)
        cursor, connection = get_cursor() 

        #Fetch teacher profile info
        cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (session['id'],))
        teacher_profile = cursor.fetchone()

         
        #Fetch user account info
        cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
        teacher_info = cursor.fetchone()

        print("Session Data:", session)
        cursor.close()  
        connection.close() 
        

        return render_template('teacher_dashboard.html',teacher_info = teacher_info, teacher_profile = teacher_profile)
    return redirect(url_for('login.login_page'))




@teacher.route('/teacher/teacher_edit_profile', methods=['GET', 'POST'])
def teacher_edit_profile():
    if 'loggedin' in session :
        user_role = session.get('role', None)
        user_id = session.get('id', None)
        # nationality list
        nationalities = ['American', 'Canadian', 'Chinese', 'Mexican', 'Brazilian', 'Argentinian', 'British', 'French', 'German', 'Italian', 'Spanish', 'Portuguese', 'Russian', 'Indian', 'Japanese', 'Korean', 'Australian', 'New Zealander', 'South African', 'Egyptian', 'Nigerian', 'Saudi', 'Emirati', 'Iranian', 'Turkish', 'Indonesian', 'Thai', 'Vietnamese', 'Filipino', 'Malaysian']
        cursor, connection = get_cursor() 
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone = request.form.get('phone')
            title = request.form.get('title')
            nationality = request.form.get('nationality')
            description = request.form.get('description')
            email = request.form.get('email')
            date_join = request.form.get('date_join')
            image_url = request.files.get('image_url')
            image_path = upload(image_url)
            
            # email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash('Invalid email address format.', 'error')
                return redirect(request.url)
            # phone format
            nz_phone_pattern = re.compile(r"^(\+64|0)([2-9]\d{1}|[27]\d{2})[-\s]?\d{3}[-\s]?\d{4}$")
            if not nz_phone_pattern.match(phone):
                flash('Phone number must be in New Zealand format.', 'error')
                return redirect(request.url)
            # date
            try:
                date_join = datetime.strptime(date_join, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return redirect(request.url)
            
            if image_path:

                cursor.execute('''
                               UPDATE Teacher
                               SET first_name=%s, last_name=%s, email=%s, title=%s, nationality=%s, description=%s, phone=%s, image_url=%s, date_join=%s
                            WHERE teacher_id=%s
                           ''', (first_name, last_name, email, title, nationality, description, phone, image_path, date_join, user_id))
            else:

                #update teacher info
                cursor.execute('''
                                UPDATE Teacher
                                SET first_name=%s, last_name=%s, email=%s, title=%s, nationality=%s, description=%s, phone=%s, date_join=%s
                                WHERE teacher_id=%s
                           ''', (first_name, last_name, email, title, nationality, description, phone, date_join, user_id))
            flash('Profile updated successfully', 'success')
            return redirect(url_for('teacher.teacher_dashboard', image_path=image_path))
        else:
            cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
            teacher_info = cursor.fetchone()
            #fetch current teacher profile for edit
            cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (session['id'],))
            teacher_profile = cursor.fetchone()


            cursor.close()  
            connection.close() 

            return render_template('teacher_edit_profile.html', teacher_profile=teacher_profile, teacher_info=teacher_info, nationalities=nationalities)
    else:
        return redirect(url_for('login.login_page'))
    
def upload(file):
    if file and file.filename:
                filename = secure_filename(file.filename)
                uploads_dir =os.path.join(current_app.root_path,'static','uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                filepath = os.path.join(uploads_dir, filename)
                file.save(filepath.replace("\\", "/"))
                return filename
    






@teacher.route("/change_password", methods=["POST"])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))

    cursor, connection = get_cursor()
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    if new_password != confirm_password:
        flash('New password and confirm password do not match.')
        return redirect(url_for('teacher.teacher_dashboard'))

    if not new_password or (len(new_password) < 8 or not any(char.isdigit() for char in new_password) or not any(char.isalpha() for char in new_password)):
        flash('Password must be at least 8 characters long and contain both letters and numbers.')
        return redirect(url_for('teacher.teacher_dashboard'))

    hashed = hashing.hash_value(new_password, salt='abcd')

    update_account_query = '''
        UPDATE User
        SET password = %s
        WHERE user_id = %s
    '''
    cursor.execute(update_account_query, (hashed, session['id']))
    connection.commit()

    flash('Your password has been successfully updated.')
    return redirect(url_for('teacher.teacher_dashboard'))



@teacher.route("/teacher_courses")
def teacher_courses():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    user_role = session.get('role', None)
    cursor, connection = get_cursor()
    courses_query = '''
                    SELECT c.course_id, c.course_name, c.image_url, c.status, l.language_id, l.language_name
                    FROM Course c
                    JOIN Language l ON c.language_id = l.language_id
                    WHERE c.creator_id = %s AND c.status IN ('Active', 'Pending')
                    '''
    cursor.execute(courses_query, (user_id,))
    teacher_courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('teacher_courses.html', teacher_courses=teacher_courses, user_role=user_role)

@teacher.route('view_students/<int:course_id>')
def view_students(course_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    student_query = '''
                    SELECT s.student_id, s.first_name, s.last_name, s.email, s.phone, s.image_url, s.status
                    FROM Student s
                    JOIN `Order` o ON s.student_id = o.user_id
                    WHERE o.course_id = %s AND o.status = 'Completed'
                    '''
    cursor.execute(student_query, (course_id,))
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('teacher_view_students.html', students=students, course_id=course_id)


@teacher.route("/edit_course/<int:course_id>", methods=['GET', 'POST'])
def edit_course(course_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    cursor, connection = get_cursor()
    # Edit course info
    if request.method == 'POST':
        # course info
        course_name = request.form['courseName']
        description = request.form['description']
        duration = request.form['duration']
        price = request.form['price']
        image_url = request.files.get('image_url')
        # quiz
        quiz_title = request.form['quizTitle']
        quiz_description = request.form['quizDescription']
        if quiz_title and quiz_description:
            cursor.execute("SELECT quiz_id FROM Quiz WHERE course_id = %s", (course_id,))
            quiz = cursor.fetchone()
            if quiz:
                cursor.execute("UPDATE Quiz SET title = %s, description = %s WHERE course_id = %s", (quiz_title, quiz_description, course_id))
            else:
                cursor.execute("INSERT INTO Quiz (course_id, title, description) VALUES (%s, %s, %s)", (course_id, quiz_title, quiz_description))
        # Edit course info
        update_query = '''
                        UPDATE Course
                        SET course_name = %s, description = %s, duration = %s, price = %s
                        WHERE course_id = %s
                        '''
        cursor.execute(update_query, (course_name, description, duration, price, course_id))

        if image_url and image_url.filename:
            image_path = upload(image_url)
            if image_path:
                cursor.execute('UPDATE Course SET image_url = %s WHERE course_id = %s', (image_path, course_id))
        # Edit section
        sections = [key for key in request.form.keys() if key.startswith('sectionTitle')]
        for key in sections:
            section_id = key.split('sectionTitle')[1]
            title = request.form[key]
            content = request.form['sectionContent' + section_id]
            cursor.execute('UPDATE Section SET title = %s, content = %s WHERE section_id = %s', (title, content, section_id))
        # Edit question

        cursor.execute("SELECT quiz_id FROM Quiz WHERE course_id = %s", (course_id,))
        quiz_id = cursor.fetchone()[0]
        questions = request.form.getlist('questionIds')
        for question_id in questions:
            question_text = request.form[f'question{question_id}']
            answerA = request.form[f'answerA{question_id}']
            answerB = request.form[f'answerB{question_id}']
            answerC = request.form[f'answerC{question_id}']
            correct_answer = request.form[f'correctAnswer{question_id}']
            update_question = '''
                                UPDATE Question
                                SET question = %s, A = %s, B = %s, C = %s, answer = %s
                                WHERE question_id = %s AND quiz_id = %s
                                '''
            cursor.execute(update_question, (question_text, answerA, answerB, answerC, correct_answer, question_id, quiz_id))
        connection.commit()
        flash('Course updated successfully!')

        return redirect(url_for('teacher.teacher_courses'))
    # Fetch course
    course_query = "SELECT * FROM Course WHERE course_id = %s"
    cursor.execute(course_query, (course_id,))
    course = cursor.fetchone()
    # Fetch section
    section_query = "SELECT * FROM Section WHERE course_id = %s"
    cursor.execute(section_query, (course_id,))
    sections = cursor.fetchall()

    # Fetch quiz and question
    cursor.execute("SELECT * FROM Quiz WHERE course_id = %s", (course_id,))
    quizzes = cursor.fetchall()
    print(quizzes)
    quiz_questions = {}
    for quiz in quizzes:
        cursor.execute("SELECT * FROM Question WHERE quiz_id = %s", (quiz[0],))
        questions = cursor.fetchall()
        quiz_questions[quiz[0]] = questions
    print(quiz_questions)

    cursor.close()
    connection.close()
    return render_template('teacher_edit_course.html', course=course, sections=sections, quizzes=quizzes, quiz_questions=quiz_questions)
def upload(file):
    if file and file.filename:
                filename = secure_filename(file.filename)
                uploads_dir =os.path.join(current_app.root_path,'static','course')
                os.makedirs(uploads_dir, exist_ok=True)
                filepath = os.path.join(uploads_dir, filename)
                file.save(filepath.replace("\\", "/"))
                return filename

@teacher.route("/delete_course/<int:course_id>", methods=['POST'])
def delete_course(course_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    cursor, connection = get_cursor()
    try:
        cursor.execute('''
                        SELECT 1 FROM `Order`
                        WHERE course_id = %s AND status IN ('Pending', 'Completed')
                        LIMIT 1
                        ''', (course_id,))
        if cursor.fetchone():
            return jsonify({'succuss': False, 'error': 'Cannot deactivate course with active or pending enrollments.'}), 400
        # Delete course
        cursor.execute("UPDATE Course SET status = %s WHERE course_id = %s", ('Inactive', course_id,))
        connection.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


