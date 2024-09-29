from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_hashing import Hashing
from .database import get_cursor

login = Blueprint("login", __name__, static_folder="static", 
                       template_folder="templates")

hashing = Hashing()

@login.route('/', methods=['GET', 'POST'])
def login_page():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        user_password = request.form['password']
        cursor, connection = get_cursor()  
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, user_password, salt='abcd'):
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['role'] = account[3]
                if session['role'] == 'Student':
                   return redirect(url_for('visitor_home'))
                elif session['role'] == 'Teacher':
                   cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (session['id'],))
                   teacher = cursor.fetchone()
                   if teacher[9] == 'Active':
                       return redirect(url_for('teacher.teacher_dashboard'))
                   else:
                        msg = 'Your account is currently inactive. Please contact our administrator for assistance.'
                elif session['role'] == 'Expert':
                   return redirect(url_for('expert.expert_dashboard'))
                elif session['role'] == 'Administrator':
                   return redirect(url_for('administrator.admin_dashboard'))
            else:
                msg = 'Incorrect password!'
        else:
            msg = 'Incorrect username'
        
        cursor.close()  
        connection.close()  
    return render_template('login.html', msg=msg)

@login.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('visitor_home'))


