from flask import render_template

from animation_studio_app import db, app
from database.models import Projects, Employees


# @app.route('/')
# def show_main_page():
#     con = get_db_connection()
#     with con.cursor() as cursor:
#         cursor.execute("call get_projects_and_supervisors")
#         rows = cursor.fetchall()
#     con.close()
#     return render_template('projects.html', projects=rows)


@app.route('/')
def show_main_page():
    projects = db.session.query(Projects, Employees). \
        join(Employees, Employees.id_employee == Projects.supervisor).all()
    return render_template('projects.html', projects=projects)
