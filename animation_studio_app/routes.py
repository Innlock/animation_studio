import os.path

from flask import render_template, request, redirect, flash, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import update, and_, or_
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from animation_studio_app import db, app, manager, ALLOWED_EXTENSIONS
from database.db_connection import get_db_connection
from database.models import Projects, Employees, Files, Teams, ProjectsTeams, TeamsEmployees


def get_current_id():
    if current_user.is_authenticated:
        user_id = current_user.id_employee
        return user_id
    return None


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


def query_with_filters(args):
    pr, team, empl = args
    i = 0
    while i < len(args):
        if args[i] == 'Не выбрано':
            args.pop(i)
        else:
            i += 1
    print(pr, team, empl)
    files = db.session.query(Files, Projects, Employees, ProjectsTeams). \
        join(Projects, Projects.id_project == Files.id_project). \
        join(Employees, Employees.id_employee == Files.id_employee). \
        join(ProjectsTeams, Files.id_project == ProjectsTeams.id_project)

    match len(args):
        case 3:
            selected_files = files.filter(and_(
                Employees.full_name == empl, Projects.name == pr,
                ProjectsTeams.id_team == team.split(' ')[0])). \
                group_by(Files.id_file).all()
        case 2:
            if pr == 'Не выбрано':
                selected_files = files.filter(and_(
                    Employees.full_name == empl, ProjectsTeams.id_team == team.split(' ')[0])). \
                    group_by(Files.id_file).all()
            elif team == 'Не выбрано':
                selected_files = files.filter(and_(
                    Employees.full_name == empl, Projects.name == pr)). \
                    group_by(Files.id_file).all()
                print(selected_files)
            elif empl == 'Не выбрано':
                selected_files = files.filter(and_(
                    Projects.name == pr, ProjectsTeams.id_team == team.split(' ')[0])). \
                    group_by(Files.id_file).all()
        case 1:
            if pr != 'Не выбрано':
                selected_files = files.filter(
                    Projects.name == pr). \
                    group_by(Files.id_file).all()
            elif team != 'Не выбрано':
                selected_files = files.filter(
                    ProjectsTeams.id_team == team.split(' ')[0]). \
                    group_by(Files.id_file).all()
            elif empl != 'Не выбрано':
                selected_files = files.filter(
                    Employees.full_name == empl). \
                    group_by(Files.id_file).all()
        case _:
            selected_files = ''
    return selected_files


@app.route('/files', methods=['GET', 'POST'])
def search_for_file():
    user_id = get_current_id()
    user_logged = user_id is not None
    files = db.session.query(Files, Projects, Employees, ProjectsTeams). \
        join(Projects, Projects.id_project == Files.id_project). \
        join(Employees, Employees.id_employee == Files.id_employee).all()
    projects = db.session.query(Projects).all()
    teams = db.session.query(Teams).all()
    employees = db.session.query(Employees).all()

    if request.method == 'POST':
        pr = request.form.get('project')
        team = request.form.get('team')
        empl = request.form.get('employee')
        if pr == team == empl == 'Не выбрано':
            flash('Выберите фильтры поиска')
        else:
            selected_files = query_with_filters([pr, team, empl])
            return render_template('files.html', files=selected_files,
                                   employees=employees, teams=teams,
                                   projects=projects, user_logged=user_logged)
    return render_template('files.html', files=files,
                           employees=employees, teams=teams,
                           projects=projects, user_logged=user_logged)


@app.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    user_id = get_current_id()
    user_logged = user_id is not None
    employees = db.session.query(Employees).filter(Employees.id_employee != user_id).all()
    current_user_info = db.session.query(Employees).filter(Employees.id_employee == user_id).one()
    if request.method == 'POST':
        form_employees = request.form.getlist('employee')
        name = request.form.get('name')
        if not name:
            flash('Введите название команды')
        else:
            new_team = Teams()
            new_team.name = name
            new_team.leader = user_id
            db.session.add(new_team)
            db.session.commit()
            new_team_id = db.session.query(Teams).filter(Teams.name == name).first().id_team
            for empl in form_employees:
                new_team_employee = TeamsEmployees()
                new_team_employee.id_team = new_team_id
                new_team_employee.id_employee = db.session.query(Employees). \
                    filter(Employees.full_name == empl).first().id_employee
                new_team_employee.position = "-"
                db.session.add(new_team_employee)
            db.session.commit()
            return redirect("/user_page")
    return render_template('create_team.html', user_logged=user_logged, employees=employees, user=current_user_info)


@app.route('/team/<int:id_team>', methods=['GET', 'POST'])
@login_required
def show_team(id_team):
    user_id = get_current_id()
    user_logged = user_id is not None
    employees = db.session.query(Employees).filter(Employees.id_employee != user_id).all()
    current_user_info = db.session.query(Employees).filter(Employees.id_employee == user_id).one()
    team = db.session.query(Teams, Employees, TeamsEmployees). \
        join(TeamsEmployees, TeamsEmployees.id_team == Teams.id_team). \
        join(Employees,
             (Employees.id_employee == Teams.leader) | (Employees.id_employee == TeamsEmployees.id_employee)). \
        filter(Teams.id_team == id_team).group_by(Teams.id_team, Employees.id_employee).all()
    return render_template('team.html', user_logged=user_logged, employees=employees, user=current_user_info, team=team)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_info(new_file, name, user_id, filename):
    new_file.name = name
    new_file.id_employee = user_id
    new_file.id_project = db.session.query(Projects). \
        filter(Projects.name == request.form.get('project')).one().id_project
    new_file.date = request.form.get('date')
    new_file.link = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    new_file.version = request.form.get('version')
    new_file.type = request.form.get('type')
    if not new_file.date:
        new_file.date = None
    return new_file


@app.route('/create_file', methods=['GET', 'POST'])
@login_required
def create_file():
    user_id = get_current_id()
    user_logged = user_id is not None
    projects = db.session.query(Projects).all()
    files_amount = db.session.query(Files.id_file).order_by(Files.id_file.desc()).first().id_file
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Невозможно прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Выберите файл для загрузки')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            filename = str(files_amount + 1) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            name = request.form.get('name')
            if not name:
                flash('введите имя')
            else:
                new_file = get_file_info(Files(), name, user_id, filename)
                db.session.add(new_file)
                db.session.commit()
                return redirect("/user_page")
    return render_template('create_file.html', user_logged=user_logged, projects=projects)


@app.route('/uploads/<name>')
@login_required
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
        button = request.form.get('button')
        if button == 'Удалить файл':
            db.session.delete(file)
            db.session.commit()
            if os.path.exists(file.link):
                os.remove(file.link)
            return redirect('/user_page')
        elif button == 'Обновить файл':
            if user_id != file.id_employee:
                flash('Вы не можете редактировать чужой файл')
            else:
                downloaded_file = request.files['file']
                if downloaded_file.filename == '':
                    filename = file.link.split('\\')[2]
                elif allowed_file(downloaded_file.filename):
                    filename = str(file.id_file) + "_" + secure_filename(downloaded_file.filename)
                    downloaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    os.remove(file.link)
                name = request.form.get('name')
                if not name:
                    flash('введите имя')
                else:
                    file.id_file = id_file
                    file = get_file_info(file, name, user_id, filename)
                    db.session.commit()
    return render_template('file.html', user_logged=user_logged, file=file, projects=projects)


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

    # все проекты и файлы этого человека внутри команды - projects1
    teams_ids = []
    for t in teams:
        teams_ids.append(str(t['Teams'].id_team))

    projects = db.session.query(Projects, ProjectsTeams, Files). \
        join(ProjectsTeams, Projects.id_project == ProjectsTeams.id_project). \
        filter(ProjectsTeams.id_team.in_(teams_ids)). \
        join(Files, Files.id_project == Projects.id_project). \
        filter(Files.id_employee == user_id).all()

    # все проекты и файлы этого человека - files
    files = db.session.query(Files, Projects). \
        join(Projects, Projects.id_project == Files.id_project). \
        filter(Files.id_employee == user_id).group_by(Files.id_file).all()

    return render_template('user_page.html', user_logged=user_logged,
                           teams=teams, projects1=projects, files=files)


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
    if request.method == 'POST':
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
    if request.method == 'POST':
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
                return redirect("/login")
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
