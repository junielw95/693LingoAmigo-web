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
   |    |    |-- admin_eodit_profile.html                      # Admin  edit profile and change password
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
   |    |    |
   |
   |-- requirements.txt                    # Application Dependencies
   |
   |-- run.py                              # Start the app in development and production
   |
   |-- LingoAmigo.sql                    # Database


