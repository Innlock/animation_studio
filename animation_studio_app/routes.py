from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from animation_studio_app import db, app, manager
from database.models import Projects, Employees, Files, Teams, ProjectsTeams, TeamsEmployees


# @app.route('/')
# def show_main_page():
#     con = get_db_connection()
#     with con.cursor() as cursor:
#         cursor.execute("call get_projects_and_supervisors")
#         rows = cursor.fetchall()
#     con.close()
#     return render_template('projects.html', projects=rows)

# @manager.user_loader
# def load_user(user_id):
#     try:
#         return Employees.query.get(user_id)
#     except Exception:
#         return None


@app.route('/')
def show_main_page():
    # # id человека
    # if current_user.is_authenticated:
    #     id = current_user.id_employee
    #     print(id)

    # # все команды человека
    # teams = db.session.query(Teams, Employees, TeamsEmployees). \
    #     join(TeamsEmployees, TeamsEmployees.id_team == Teams.id_team).\
    #     join(Employees, Employees.id_employee == TeamsEmployees.id_employee
    #     or Employees.id_employee == Teams.leader).\
    #     filter(Employees.id_employee == 1).group_by(Teams.id_team, Employees.id_employee).all()
    # print(teams)

    # # файлы по проекту
    # files = db.session.query(Files, Employees, Projects).\
    #     join(Employees, Employees.id_employee == Files.id_employee).\
    #     join(Projects, Projects.id_project == Files.id_project).\
    #     filter(Projects.id_project == 1).all()
    # print(files)

    projects = db.session.query(Projects, Employees). \
        join(Employees, Employees.id_employee == Projects.supervisor).all()
    return render_template('projects.html', projects=projects)


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
    return redirect(url_for('show_main_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page' + '?next=' + request.url))
    return response
