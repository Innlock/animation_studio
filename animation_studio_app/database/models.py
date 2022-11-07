import enum
from flask_login import UserMixin

from animation_studio_app import db, manager


class Employees(db.Model, UserMixin):
    id_employee = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(20))
    birthday = db.Column(db.DateTime())
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Employee {self.full_name}>'

    def __init__(self, login, password):
        self.full_name = login
        self.password = password

    def get_id(self):
        return self.id_employee

    def get_login(self):
        return self.full_name


@manager.user_loader
def load_user(user_id):
    return Employees.query.get(user_id)


class Projects(db.Model):
    id_project = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completeness = db.Column(db.Boolean)
    supervisor = db.Column(db.Integer, db.ForeignKey("employees.id_employee"), nullable=False)
    employees = db.relationship('Employees', backref=db.backref('projects', lazy=True))

    def __repr__(self):
        return f'<Project {self.name}>'


class TeamsEmployees(db.Model):
    id_team = db.Column(db.Integer, db.ForeignKey("teams.id_team"), nullable=False, primary_key=True)
    id_employee = db.Column(db.Integer, db.ForeignKey("employees.id_employee"), nullable=False, primary_key=True)
    position = db.Column(db.String(500), nullable=False)


class ProjectsTeams(db.Model):
    id_project = db.Column(db.Integer, db.ForeignKey("projects.id_project"), nullable=False, primary_key=True)
    id_team = db.Column(db.Integer, db.ForeignKey("teams.id_team"), nullable=False, primary_key=True)
    profile = db.Column(db.String(500), nullable=False)


class Teams(db.Model):
    id_team = db.Column(db.Integer, primary_key=True)
    leader = db.Column(db.Integer, db.ForeignKey("employees.id_employee"), nullable=False)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'<Team {self.name}>'


class FileType(enum.Enum):
    audio = 1
    animation = 2
    video = 3
    picture = 4


class Files(db.Model):
    id_file = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer, db.ForeignKey("projects.id_project"))
    type = db.Column(db.Enum(FileType))
    name = db.Column(db.String(100))
    link = db.Column(db.String(500), nullable=False)
    version = db.Column(db.String(35))
    date = db.Column(db.DateTime())
    id_employee = db.Column(db.Integer, db.ForeignKey("employees.id_employee"))

    def __repr__(self):
        return f'<File {self.name}>'
