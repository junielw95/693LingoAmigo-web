from LingoAmigo import app
from .database import get_cursor
from LingoAmigo import Blueprint
from flask import Blueprint, render_template, request, g, session
from math import ceil
from decimal import Decimal, InvalidOperation

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
                            t.image_url AS teacher_image, t.teacher_id, c.discount_details
                    FROM Course c
                    JOIN Teacher t ON c.creator_id = t.teacher_id
                    JOIN Language l ON c.language_id = l.language_id 
                    WHERE c.status = 'Active'
                    LIMIT 8
                    '''
    if language_filter:
        course_query += " WHERE l.language_id = %s"
        cursor.execute(course_query, (language_filter,))
    else:
        cursor.execute(course_query)
    course_list = cursor.fetchall()
    
    # calculate the discounted price
    
    courses_with_discounts = []
    for course in course_list:
        
        try:
            if course[12] and course[12] != 'None':
                discount_rate = Decimal(course[12].rstrip('%')) / 100
                discount_price = course[4] * (1 - discount_rate)
            else:
                discount_price = course[4]

        except InvalidOperation:
            discount_price = course[4]
        courses_with_discounts.append(course + (discount_price,))
            
    
    current_language = None
    if language_filter and course_list:
        current_language = course_list[0][8]
    
    news_query = '''
                    SELECT r.resource_id, r.topic, r.content, r.published_date, r.image_url,
                    COALESCE(e.first_name, a.first_name) AS first_name,
                    COALESCE(e.last_name, a.last_name) AS last_name,
                    r.creator_id
                    FROM Resource r
                    LEFT JOIN Expert e ON r.creator_id = e.expert_id
                    LEFT JOIN Administrator a ON r.creator_id = a.admin_id
                    WHERE r.type = 'Article'
                    ORDER BY r.published_date DESC
                    LIMIT 3
                    '''
    cursor.execute(news_query)
    news_items = cursor.fetchall()

    cursor.close()  
    connection.close() 

    return render_template('index.html', teachers=teachers, course_list=courses_with_discounts, current_language=current_language, news_items=news_items)


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
        cursor.execute("SELECT * FROM Teacher WHERE first_name LIKE %s OR last_name LIKE %s OR nationality LIKE %s AND status = 'Active'", (search_query, search_query, search_query))
    else:
        cursor.execute("SELECT * FROM Teacher WHERE status = 'Active'")


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


@app.context_processor
def courselist():
    if not hasattr(g, 'courselist'):

        cursor, connection = get_cursor() 
        cursor.execute('SELECT * FROM Course WHERE status = %s', ('Active',))
        g.courselist = cursor.fetchall()

        cursor.close()  
        connection.close() 
    

    return dict(courselist=g.courselist)


@app.context_processor
def experts():
    if not hasattr(g, 'experts'):

        cursor, connection = get_cursor() 
        cursor.execute('SELECT * FROM Expert')
        g.experts = cursor.fetchall()

        cursor.close()  
        connection.close() 
    

    return dict(experts=g.experts)

@app.route('/courses')
def courses():
    cursor, connection = get_cursor() 
    language_filter = request.args.get('language_id')
   

    page = request.args.get('page', 1, type=int)
    per_page = 30
    offset = (page - 1) * per_page

    

    base_query = '''
                FROM Course c
                JOIN Teacher t ON c.creator_id = t.teacher_id
                JOIN Language l ON c.language_id = l.language_id
                WHERE c.status = 'Active'
                '''
    where_clause = []
    query_params = []
    

    # Apply language filter
    if language_filter:
        where_clause.append("l.language_id = %s")
        query_params.append(language_filter)

    # Construct the complete sql for counting filtered results
    count_query = f"SELECT COUNT(*) {base_query}"
    if where_clause:
        count_query += " AND " + " AND ".join(where_clause)

    # Execute the count query
    cursor.execute(count_query, query_params)
    total_courses = cursor.fetchone()[0]
    total_pages = ceil(total_courses / per_page)
    
    #Fetch all courses
    course_query = f'''
                    SELECT c.course_id, c.course_name, c.description, c.duration, c.price, c.image_url, c.status,
                            CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
                            l.language_name, l.language_id,
                            t.image_url AS teacher_image, t.teacher_id,
                            c.discount_details
                    {base_query}
                    '''
    if where_clause:
        course_query += " AND " + " AND ".join(where_clause) 
    course_query += " ORDER BY c.course_id LIMIT %s OFFSET %s"
    query_params.extend([per_page, offset])

    # Execute course query
    cursor.execute(course_query, query_params)
    course_list = cursor.fetchall()

    # Fetch current language name
    current_language = None
    if language_filter:
        cursor.execute("SELECT language_name FROM Language WHERE language_id = %s", (language_filter,))
        current_language = cursor.fetchone()[0]

    # calculate the discounted price
    
    courses_with_discounts = []
    for course in course_list:
        
        try:
            if course[12] and course[12] != 'None':
                discount_rate = Decimal(course[12].rstrip('%')) / 100
                discount_price = course[4] * (1 - discount_rate)
            else:
                discount_price = course[4]

        except InvalidOperation:
            discount_price = course[4]
        courses_with_discounts.append(course + (discount_price,))
            
    
    cursor.close()  
    connection.close() 

    return render_template('courses.html', course_list=courses_with_discounts, language_filter=language_filter, current_language=current_language, total_pages=total_pages, current_page=page)


@app.route('/course_details/<int:course_id>')
def course_details(course_id):
    cursor, connection = get_cursor()
    user_role = session.get('role', None)
    user_id = session.get('id', None)

    #Check the student purchase the course
    purchase_check_query = '''
                            SELECT *
                            FROM `Order`
                            WHERE user_id = %s AND course_id = %s AND status = 'Completed'
                            '''
    cursor.execute(purchase_check_query, (user_id, course_id))
    user_has_access = cursor.fetchone() is not None
    #Fetch all courses
    course_query = '''
                    SELECT c.course_id, c.course_name, c.description, c.duration, c.price, c.image_url, c.status,
                            CONCAT(t.first_name, ' ', t.last_name) AS teacher_name, t.image_url AS teacher_image,
                            l.language_name, l.language_id,
                            t.teacher_id, c.creator_id, c.discount_details
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
                    SELECT s.title, s.content, v.video_id
                    FROM Section s
                    JOIN Video v ON s.section_id = v.section_id
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

    #Fetch quiz for course
    quiz_query = '''
                SELECT quiz_id FROM Quiz WHERE course_id = %s
                '''
    cursor.execute(quiz_query, (course_id,))
    quiz = cursor.fetchone()
    quiz_id = quiz[0] if quiz else None
    related_courses = '''
                        SELECT course_id, course_name, price, image_url, status, discount_details
                        FROM Course
                        WHERE language_id = %s AND course_id !=%s AND status = 'Active'
                        ORDER BY RAND()
                        LIMIT 8
                    '''
    cursor.execute(related_courses, (course[10], course_id))
    related_courses = cursor.fetchall()

    
    # calculate the discounted price
    
    try:
        if course[13] and course[13] != 'None':
            discount_rate = Decimal(course[13].rstrip('%')) / 100
            discount_price = course[4] * (1 - discount_rate)
        else:
            discount_price = course[4]

    except InvalidOperation:
        discount_price = course[4]

    course = course + (discount_price,)

    # calculate the discounted price for related course
    related_courses_with_discount = []
    for rc in related_courses:
        try:
            if rc[5] and rc[5] != 'None':
                discount_rate = Decimal(rc[5].rstrip('%')) / 100
                discount_price = rc[2] * (1 - discount_rate)
            else:
                discount_price = rc[2]

        except InvalidOperation:
            discount_price = rc[2]

    related_courses_with_discount.append(rc + (discount_price,))
        
    cursor.close()  
    connection.close() 
    return render_template('course_details.html', course=course, sections=sections, user_role=user_role, section_count=section_count, related_courses=related_courses_with_discount, user_has_access=user_has_access, course_id=course_id, quiz_id=quiz_id)

@app.route('/news')
def news():
    cursor, connection = get_cursor()
    try:
        news_query = '''
                    SELECT r.resource_id, r.topic, r.content, r.published_date, r.image_url,
                    COALESCE(e.first_name, a.first_name) AS first_name,
                    COALESCE(e.last_name, a.last_name) AS last_name,
                    r.creator_id
                    FROM Resource r
                    LEFT JOIN Expert e ON r.creator_id = e.expert_id
                    LEFT JOIN Administrator a ON r.creator_id = a.admin_id
                    WHERE r.type = 'News'
                    ORDER BY r.published_date DESC
                    '''
        cursor.execute(news_query)
        news_items = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    
    return render_template('news.html', news_items=news_items)

@app.route('/Research')
def research():
    cursor, connection = get_cursor()
    try:
        news_query = '''
                    SELECT r.resource_id, r.topic, r.content, r.published_date, r.image_url,
                    COALESCE(e.first_name, a.first_name) AS first_name,
                    COALESCE(e.last_name, a.last_name) AS last_name,
                    r.creator_id
                    FROM Resource r
                    LEFT JOIN Expert e ON r.creator_id = e.expert_id
                    LEFT JOIN Administrator a ON r.creator_id = a.admin_id
                    WHERE r.type = 'Research'
                    ORDER BY r.published_date DESC
                    '''
        cursor.execute(news_query)
        news_items = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    
    return render_template('research.html', news_items=news_items)


@app.route('/Article')
def article():
    cursor, connection = get_cursor()
    try:
        news_query = '''
                    SELECT r.resource_id, r.topic, r.content, r.published_date, r.image_url,
                    COALESCE(e.first_name, a.first_name) AS first_name,
                    COALESCE(e.last_name, a.last_name) AS last_name,
                    r.creator_id
                    FROM Resource r
                    LEFT JOIN Expert e ON r.creator_id = e.expert_id
                    LEFT JOIN Administrator a ON r.creator_id = a.admin_id
                    WHERE r.type = 'Article'
                    ORDER BY r.published_date DESC
                    '''
        cursor.execute(news_query)
        news_items = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    
    return render_template('article.html', news_items=news_items)


@app.route('/tutorial')
def tutorial():
    cursor, connection = get_cursor()
    try:
        news_query = '''
                    SELECT r.resource_id, r.topic, r.content, r.published_date, r.image_url,
                    COALESCE(e.first_name, a.first_name) AS first_name,
                    COALESCE(e.last_name, a.last_name) AS last_name,
                    r.creator_id
                    FROM Resource r
                    LEFT JOIN Expert e ON r.creator_id = e.expert_id
                    LEFT JOIN Administrator a ON r.creator_id = a.admin_id
                    WHERE r.type = 'Tutorial'
                    ORDER BY r.published_date DESC
                    '''
        cursor.execute(news_query)
        news_items = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    
    return render_template('tutorial.html', news_items=news_items)


@app.route('/resource_details/<int:resource_id>')
def resource_details(resource_id):
    cursor, connection = get_cursor()
    try:
        news_query = '''
                    SELECT r.resource_id, r.topic, r.content, r.published_date, r.image_url,
                    COALESCE(e.first_name, a.first_name) AS first_name,
                    COALESCE(e.last_name, a.last_name) AS last_name,
                    r.creator_id, r.details
                    FROM Resource r
                    LEFT JOIN Expert e ON r.creator_id = e.expert_id
                    LEFT JOIN Administrator a ON r.creator_id = a.admin_id
                    WHERE r.resource_id = %s 
                    '''
        cursor.execute(news_query, (resource_id,))
        news_items = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    
    return render_template('resource_details.html', news_items=news_items)