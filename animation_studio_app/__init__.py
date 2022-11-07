from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'i want to sleep'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/animation_studio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
# db.create_all()

