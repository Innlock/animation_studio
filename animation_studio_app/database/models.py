from animation_studio_app import db


class Employees(db.Model):
    id_employee = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(20))
    birthday = db.Column(db.DateTime())


class Projects(db.Model):
    id_project = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completeness = db.Column(db.Boolean)
    supervisor = db.Column(db.Integer, db.ForeignKey("employees.id_employee"), nullable=False)
    employees = db.relationship('Employees', backref=db.backref('projects', lazy=True))

    def __repr__(self):
        return f'<Project {self.name}>'
