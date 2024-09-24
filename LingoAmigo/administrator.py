from LingoAmigo import app
from LingoAmigo import Blueprint
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify,current_app
from .database import get_cursor
from decimal import Decimal, InvalidOperation
import re
from flask_hashing import Hashing
from datetime import datetime, timedelta, date, time
from werkzeug.utils import secure_filename
import os

administrator = Blueprint("administrator", __name__, static_folder="static", 
                       template_folder="templates")

hashing = Hashing(app)



@administrator.route('/')
def admin_dashboard():
    if 'loggedin' in session: # Ensuring the user is a logged-in administrator
        user_role = session.get('role', None)
        user_id = session.get('id', None)
        cursor, connection = get_cursor() 

        #Fetch administrator profile info
        cursor.execute('SELECT * FROM Administrator WHERE admin_id = %s', (session['id'],))
        admin_profile = cursor.fetchone()

         
        #Fetch user account info
        cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
        admin_info = cursor.fetchone()

        cursor.close()  
        connection.close() 
        

        return render_template('admin_dashboard.html',admin_info = admin_info, admin_profile = admin_profile)
    return redirect(url_for('login.login_page'))




@administrator.route('/administrator/admin_edit_profile', methods=['GET', 'POST'])
def admin_edit_profile():
    if 'loggedin' in session :
        user_role = session.get('role', None)
        user_id = session.get('id', None)
        cursor, connection = get_cursor() 
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone = request.form.get('phone')
            title = request.form.get('title')
            description = request.form.get('description')
            email = request.form.get('email')
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
            
            if image_path:

                cursor.execute('''
                               UPDATE Administrator
                               SET first_name=%s, last_name=%s, email=%s, title=%s, description=%s, phone=%s, image_url=%s
                            WHERE admin_id=%s
                           ''', (first_name, last_name, email, title, description, phone, image_path, user_id))
            else:

                #update administrator info
                cursor.execute('''
                                UPDATE Administrator
                                SET first_name=%s, last_name=%s, email=%s, title=%s, description=%s, phone=%s
                                WHERE admin_id=%s
                           ''', (first_name, last_name, email, title, description, phone, user_id))
            flash('Profile updated successfully', 'success')
            return redirect(url_for('administrator.admin_dashboard', image_path=image_path))
        else:
            cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
            admin_info = cursor.fetchone()
            #fetch current administrator profile for edit
            cursor.execute('SELECT * FROM Administrator WHERE admin_id = %s', (session['id'],))
            admin_profile = cursor.fetchone()


            cursor.close()  
            connection.close() 

            return render_template('admin_edit_profile.html', admin_profile=admin_profile, admin_info=admin_info)
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
    






@administrator.route("/change_password", methods=["POST"])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))

    cursor, connection = get_cursor()
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    if new_password != confirm_password:
        flash('New password and confirm password do not match.')
        return redirect(url_for('administrator.admin_dashboard'))

    if not new_password or (len(new_password) < 8 or not any(char.isdigit() for char in new_password) or not any(char.isalpha() for char in new_password)):
        flash('Password must be at least 8 characters long and contain both letters and numbers.')
        return redirect(url_for('administrator.admin_dashboard'))

    hashed = hashing.hash_value(new_password, salt='abcd')

    update_account_query = '''
        UPDATE User
        SET password = %s
        WHERE user_id = %s
    '''
    cursor.execute(update_account_query, (hashed, session['id']))
    connection.commit()

    flash('Your password has been successfully updated.')
    return redirect(url_for('administrator.admin_dashboard'))


@administrator.route("/admin_all_courses")
def admin_all_courses():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    user_role = session.get('role', None)
    cursor, connection = get_cursor()
    courses_query = '''
                    SELECT c.course_id, c.course_name, c.image_url, c.status, l.language_id, l.language_name, c.price, c.discount_details
                    FROM Course c
                    JOIN Language l ON c.language_id = l.language_id
                    '''
    cursor.execute(courses_query)
    all_courses = cursor.fetchall()

    courses_with_discounts = []
    for course in all_courses:
        
        try:
            if course[7] and '%' in course[7]:
                discount_rate = Decimal(course[7].rstrip('%')) / 100
                discount_price = course[6] * (1 - discount_rate)
            else:
                discount_price = course[6]

        except InvalidOperation:
            discount_price = course[6]
        courses_with_discounts.append(course + (discount_price,))
            

    cursor.close()
    connection.close()
    return render_template('admin_all_courses.html', all_courses=courses_with_discounts, user_role=user_role)


@administrator.route("/edit_course/<int:course_id>", methods=['GET', 'POST'])
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
            video_file = request.files.get(f'sectionVideo{section_id}')
            cursor.execute('UPDATE Section SET title = %s, content = %s WHERE section_id = %s', (title, content, section_id))

            if video_file and video_file.filename:
                video_path = upload_video(video_file)
                cursor.execute('UPDATE Video SET video_url = %s WHERE section_id = %s', (video_path, section_id))
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

        return redirect(url_for('administrator.admin_all_courses'))
    # Fetch course
    course_query = "SELECT * FROM Course WHERE course_id = %s"
    cursor.execute(course_query, (course_id,))
    course = cursor.fetchone()
    # Fetch section
    section_query = '''
                    SELECT s.section_id, s.course_id, s.title, s.content, v.video_url
                    FROM Section s
                    LEFT JOIN Video v ON s.section_id = v.section_id
                    WHERE s.course_id = %s 
                    '''
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
def upload_video(file):
    if file and file.filename:
                filename = secure_filename(file.filename)
                uploads_dir =os.path.join(current_app.root_path,'static','videos')
                os.makedirs(uploads_dir, exist_ok=True)
                filepath = os.path.join(uploads_dir, filename)
                file.save(filepath.replace("\\", "/"))
                return filename

@administrator.route("/delete_course/<int:course_id>", methods=['POST'])
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


@administrator.route("/approve_course/<int:course_id>", methods=['POST'])
def approve_course(course_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    cursor, connection = get_cursor()
    try:
        # Approve course
        cursor.execute("UPDATE Course SET status = %s WHERE course_id = %s", ('Active', course_id,))
        connection.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@administrator.route("/admin_language")
def admin_language():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    cursor, connection = get_cursor()
    course_query = '''
                    SELECT course_id, course_name, language_id
                    FROM Course
                    ORDER BY language_id
                    '''
    cursor.execute(course_query)
    courses = cursor.fetchall()

    language_courses = {}
    for course in courses:
        if course[2] not in language_courses:
            language_courses[course[2]] = []
        language_courses[course[2]].append(course)
    cursor.close()
    connection.close()

    return render_template('admin_all_language.html', language_courses=language_courses)

@administrator.route("/add_language", methods=['POST'])
def add_language():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    language_name = request.form['language_name']
    image_url = request.files.get('image_url')
    cursor, connection = get_cursor()
    try:
        insert_query = "INSERT INTO Language (language_name, image_url) VALUES (%s, %s)"
        if image_url and image_url.filename:
                image_path = upload(image_url)
        else:
            image_path = None
        cursor.execute(insert_query, (language_name, image_path))
        connection.commit()
        return redirect(url_for('administrator.admin_language'))
    except Exception as e:
        connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
def upload(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        uploads_dir =os.path.join(current_app.root_path,'static','course')
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath.replace("\\", "/"))
        return filename
    
    
@administrator.route("/update_language/<int:language_id>", methods=['POST'])
def update_language(language_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    language_name = request.form['language_name']
    image_url = request.files.get('image_url')
    cursor, connection = get_cursor()
    try:
        if image_url and image_url.filename:
            image_path = upload(image_url)
            update_query = "UPDATE Language SET language_name = %s, image_url = %s WHERE language_id = %s"
            cursor.execute(update_query, (language_name, image_path, language_id))
        else:
            update_query = "UPDATE Language SET language_name = %s WHERE language_id = %s"
            cursor.execute(update_query, (language_name, language_id))
        
        connection.commit()
        return redirect(url_for('administrator.admin_language'))
    except Exception as e:
        connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
def upload(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        uploads_dir =os.path.join(current_app.root_path,'static','course')
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath.replace("\\", "/"))
        return filename
    
@administrator.route("/delete_post/<int:post_id>", methods=['GET'])
def delete_post(post_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    try:
        # Delete post and related replies
        delete_replies_query = "DELETE FROM Replies WHERE post_id = %s"
        cursor.execute(delete_replies_query, (post_id,))

        delete_post_query = "DELETE FROM Post WHERE post_id = %s"
        cursor.execute(delete_post_query, (post_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('student.discussion_board'))


@administrator.route("/delete_reply/<int:reply_id>/<int:post_id>", methods=['GET'])
def delete_reply(reply_id, post_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    try:
        # Delete replies
        delete_replies_query = "DELETE FROM Replies WHERE reply_id = %s"
        cursor.execute(delete_replies_query, (reply_id,))

        
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('student.post_details', post_id=post_id))


@administrator.route('view_students')
def view_students():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    student_query = '''
                    SELECT s.student_id, s.first_name, s.last_name, s.email, s.phone, s.image_url, s.status
                    FROM Student s
                    '''
    cursor.execute(student_query)
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_all_students.html', students=students)


@administrator.route('view_teachers')
def view_teachers():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    teacher_query = '''
                    SELECT *
                    FROM Teacher
                    '''
    cursor.execute(teacher_query)
    teachers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_all_teachers.html', teachers=teachers)


@administrator.route('view_experts')
def view_experts():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    expert_query = '''
                    SELECT *
                    FROM Expert
                    '''
    cursor.execute(expert_query)
    experts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_all_experts.html', experts=experts)


@administrator.route('/administrator/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    if 'loggedin' in session :


        # nationality list
        nationalities = ['American', 'Canadian', 'Chinese', 'Mexican', 'Brazilian', 'Argentinian', 'British', 'French', 'German', 'Italian', 'Spanish', 'Portuguese', 'Russian', 'Indian', 'Japanese', 'Korean', 'Australian', 'New Zealander', 'South African', 'Egyptian', 'Nigerian', 'Saudi', 'Emirati', 'Iranian', 'Turkish', 'Indonesian', 'Thai', 'Vietnamese', 'Filipino', 'Malaysian']
        cursor, connection = get_cursor() 
        # Fetch teacher details for the give teacher_id
        cursor.execute("SELECT * FROM Teacher WHERE teacher_id = %s", (teacher_id,))
        teacher_profile = cursor.fetchone()
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
                           ''', (first_name, last_name, email, title, nationality, description, phone, image_path, date_join, teacher_id))
            else:

                #update teacher info
                cursor.execute('''
                                UPDATE Teacher
                                SET first_name=%s, last_name=%s, email=%s, title=%s, nationality=%s, description=%s, phone=%s, date_join=%s
                                WHERE teacher_id=%s
                           ''', (first_name, last_name, email, title, nationality, description, phone, date_join, teacher_id))
            flash('Profile updated successfully', 'success')
            return redirect(url_for('administrator.view_teachers', image_path=image_path))
        else:
            cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
            teacher_info = cursor.fetchone()
            #fetch current teacher profile for edit
            cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (teacher_id,))
            teacher_profile = cursor.fetchone()


            cursor.close()  
            connection.close() 

            return render_template('admin_edit_teacher.html', teacher_profile=teacher_profile, teacher_info=teacher_info, nationalities=nationalities)
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
    



@administrator.route('/administrator/edit_expert/<int:expert_id>', methods=['GET', 'POST'])
def edit_expert(expert_id):
    if 'loggedin' in session :

        # nationality list
        nationalities = ['American', 'Canadian', 'Chinese', 'Mexican', 'Brazilian', 'Argentinian', 'British', 'French', 'German', 'Italian', 'Spanish', 'Portuguese', 'Russian', 'Indian', 'Japanese', 'Korean', 'Australian', 'New Zealander', 'South African', 'Egyptian', 'Nigerian', 'Saudi', 'Emirati', 'Iranian', 'Turkish', 'Indonesian', 'Thai', 'Vietnamese', 'Filipino', 'Malaysian']
        cursor, connection = get_cursor()
        # Fetch expert details for the give expert_id
        cursor.execute("SELECT * FROM Expert WHERE expert_id = %s", (expert_id,))
        expert_profile = cursor.fetchone()
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
                               UPDATE Expert
                               SET first_name=%s, last_name=%s, email=%s, title=%s, nationality=%s, description=%s, phone=%s, image_url=%s, date_join=%s
                            WHERE expert_id=%s
                           ''', (first_name, last_name, email, title, nationality, description, phone, image_path, date_join, expert_id))
            else:

                #update expert info
                cursor.execute('''
                                UPDATE Expert
                                SET first_name=%s, last_name=%s, email=%s, title=%s, nationality=%s, description=%s, phone=%s, date_join=%s
                                WHERE expert_id=%s
                           ''', (first_name, last_name, email, title, nationality, description, phone, date_join, expert_id))
            flash('Profile updated successfully', 'success')
            return redirect(url_for('administrator.view_experts', image_path=image_path))
        else:
            cursor.execute('SELECT * FROM User WHERE user_id = %s',(expert_id,))
            expert_info = cursor.fetchone()
            #fetch current expert profile for edit
            cursor.execute('SELECT * FROM Expert WHERE expert_id = %s', (expert_id,))
            expert_profile = cursor.fetchone()


            cursor.close()  
            connection.close() 

            return render_template('admin_edit_expert.html', expert_profile=expert_profile, expert_info=expert_info, nationalities=nationalities)
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
    

@administrator.route('/administrator/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'loggedin' in session :
        
        cursor, connection = get_cursor() 
        #fetch current student profile for edit
        cursor.execute('SELECT * FROM student WHERE student_id = %s', (student_id,))
        student_profile = cursor.fetchone()

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            date_birth = request.form.get('date_birth')
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
                date_birth = datetime.strptime(date_birth, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return redirect(request.url)
            
            if image_path:

                cursor.execute('''
                               UPDATE Student
                               SET first_name=%s, last_name=%s, phone=%s, email=%s, image_url=%s, date_birth=%s
                            WHERE student_id=%s
                           ''', (first_name, last_name, phone, email, image_path, date_birth, student_id))

            else:

                #update student info
                cursor.execute('''
                                UPDATE Student
                                SET first_name=%s, last_name=%s, phone=%s, email=%s, date_birth=%s
                                WHERE student_id=%s
                           ''', (first_name, last_name, phone, email, date_birth, student_id))
            flash('Profile updated successfully', 'success')
            return redirect(url_for('administrator.view_students', image_path=image_path))
        else:
            cursor.execute('SELECT * FROM User WHERE user_id = %s',(student_id,))
            student_info = cursor.fetchone()
            #fetch current student profile for edit
            cursor.execute('SELECT * FROM student WHERE student_id = %s', (student_id,))
            student_profile = cursor.fetchone()


            cursor.close()  
            connection.close() 

            return render_template('admin_edit_student.html', student_profile=student_profile, student_info=student_info)
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
    
@administrator.route('update_language_discount', methods=['POST'])
def update_language_discount():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()

    langauge_id = request.form.get('language_id')
    discount = request.form.get('discount')

    try:
        cursor.execute("UPDATE Course SET discount_details = %s WHERE language_id = %s", (discount, langauge_id))
        connection.commit()
        flash('Discount updated successfully!', 'success')
    except Exception as e:
        connection.rollback()
        flash(f'An error occurred: {str(e)}', 'error')
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('administrator.admin_all_courses'))

    
@administrator.route('update_course_discount', methods=['POST'])
def update_course_discount():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()

    course_id = request.form.get('course_id')
    discount = request.form.get('discount')

    try:
        cursor.execute("UPDATE Course SET discount_details = %s WHERE course_id = %s", (discount, course_id))
        connection.commit()
        flash('Discount updated successfully!', 'success')
    except Exception as e:
        connection.rollback()
        flash(f'An error occurred: {str(e)}', 'error')
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('administrator.admin_all_courses'))

@administrator.route('/approve_teacher/<int:teacher_id>', methods=['POST'])
def approve_teacher(teacher_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    cursor, connection = get_cursor()
    try:
        cursor.execute("UPDATE Teacher SET status = 'Active' WHERE teacher_id = %s", (teacher_id,))
        connection.commit()
        return jsonify({'success': 'Teacher approved successfully'}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()