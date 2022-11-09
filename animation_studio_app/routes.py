import os.path

from flask import render_template, request, redirect, flash, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from animation_studio_app import db, app, manager, ALLOWED_EXTENSIONS
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
    con.close()
    user_logged = user_id is not None
    return render_template('projects.html', projects=projects, user_logged=user_logged)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create_file', methods=['GET', 'POST'])
@login_required
def create_file():
    user_id = get_current_id()
    user_logged = user_id is not None
    projects = db.session.query(Projects).all()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Невозможно прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Выберите файл для загрузки')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            name = request.form.get('name')
            if not name:
                flash('введите имя')
            else:
                new_file = Files()
                new_file.name = name
                new_file.id_employee = user_id
                new_file.id_project = db.session.query(Projects).\
                    filter(Projects.name == request.form.get('project')).one().id_project
                new_file.date = request.form.get('date')
                new_file.link = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                new_file.version = request.form.get('version')
                new_file.type = request.form.get('type')
                if not new_file.date:
                    new_file.date = None
                db.session.add(new_file)
                db.session.commit()

    return render_template('create_file.html', user_logged=user_logged, projects=projects)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/file/<int:id_file>', methods=['GET', 'POST'])
@login_required
def show_file(id_file):
    projects = db.session.query(Projects).all()
    user_id = get_current_id()
    user_logged = user_id is not None
    file = db.session.query(Files).filter(Files.id_file == id_file).one()
    if request.method == 'POST':
        if file:
            db.session.delete(file)
            db.session.commit()
            return redirect('/user_page')
    return render_template('file.html', user_logged=user_logged, file=file, projects=projects)


def get_current_id():
    if current_user.is_authenticated:
        user_id = current_user.id_employee
        return user_id
    return None


@app.route('/user_page', methods=['GET', 'POST'])
@login_required
def show_user_page():
    user_id = get_current_id()
    user_logged = user_id is not None

    # все команды человека
    teams = db.session.query(Teams, Employees, TeamsEmployees). \
        join(TeamsEmployees, TeamsEmployees.id_team == Teams.id_team). \
        join(Employees, (Employees.id_employee == TeamsEmployees.id_employee) |
             (Employees.id_employee == Teams.leader)). \
        filter(Employees.id_employee == user_id).group_by(Employees.id_employee, Teams.id_team).all()

    # все проекты и файлы этого человека внутри команды - projects1 и без - files
    teams_ids = []
    for t in teams:
        teams_ids.append(str(t['Teams'].id_team))

    projects1 = db.session.query(Projects, ProjectsTeams, Files). \
        join(ProjectsTeams, Projects.id_project == ProjectsTeams.id_project). \
        filter(ProjectsTeams.id_team.in_(teams_ids)). \
        join(Files, Files.id_project == Projects.id_project). \
        filter(Files.id_employee == user_id).all()

    files = db.session.query(Files, Projects).\
        join(Projects, Projects.id_project == Files.id_project).\
        filter(Files.id_employee == user_id).group_by(Files.id_file).all()

    return render_template('user_page.html', user_logged=user_logged,
                           teams=teams, projects1=projects1, files=files)


# @app.route('/')
# def show_main_page():
#     user_id = get_current_id()
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
def show_login_page():
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
