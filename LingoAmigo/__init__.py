from flask import Flask
from flask import Blueprint


app = Flask(__name__)

app.secret_key = 'your secret key'

from LingoAmigo import student
from LingoAmigo import teacher
from LingoAmigo import expert
from LingoAmigo import administrator
from LingoAmigo import visitor
from LingoAmigo import register
from LingoAmigo import login

from .student import student
from .teacher import teacher
from .expert import expert
from .administrator import administrator
from .register import register
from .login import login
from .visitor import visitor

app.register_blueprint(visitor)
app.register_blueprint(student, url_prefix="/student", static_folder='static')
app.register_blueprint(teacher, url_prefix="/teacher")
app.register_blueprint(expert, url_prefix="/expert")
app.register_blueprint(administrator, url_prefix="/administrator")
app.register_blueprint(register, url_prefix="/register")
app.register_blueprint(login, url_prefix="/login")