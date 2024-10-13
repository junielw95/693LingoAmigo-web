< LingoAmigo > -- Wenjing Wang 1157756
   |
   |-- app/
   |    |
   |    | -- _init__.py                     # bundle all above sections and expose the Flask APP  
   |    | -- administrator.py               # for administrator functionalities
   |    | -- connect.py                     # manage database connections and configurations
   |    | -- database.py                    #  database operayions, models and schema definitions
   |    | -- expert.py                      # for expert features
   |    | -- login.py                       # login
   |    | -- register.py                    # registration
   |    | -- student.py                     # for student functionalities
   |    | -- teacher.py                     # for teacher functionalities
   |    | -- visitor.py                     # for visitor functionalities
   |    |
   |    |-- static/
   |    |    |-- <css, js, images, fonts, course, picture, uploads, resources, videos>         # CSS files, Javascripts files and pictures
   |    |
   |    |-- templates/
   |    |    |
   |    |    |-- index.html                      # The home page
   |    |    |accounts:
   |    |    |-- login.html                      # Login page
   |    |    |-- register.html                   # Register page
   |    |    |layout:
   |    |    |-- layout.html                      # Layout for all pages, navigation, footer
   |    |    |dashboard:
   |    |    |-- student_dashboard.html                      # Student dashboard
   |    |    |-- student_edit_profile.html                      # Student edit profile and change password
   |    |    |-- teacher_dashboard.html                      # Teacher dashboard
   |    |    |-- teacher_edit_profile.html                      # Teacher edit profile and change password
   |    |    |-- expert_dashboard.html                      # Expert dashboard
   |    |    |-- expert_edit_profile.html                      # Expert edit profile and change password
   |    |    |-- admin_dashboard.html                      # Admin dashboard
   |    |    |-- admin_edit_profile.html                      # Admin  edit profile and change password
   |    |    |visitor pages:
   |    |    |-- about.html                      # Page for the LingoAmigo information
   |    |    |-- contact.html                      # Page for contact details of LingoAmigo
   |    |    |-- courses.html                      # Show all courses
   |    |    |-- courses_details.html                      # Show the selected course details
   |    |    |-- expert_list_profile.html                      # Show expert profile
   |    |    |-- news.html                      # News of the LingoAmigo
   |    |    |-- article.html                      # Articles about language learning
   |    |    |-- research.html                      # Researches about language learning
   |    |    |-- tutorial.html                      # Tutorials about language learning
   |    |    |-- resource_details.html                      # Details of selected resource
   |    |    |-- teachers_list.html                      # Show all teachers
   |    |    |-- teachers_list_profile.html                      # Show the selected teacher profile
   |    |    |student pages:
   |    |    |-- shopping_cart.html                      # Student add courses to the shopping cart
   |    |    |-- course_checkout.html                      # Student checkout selected cources and make a payment
   |    |    |-- student_courses.html                      # Show the student's courses that are paid
   |    |    |-- video.html                      # Student watch course video
   |    |    |-- quiz.html                        # Student complete quiz
   |    |    |-- discussion_board.html         # Student submit posts to ask questions or discuss with others
   |    |    |-- post_details.html             # Student can view post content. All users can reply posts
   |    |    |-- student_session.html             # Student choose a expert, and start session with the expert
   |    |    |-- apply_for_teacher.html          # Student can apply to become a teacher
   |    |    |-- 
   |    |    |Teacher pages:
   |    |    |-- teacher_courses.html          # Teacher view their own courses
   |    |    |-- teacher_create_course.html    # Teacher upload new courses
   |    |    |-- student_edit_course.html      # Teacher edit their own courses
   |    |    |-- teacher_view_students.html    # Teacher view students who subscribe the course
   |    |    |Expert pages:
   |    |    |-- add_resource.html             # Expert create new resources including news, articles, tutorials and researches
   |    |    |Admin pages:
   |    |    |-- admin_all_courses.html          # Admin manage all courses
   |    |    |-- admin_all_language.html         # Admin manage all language
   |    |    |-- admin_all_students.html         # Admin manage all students
   |    |    |-- admin_all_teachers.html         # Admin manage all teachers
   |    |    |-- admin_all_experts.html         # Admin manage all experts
   |    |    |-- admin_edit_student.html        # Admin edit student profile
   |    |    |-- admin_edit_teachers.html         # Admin edit teacher profile
   |    |    |-- admin_edit_experts.html         # Admin edit expert profile
   |    |    |-- view_report.html           # Admin see the sales and revenue of courses
   |    |    |-- 
   |    |    |-- 
   |    |    |-- 
   |
   |-- requirements.txt                    # Application Dependencies
   |
   |-- run.py                              # Start the app in development and production
   |
   |-- LingoAmigo.sql                    # Database



Web App Log-in details
Student
Username: student1; Password: NewPassword1!
Username: student2; Password: NewPassword1!
Username: student3; Password: NewPassword1!
Username: student4; Password: NewPassword1!
Username: student5; Password: NewPassword1!
Username: student6; Password: NewPassword1!
Username: student7; Password: NewPassword1!
Username: student8; Password: NewPassword1!
Username: student9; Password: NewPassword1!
Username: student10; Password: NewPassword1!
Username: student11; Password: NewPassword1!
Username: student12; Password: NewPassword1!
Username: student13; Password: NewPassword1!
Username: student14; Password: NewPassword1!
Username: student15; Password: NewPassword1!
Teacher
Username: teacher1; Password: NewPassword1!
Username: teacher2; Password: NewPassword1!
Username: teacher3; Password: NewPassword1!
Username: teacher4; Password: NewPassword1!
Username: teacher5; Password: NewPassword1!
Username: teacher6; Password: NewPassword1!
Username: teacher7; Password: NewPassword1!
Expert
Username: expert1; Password: NewPassword1!
Username: expert2; Password: NewPassword1!
Username: expert3; Password: NewPassword1!
Administrator
Username: admin1; Password: NewPassword1!
Username: admin2; Password: NewPassword1!

