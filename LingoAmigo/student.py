from LingoAmigo import app
import re
from LingoAmigo import Blueprint
from .database import get_cursor
from flask import Blueprint, session, url_for, render_template, redirect, request, flash, current_app, jsonify
from flask_hashing import Hashing
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from decimal import Decimal
from datetime import datetime, timedelta, date

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
                SELECT c.course_id, c.course_name, c.price, c.image_url, o.order_id
                FROM Course c
                JOIN `Order` o ON c.course_id = o.course_id
                WHERE o.user_id = %s AND o.status = 'Incart'
                '''
    cursor.execute(cart_query, (user_id,))
    cart_items = cursor.fetchall()

    cursor.close()  
    connection.close() 
    return render_template('shopping_cart.html', cart_items=cart_items, user_role=user_role)


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
                    SELECT course_id, course_name, price, image_url
                    FROM Course
                    WHERE course_id IN (%s)
                    ''' % ','.join(['%s'] * len(selected_course_ids))
    cursor.execute(course_query, tuple(selected_course_ids))
    cart_items = cursor.fetchall()

    total_price = sum(item[2] for item in cart_items)

    cursor.close()  
    connection.close() 

    return render_template('course_checkout.html', cart_items=cart_items, total_price=total_price)

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
        cursor.execute("SELECT s.course_id, s.section_id FROM Section s JOIN Video v ON s.section_id = v.section_id WHERE v.video_id = %s", (video_id,))
        course_result = cursor.fetchone()
        if not course_result:
            flash('Video not found.', 'error')
            return redirect(url_for('student.student_dashboard'))
        course_id, section_id = course_result

        cursor.execute("SELECT 1 FROM `Order` WHERE user_id = %s AND course_id = %s AND status = 'Completed'", (session.get('id'), course_id))
        if cursor.fetchone() is None:
            flash('You do not have access to this video.', 'error')
            return redirect(url_for('visitor.course_details', course_id=course_id))
        
        #Fetch video
        cursor.execute("SELECT video_url, section_id FROM Video WHERE video_id = %s", (video_id,))
        video_details = cursor.fetchone()

        cursor.execute("SELECT title, content FROM Section WHERE section_id = %s", (section_id,))
        section_details = cursor.fetchone()

        if video_details:
            return render_template('video.html', video_url=video_details[0], course_id=course_id, section_title=section_details[0], section_content=section_details[1])
        else:
            flash('Video details not found.', 'error')
            return redirect(url_for('visitor.course_details', course_id=course_id))
    finally:
        cursor.close()
        connection.close()