from collections import namedtuple
import pymysql
from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy

from db_connection import get_db_connection

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/animation_studio'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
#
# class Employees(db.Model):
#     id_employee = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     telephone = db.Column(db.String(20))
#     email = db.Column(db.String(20))
#     birthday = db.Column(db.DateTime())
#
#
# class Projects(db.Model):
#     id_project = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     completeness = db.Column(db.Boolean)
#     supervisor = db.Column(db.Integer, db.ForeignKey("employees.id_employee"), nullable=False)
#     employees = db.relationship('Employees', backref=db.backref('projects', lazy=True))


# db.create_all()


@app.route('/')
def index():
    con = get_db_connection()
    with con.cursor() as cursor:
        cursor.execute("call get_projects_and_supervisors")
        rows = cursor.fetchall()
    con.close()
    return render_template('projects.html', projects=rows)


if __name__ == "__main__":
    app.run()
