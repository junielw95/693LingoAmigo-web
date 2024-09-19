from LingoAmigo import app
import re
from LingoAmigo import Blueprint
from .database import get_cursor
from flask import Blueprint, session, url_for, render_template, redirect, request, flash, current_app, jsonify
from flask_hashing import Hashing
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta, date
from math import ceil

student = Blueprint("student", __name__, static_folder="static", 
                       template_folder="templates")

hashing = Hashing(app)

@student.route('/')
def student_dashboard():
    if 'loggedin' in session: # Ensuring the user is a logged-in student
        user_role = session.get('role', None)
        user_id = session.get('id', None)
        cursor, connection = get_cursor() 

        #Fetch student profile info
        cursor.execute('SELECT * FROM Student WHERE student_id = %s', (session['id'],))
        student_profile = cursor.fetchone()

         
        #Fetch user account info
        cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
        student_info = cursor.fetchone()

        cursor.close()  
        connection.close() 
        

        return render_template('student_dashboard.html',student_info = student_info, student_profile = student_profile)
    return redirect(url_for('login.login_page'))


@student.route('/student/student_edit_profile', methods=['GET', 'POST'])
def student_edit_profile():
    if 'loggedin' in session :
        user_role = session.get('role', None)
        user_id = session.get('id', None)
        cursor, connection = get_cursor() 
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
                           ''', (first_name, last_name, phone, email, image_path, date_birth, user_id))

            else:

                #update student info
                cursor.execute('''
                                UPDATE Student
                                SET first_name=%s, last_name=%s, phone=%s, email=%s, date_birth=%s
                                WHERE student_id=%s
                           ''', (first_name, last_name, phone, email, date_birth, user_id))
            flash('Profile updated successfully', 'success')
            return redirect(url_for('student.student_dashboard', image_path=image_path))
        else:
            cursor.execute('SELECT * FROM User WHERE user_id = %s',(session['id'],))
            student_info = cursor.fetchone()
            #fetch current student profile for edit
            cursor.execute('SELECT * FROM student WHERE student_id = %s', (session['id'],))
            student_profile = cursor.fetchone()


            cursor.close()  
            connection.close() 

            return render_template('student_edit_profile.html', student_profile=student_profile, student_info=student_info, user_role=user_role)
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
    




@student.route("/change_password", methods=["POST"])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))

    cursor, connection = get_cursor()
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    if new_password != confirm_password:
        flash('New password and confirm password do not match.')
        return redirect(url_for('student.student_dashboard'))

    if not new_password or (len(new_password) < 8 or not any(char.isdigit() for char in new_password) or not any(char.isalpha() for char in new_password)):
        flash('Password must be at least 8 characters long and contain both letters and numbers.')
        return redirect(url_for('student.student_dashboard'))

    hashed = hashing.hash_value(new_password, salt='abcd')

    update_account_query = '''
        UPDATE User
        SET password = %s
        WHERE user_id = %s
    '''
    cursor.execute(update_account_query, (hashed, session['id']))
    connection.commit()

    flash('Your password has been successfully updated.')
    return redirect(url_for('student.student_dashboard'))

@student.route('/cart')
def cart():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))

    user_role = session.get('role', None)
    user_id = session.get('id', None)
    cursor, connection = get_cursor()
    cart_query = '''
                SELECT c.course_id, c.course_name, c.price, c.image_url, o.order_id, c.discount_details
                FROM Course c
                JOIN `Order` o ON c.course_id = o.course_id
                WHERE o.user_id = %s AND o.status = 'Incart'
                '''
    cursor.execute(cart_query, (user_id,))
    cart_items = cursor.fetchall()

    
    # calculate the discounted price
    
    courses_with_discounts = []
    for course in cart_items:
        
        try:
            if course[5] and course[5] != 'None':
                discount_rate = Decimal(course[5].rstrip('%')) / 100
                discount_price = course[2] * (1 - discount_rate)
            else:
                discount_price = course[2]

        except InvalidOperation:
            discount_price = course[2]
        courses_with_discounts.append(course + (discount_price,))
            
    

    cursor.close()  
    connection.close() 
    return render_template('shopping_cart.html', cart_items=courses_with_discounts, user_role=user_role)


@student.route("/add_to_cart/<int:course_id>", methods=["POST"])
def add_to_cart(course_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))

    user_id = session.get('id', None)
    cursor, connection = get_cursor()
    cursor.execute('SELECT * FROM `Order` WHERE user_id = %s AND course_id = %s', (user_id, course_id))
    existing_order = cursor.fetchone()
    if existing_order and existing_order[4] not in ["InCart", "Cancelled"]:
            return jsonify({'error':'Course already purchased.'}), 409
    if not existing_order or existing_order[4] =="Cancelled":
        cursor.execute('INSERT INTO `Order` (user_id, course_id, order_date, status) VALUES (%s, %s, CURDATE(), %s)', (user_id, course_id, "InCart"))
        connection.commit()

    cursor.close()  
    connection.close() 
    return jsonify({'success': 'Course added to cart'}), 200


@student.route('/remove_from_cart/<int:order_id>', methods=['POST'])
def remove_from_cart(order_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))

    cursor, connection = get_cursor()
    cursor.execute('DELETE FROM `Order` WHERE order_id = %s', (order_id,))
    connection.commit()

    cursor.close()  
    connection.close() 
    return jsonify({'success': 'Course removed from cart'}), 200

@student.route('/checkout')
def checkout():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    
    selected_course_ids = request.args.getlist('selected_courses')
    if not selected_course_ids:
        flash('No courses selected for checkout.', 'error')
        return redirect(url_for('student.cart'))
    
    selected_course_ids = request.args.get('selected_courses', '').split(',')

    cursor, connection = get_cursor()
    course_query = '''
                    SELECT course_id, course_name, price, image_url, discount_details
                    FROM Course
                    WHERE course_id IN (%s)
                    ''' % ','.join(['%s'] * len(selected_course_ids))
    cursor.execute(course_query, tuple(selected_course_ids))
    cart_items = cursor.fetchall()
    
    # calculate the discounted price
    
    courses_with_discounts = []
    for course in cart_items:
        
        try:
            if course[4] and course[4] != 'None':
                discount_rate = Decimal(course[4].rstrip('%')) / 100
                discount_price = course[2] * (1 - discount_rate)
            else:
                discount_price = course[2]

        except InvalidOperation:
            discount_price = course[2]
        courses_with_discounts.append(course + (discount_price,))

    # calculate total price considering discounts
    total_price = 0
    for course in cart_items:  
        if course[4] and course[4] != 'None':
            discount_rate = Decimal(course[4].rstrip('%')) / 100
            discount_price = course[2] * (1 - discount_rate)
        else:
            discount_price = course[2]
        total_price += discount_price  

   

    cursor.close()  
    connection.close() 

    return render_template('course_checkout.html', cart_items=courses_with_discounts, total_price=total_price)

@student.route('make_payment', methods = ['POST'])
def make_payment():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    cursor, connection = get_cursor()
    selected_course_ids = request.form.getlist('selected_courses')
    print("Selected Course IDs: ", selected_course_ids)
    try:
        card_number = request.form.get('card_number')
        card_name = request.form.get('name')
        expiry_mm = request.form.get('expiry_mm')
        expiry_yy = request.form.get('expiry_yy')
        cvc = request.form.get('cvc')
        

        # Validate card expiry
        if not expiry_mm or not expiry_yy:
            flash('Expiry month and year must be provided.', 'error')
            return redirect(url_for('student.checkout'))
        try:
            expiry_date = datetime(int(expiry_yy), int(expiry_mm), 1)
            if expiry_date <= datetime.now():
                raise ValueError('Your credit card is expired.')
    
        except ValueError as e:
            flash('Invalid expiry date.', 'error')
            return redirect(url_for('student.checkout'))
        
        # card number not none
        if not card_number:
            flash('Card Number is required.', 'error')
            return redirect(url_for('student.checkout'))
    
    # Update orders
        
        for course_id in selected_course_ids:
            update_query = '''
                            UPDATE `Order`
                            SET order_date = CURDATE(), status = 'Completed'
                            WHERE course_id = %s AND user_id = %s AND status IN ('InCart', 'Pending')
                            '''
            cursor.execute(update_query, (course_id, session['id'])) 
            print(update_query)
        connection.commit()
        flash('Payment successful and orders updated.', 'success')
        return redirect(url_for('student.student_courses'))
    
    except Exception as e:
        for course_id in selected_course_ids:
            update_query = '''
                            UPDATE `Order`
                            SET order_date = CURDATE(), status = 'Pending'
                            WHERE course_id = %s AND user_id = %s AND status = 'InCart'
                            '''
            cursor.execute(update_query, (course_id, session['id']))
        connection.commit()
        print("Error during payment processing: ", e)
        flash(f'Payment failed: {str(e)}', 'success')
        return redirect(url_for('student.checkout'))
    finally:
        cursor.close()
        connection.close()

@student.route('/student_courses')
def student_courses():
    if 'loggedin' not in session:
            return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    cursor, connection = get_cursor()

    view_courses_query = '''
                        SELECT c.course_id, c.course_name, c.price, c.image_url, o.status, o.order_id,
                        l.language_id, l.language_name,
                        CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
                        t.teacher_id
                        FROM Course c
                        JOIN `Order` o ON c.course_id = o.course_id
                        JOIN Teacher t ON c.creator_id = t.teacher_id
                        JOIN Language l ON c.language_id = l.language_id
                        WHERE o.user_id = %s AND o.status IN ('Completed', 'Cancelled', 'Pending')
                        '''
    cursor.execute(view_courses_query,(user_id,))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('student_courses.html', courses=courses)

@student.route('/unsubscribe/<int:order_id>', methods=['POST'])
def unsubscribe(order_id):
    if 'loggedin' not in session:
            return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    cursor, connection = get_cursor()
    try:
        update_order_query = '''
                            UPDATE `Order`
                            SET order_date = CURDATE(), status = 'Cancelled'
                            WHERE order_id = %s AND user_id = %s
                            '''
        cursor.execute(update_order_query, (order_id, user_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify({'success': True})

@student.route('/play_video/<int:video_id>')
def play_video(video_id):
    cursor, connection = get_cursor()
    try:
        cursor.execute("SELECT s.course_id, s.section_id, c.creator_id FROM Section s JOIN Video v ON s.section_id = v.section_id JOIN Course c ON s.course_id = c.course_id WHERE v.video_id = %s", (video_id,))
        course_result = cursor.fetchone()
        if not course_result:
            flash('Video not found.', 'error')
            return redirect(url_for('student.student_dashboard'))
        course_id, section_id, creator_id = course_result

        # Check if user has purchased the course
        user_id = session.get('id')
        user_role = session.get('role')
        has_access = False
        if user_role in ['Administrator', 'Expert'] or user_id == creator_id:
            has_access = True
        else:
            if user_role == 'Student':
                cursor.execute("SELECT 1 FROM `Order` WHERE user_id = %s AND course_id = %s AND status = 'Completed'", (session.get('id'), course_id))
                has_access = cursor.fetchone() is not None
        if not has_access:
                flash('You do not have access to this video.', 'error')
                return redirect(url_for('visitor.course_details', course_id=course_id))
            
        #Fetch video
        cursor.execute("SELECT video_url, section_id FROM Video WHERE video_id = %s", (video_id,))
        video_details = cursor.fetchone()
        #Fetch video description
        cursor.execute("SELECT title, content FROM Section WHERE section_id = %s", (section_id,))
        section_details = cursor.fetchone()
        #Fetch comments
        comments_query = '''
                            SELECT c.content, c.timestamp, CONCAT(s.first_name, ' ', s.last_name) AS full_name
                            FROM VideoComments c
                            JOIN Student s ON c.user_id = s.student_id
                            WHERE c.video_id = %s
                            ORDER BY c.timestamp DESC
                        '''
        cursor.execute(comments_query, (video_id,))
        comments = cursor.fetchall()
        if video_details:
            return render_template('video.html', video_url=video_details[0], course_id=course_id, section_title=section_details[0], section_content=section_details[1], comments=comments, video_id=video_id)
        else:
            flash('Video details not found.', 'error')
            return redirect(url_for('visitor.course_details', course_id=course_id))
    finally:
        cursor.close()
        connection.close()


@student.route('/add_comment/<int:video_id>', methods=['POST'])
def add_comment(video_id):
    content = request.form.get('content')
    user_id = session.get('id', None)
    cursor, connection = get_cursor()
    try:
        cursor.execute("INSERT INTO VideoComments (video_id, user_id, content, timestamp) VALUES (%s, %s, %s, NOW())", (video_id, user_id, content))
        connection.commit()
        flash('Comment added successfully.', 'success')
    except Exception as e:
        connection.rollback()
        flash(f"Error adding comment: {str(e)}", 'error')
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('student.play_video', video_id=video_id))

@student.route('/quiz/<int:course_id>/<int:quiz_id>')
def quiz_page(course_id, quiz_id, results=None, score=None):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    user_role = session.get('role', None)
    cursor, connection = get_cursor()

    # Check if user is expert or admin or the teacher who create the course
    cursor.execute("SELECT creator_id FROM Course WHERE course_id = %s", (course_id,))
    course_creator = cursor.fetchone()
    if course_creator and (session['role'] == 'Teacher' and course_creator[0] == user_id) or user_role in ['Expert', 'Administrator']:
        pass
    else:
        cursor.execute("SELECT 1 FROM `Order` WHERE user_id = %s AND course_id = %s AND status = 'Completed'", (user_id, course_id)) # Check if user has purchased the course
        if cursor.fetchone() is None:
            flash('You do not have access to this quiz.', 'error')
            return redirect(url_for('course_details', course_id=course_id))
        

    # Fetch quiz
    cursor.execute("SELECT * FROM Quiz WHERE course_id = %s", (course_id,))
    quiz = cursor.fetchone()
    quiz_id=quiz[0]
    if not quiz:
        flash('Quiz not found.', 'error')
        return redirect(url_for('visitor.course_details', course_id=course_id))
    cursor.execute("SELECT * FROM Quiz WHERE course_id = %s", (course_id,))
    quizs = cursor.fetchall()

    # Fetch questions
    cursor.execute("SELECT * FROM Question WHERE quiz_id = %s", (quiz_id,))
    questions = cursor.fetchall()

    cursor.close()
    connection.close()

    results = session.get('quiz_results', [])
    score = session.get('quiz_score', 0)

    return render_template('quiz.html', questions=questions, quiz=quiz, course_id=course_id, quiz_id=quiz_id, results=results, score=score, quizs=quizs)

@student.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    cursor, connection = get_cursor()

    # get course_id
    course_id=request.form.get('course_id')

    # Fetch questions
    cursor.execute("SELECT * FROM Question WHERE quiz_id = %s", (quiz_id,))
    questions = cursor.fetchall()

    results = []
    score = 0

    for question in questions:
        student_answer = request.form.get(f'question{question[0]}')
        is_correct = student_answer == question[6]
        score += is_correct
        results.append({'question':question, 'is_correct': is_correct, 'student_answer': student_answer})
        
    cursor.close()
    connection.close()

    session['quiz_results'] = results
    session['quiz_score'] = score
    session.modified = True



    return redirect(url_for('student.quiz_page', course_id=course_id, quiz_id=quiz_id))


@student.route('/reset_quiz/<int:course_id>/<int:quiz_id>')
def reset_quiz(course_id, quiz_id):
    if 'quiz_results' in session:
        del session['quiz_results']
    if 'quiz_score' in session:
        del session['quiz_score']
    session.modified = True
    return redirect(url_for('student.quiz_page', course_id=course_id, quiz_id=quiz_id))


@student.route('/discussion_board')
def discussion_board():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)

    
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    keyword = request.args.get('keyword', '')
    language = request.args.get('language', None)
    
    cursor, connection = get_cursor()

    base_query = '''
                FROM Post p
                JOIN User u ON p.user_id = u.user_id
                LEFT JOIN Student s ON u.user_id = s.student_id
                LEFT JOIN Teacher t ON u.user_id = t.teacher_id
                LEFT JOIN Expert e ON u.user_id = e.expert_id
                LEFT JOIN Administrator a ON u.user_id = a.admin_id
                JOIN DiscussionBoard d ON p.discussion_id = d.discussion_id
                JOIN Language l ON d.language_id = l.language_id
                WHERE (p.topic LIKE %s OR p.content LIKE %s)
                '''
    # For search bar
    search_values = [f'%{keyword}%', f'%{keyword}%']

    
    # For language filter
    if language:
        base_query += ' AND l.language_id = %s'
        search_values.append(language)

    # Count total posts with filters
    count_query = "SELECT COUNT(*) " + base_query
    cursor.execute(count_query, search_values)
    total_posts = cursor.fetchone()[0]
    total_pages = ceil(total_posts / per_page)

    # Fetch post
    post_query = f'''
                SELECT p.post_id, p.topic, p.content, p.timestamp, u.user_id, u.username, u.role,
                    COALESCE(s.image_url, t.image_url, e.image_url, a.image_url) AS image_url,
                    COALESCE(s.first_name, t.first_name, e.first_name, a.first_name) AS first_name,
                    COALESCE(s.last_name, t.last_name, e.last_name, a.last_name) AS last_name,
                    l.language_name
                {base_query}
                ORDER BY p.timestamp DESC
                LIMIT %s OFFSET %s
                '''
    full_search_values = search_values + [per_page, offset]
    cursor.execute(post_query, full_search_values)
    posts = cursor.fetchall()

            
    cursor.close()
    connection.close()

    return render_template('discussion_board.html', posts=posts, total_pages=total_pages, current_page=page, keyword=keyword, language=language)

@student.route('/submit_post', methods=['POST'])
def submit_post():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)

    topic = request.form['topic']
    content = request.form['content']
    language_id = request.form['language_id']
    course_id = request.form.get('course_id')
    
    cursor, connection = get_cursor()
    # Insert data to DiscussionBoard table
    discussion_query = '''
                        INSERT INTO DiscussionBoard (course_id, language_id)
                        VALUES (%s, %s)
                        '''
    cursor.execute(discussion_query, (course_id if course_id else None, language_id))
    discussion_id = cursor.lastrowid
    # Insert data to Post table
    post_query = '''
                    INSERT INTO Post (discussion_id, user_id, topic, content)
                    VALUES (%s, %s, %s, %s)
                    '''
    cursor.execute(post_query, (discussion_id, user_id, topic, content))

    connection.commit()  
    cursor.close()
    connection.close()

    return redirect(url_for('student.discussion_board'))

@student.route('/post_details/<int:post_id>')
def post_details(post_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)
    cursor, connection = get_cursor()

    # Fetch posts
    post_query = '''
                SELECT p.post_id, p.topic, p.content, p.timestamp, u.user_id, u.username, u.role,
                    COALESCE(s.image_url, t.image_url, e.image_url, a.image_url) AS image_url,
                    COALESCE(s.first_name, t.first_name, e.first_name, a.first_name) AS first_name,
                    COALESCE(s.last_name, t.last_name, e.last_name, a.last_name) AS last_name,
                    l.language_name
                    FROM Post p
                JOIN User u ON p.user_id = u.user_id
                LEFT JOIN Student s ON u.user_id = s.student_id
                LEFT JOIN Teacher t ON u.user_id = t.teacher_id
                LEFT JOIN Expert e ON u.user_id = e.expert_id
                LEFT JOIN Administrator a ON u.user_id = a.admin_id
                JOIN DiscussionBoard d ON p.discussion_id = d.discussion_id
                JOIN Language l ON d.language_id = l.language_id
                WHERE p.post_id = %s
                '''
    cursor.execute(post_query, (post_id,))
    post = cursor.fetchone()

    # Fetch replies
    replies_query = '''
                    SELECT r.content, r.timestamp, u.user_id, u.role,
                        COALESCE(s.image_url, t.image_url, e.image_url, a.image_url) AS image_url,
                        COALESCE(s.first_name, t.first_name, e.first_name, a.first_name) AS first_name,
                        COALESCE(s.last_name, t.last_name, e.last_name, a.last_name) AS last_name,
                        r.reply_id
                    FROM Replies r
                    JOIN User u ON r.user_id = u.user_id
                    LEFT JOIN Student s ON u.user_id = s.student_id
                    LEFT JOIN Teacher t ON u.user_id = t.teacher_id
                    LEFT JOIN Expert e ON u.user_id = e.expert_id
                    LEFT JOIN Administrator a ON u.user_id = a.admin_id
                    WHERE r.post_id = %s
                    ORDER BY r.timestamp ASC
                    '''
    cursor.execute(replies_query, (post_id,))
    replies = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('post_details.html', post=post, replies=replies)

@student.route('/submit_reply/<int:post_id>', methods=['POST'])
def submit_reply(post_id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    user_id = session.get('id', None)

    content = request.form['reply_content']

    cursor, connection = get_cursor()

    # Insert reply into Replies table
    reply_query = '''
                    INSERT INTO Replies (post_id, user_id, content)
                    VALUES (%s, %s, %s)
                    '''
    cursor.execute(reply_query, (post_id, user_id, content))
    reply_id = cursor.lastrowid

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('student.post_details', post_id=post_id, reply_id=reply_id))

@student.route('/student_session')
def student_session():
    return render_template('student_session.html')
    

@student.route('/start_session', methods=['POST'])
def start_session():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    student_id = request.form['student_id']
    expert_id = request.form['expert_id']
    try:
        cursor, connection = get_cursor()

        cursor.execute("INSERT INTO Session (student_id, expert_id, start_time, status) VALUES (%s, %s, NOW(), 'InProgress')", (student_id, expert_id))
        session_id = cursor.lastrowid

        connection.commit()
        return jsonify({'session_id': session_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    

@student.route('send_message', methods=['POST'])
def send_message():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    data = request.get_json()
    session_id = data['session_id']
    message = data['message']
    try:
        cursor, connection = get_cursor()

        cursor.execute("INSERT INTO Messages (session_id, message, timestamp) VALUES (%s, %s, NOW())", (session_id, message))
        
        connection.commit()
        return jsonify({'message': 'Message sent'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    

@student.route('get_message', methods=['GET'])
def get_message():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    session_id = request.args.get('session_id')
    try:
        cursor, connection = get_cursor()

        cursor.execute("SELECT message, timestamp FROM Messages WHERE session_id = %s ORDER BY timestamp ASC", (session_id,))
        messages = cursor.fetchall()
        return jsonify({'messages': messages}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    

@student.route('complete_session', methods=['POST'])
def complete_session():
    if 'loggedin' not in session:
        return redirect(url_for('login.login_page'))
    session_id = request.form['session_id']
    try:
        cursor, connection = get_cursor()

        cursor.execute("UPDATE Session SET status='Completed' WHERE session_id=%s", (session_id,))
        connection.commit()
        return jsonify({'status': 'Session completed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()