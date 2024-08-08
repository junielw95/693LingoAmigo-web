from LingoAmigo import app
from LingoAmigo import Blueprint
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify,current_app
from .database import get_cursor
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

