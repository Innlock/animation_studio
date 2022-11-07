from flask_login import UserMixin

from animation_studio_app import db, manager


class Employees(db.Model, UserMixin):
    id_employee = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(20))
    birthday = db.Column(db.DateTime())
    password = db.Column(db.String(20), nullable=False)

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
