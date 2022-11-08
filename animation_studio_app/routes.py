from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from animation_studio_app import db, app, manager
from database.db_connection import get_db_connection
from database.models import Projects, Employees, Files, Teams, ProjectsTeams, TeamsEmployees


@app.route('/')
def show_main_page():
    user_id = get_current_id()
    # тут есть и процедура, и функция
    con = get_db_connection()
    with con.cursor() as cursor:
        cursor.execute("call get_projects_and_supervisors")
        projects = cursor.fetchall()
        for project in projects:
            cursor.execute(f"select count_people_in_project({project['id_project']}) as amount")
            amount_of_people = cursor.fetchone()
            project["amount"] = amount_of_people["amount"]
    print(projects)
    con.close()
    user_logged = user_id is not None
    return render_template('projects.html', projects=projects, user_logged=user_logged)


def get_current_id():
    if current_user.is_authenticated:
        user_id = current_user.id_employee
        return user_id
    return None


# @app.route('/')
# def show_main_page():
#     user_id = get_current_id()
#
#     # # все команды человека
#     # teams = db.session.query(Teams, Employees, TeamsEmployees). \
#     #     join(TeamsEmployees, TeamsEmployees.id_team == Teams.id_team).\
#     #     join(Employees, Employees.id_employee == TeamsEmployees.id_employee
#     #     or Employees.id_employee == Teams.leader).\
#     #     filter(Employees.id_employee == 1).group_by(Teams.id_team, Employees.id_employee).all()
#     # print(teams)
#
#     # # файлы по проекту
#     # files = db.session.query(Files, Employees, Projects).\
#     #     join(Employees, Employees.id_employee == Files.id_employee).\
#     #     join(Projects, Projects.id_project == Files.id_project).\
#     #     filter(Projects.id_project == 1).all()
#     # print(files)
#
#     projects = db.session.query(Projects, Employees). \
#         join(Employees, Employees.id_employee == Projects.supervisor).all()
#
#     user_logged = user_id is not None
#     return render_template('projects.html', projects=projects, user_logged=user_logged)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = Employees.query.filter_by(full_name=login).first()
        if user and user.password == password:  # if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('show_main_page'))
        else:
            flash('Введите корректные логин и пароль')
    else:
        flash('Введите логин и пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            # hash_pwd = generate_password_hash(password)
            # new_user = Employees(full_name=login, password=hash_pwd)
            new_user = Employees(login, password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page' + '?next=' + request.url))
    return response
