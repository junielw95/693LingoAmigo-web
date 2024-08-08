from LingoAmigo import app
from .database import get_cursor
from LingoAmigo import Blueprint
from flask import Blueprint, render_template, request, g, session
from math import ceil

visitor = Blueprint("visitor", __name__, static_folder="static", 
                       template_folder="templates")



@app.route('/')
def visitor_home():
    cursor, connection = get_cursor() 
    #Fetch teacher profile info
    cursor.execute('SELECT * FROM Teacher')
    teachers = cursor.fetchall()

    language_filter = request.args.get('language_id', type=int)
    #Fetch all courses
    course_query = '''
                    SELECT c.course_id, c.course_name, c.description, c.duration, c.price, c.image_url, c.status,
                            CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
                            l.language_name, l.language_id,
                            t.image_url AS teacher_image, t.teacher_id
                    FROM Course c
                    JOIN Teacher t ON c.creator_id = t.teacher_id
                    JOIN Language l ON c.language_id = l.language_id 
                    LIMIT 8
                    '''
    if language_filter:
        course_query += " WHERE l.language_id = %s"
        cursor.execute(course_query, (language_filter,))
    else:
        cursor.execute(course_query)
    course_list = cursor.fetchall()
    current_language = None
    if language_filter and course_list:
        current_language = course_list[0][8]
    cursor.close()  
    connection.close() 

    cursor.close()  
    connection.close() 
    return render_template('index.html', teachers=teachers, course_list=course_list, current_language=current_language)


@app.route('/about')
def about():
    cursor, connection = get_cursor() 
    #Fetch teacher profile info
    cursor.execute('SELECT * FROM Teacher')
    teachers = cursor.fetchall()

    #Fetch expert profile info
    cursor.execute('SELECT * FROM Expert')
    experts = cursor.fetchall()

    cursor.close()  
    connection.close() 

    return render_template('about.html', teachers=teachers, experts=experts)


@app.route('/contact')
def contact():


    return render_template('contact.html')

@app.route('/teachers')
def teachers():
    cursor, connection = get_cursor() 
    search_query = request.args.get('search', '')
    if search_query:
        search_query = f"%{search_query}%"
        cursor.execute('SELECT * FROM Teacher WHERE first_name LIKE %s OR last_name LIKE %s OR nationality LIKE %s', (search_query, search_query, search_query))
    else:
        cursor.execute('SELECT * FROM Teacher')


    teachers = cursor.fetchall()

    cursor.close()  
    connection.close() 
    return render_template('teachers_list.html', teachers=teachers)



@app.route('/teacher/<int:teacher_id>')
def teacher_profile(teacher_id):
    cursor, connection = get_cursor() 
    #Fetch teacher profile info
    cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (teacher_id,))
    teacher = cursor.fetchone()

    cursor.close()  
    connection.close() 
    if teacher is None:
        return "Teacher not found", 404
    
    return render_template('teachers_list_profile.html', teacher=teacher)



@app.route('/expert/<int:expert_id>')
def expert_profile(expert_id):
    cursor, connection = get_cursor() 
    #Fetch expert profile info
    cursor.execute('SELECT * FROM Expert WHERE expert_id = %s', (expert_id,))
    expert = cursor.fetchone()

    cursor.close()  
    connection.close() 
    if expert is None:
        return "Expert not found", 404
    
    return render_template('expert_list_profile.html', expert=expert)

@app.context_processor
def languages():
    if not hasattr(g, 'languages'):

        cursor, connection = get_cursor() 
        cursor.execute('SELECT * FROM Language')
        g.languages = cursor.fetchall()

        cursor.close()  
        connection.close() 
    

    return dict(languages=g.languages)

@app.route('/courses')
def courses():
    cursor, connection = get_cursor() 
    language_filter = request.args.get('language_id', type=int)
    #Fetch all courses
    course_query = '''
                    SELECT c.course_id, c.course_name, c.description, c.duration, c.price, c.image_url, c.status,
                            CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
                            l.language_name, l.language_id,
                            t.image_url AS teacher_image, t.teacher_id
                    FROM Course c
                    JOIN Teacher t ON c.creator_id = t.teacher_id
                    JOIN Language l ON c.language_id = l.language_id 
                    '''
    if language_filter:
        course_query += " WHERE l.language_id = %s"
        cursor.execute(course_query, (language_filter,))
    else:
        cursor.execute(course_query)
    course_list = cursor.fetchall()
    current_language = None
    if language_filter and course_list:
        current_language = course_list[0][8]
    cursor.close()  
    connection.close() 
    return render_template('courses.html', course_list=course_list, language_filter=language_filter, current_language=current_language)


@app.route('/course_details/<int:course_id>')
def course_details(course_id):
    cursor, connection = get_cursor()
    user_role = session.get('role', None)
    #Fetch all courses
    course_query = '''
                    SELECT c.course_id, c.course_name, c.description, c.duration, c.price, c.image_url, c.status,
                            CONCAT(t.first_name, ' ', t.last_name) AS teacher_name, t.image_url AS teacher_image,
                            l.language_name, l.language_id,
                            t.teacher_id
                    FROM Course c
                    JOIN Teacher t ON c.creator_id = t.teacher_id
                    JOIN Language l ON c.language_id = l.language_id
                    WHERE c.course_id = %s 
                    '''

    cursor.execute(course_query, (course_id,))
    course = cursor.fetchone()
    if course is None:
        return "Course not found", 404
    section_query = '''
                    SELECT s.title, s.content
                    FROM Section s
                    WHERE s.course_id = %s
                    '''
    cursor.execute(section_query, (course_id,))
    sections = cursor.fetchall()

    section_count = '''
                    SELECT COUNT(*)
                    FROM Section
                    WHERE course_id = %s
                    '''
    cursor.execute(section_count, (course_id,))
    section_count = cursor.fetchone()[0]

    related_courses = '''
                        SELECT course_id, course_name, price, image_url
                        FROM Course
                        WHERE language_id = %s AND course_id !=%s
                        ORDER BY RAND()
                        LIMIT 6
                    '''
    cursor.execute(related_courses, (course[10], course_id))
    related_courses = cursor.fetchall()
    cursor.close()  
    connection.close() 
    return render_template('course_details.html', course=course, sections=sections, user_role=user_role, section_count=section_count, related_courses=related_courses)
