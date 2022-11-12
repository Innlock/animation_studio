from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.secret_key = 'i want to sleep'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/animation_studio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = '.\\files'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'txt', 'jpeg', 'mp4'}

# db.create_all()

