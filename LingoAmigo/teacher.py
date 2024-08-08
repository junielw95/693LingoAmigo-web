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

