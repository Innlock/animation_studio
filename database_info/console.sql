create database animation_studio;
use animation_studio;

create table employees
(
    id_employee int(10) AUTO_INCREMENT primary key,
    full_name   varchar(100) NOT NULL,
    telephone   varchar(20),
    email       varchar(50),
    birthday    date,
    password    varchar(20) NOT NULL,
    CHECK (email LIKE '%_@_%._%')
);
create table teams
(
    id_team int(10) AUTO_INCREMENT primary key,
    leader  int NOT NULL,
    name    varchar(100) unique,
    FOREIGN KEY (leader) REFERENCES employees (id_employee) ON UPDATE CASCADE ON DELETE CASCADE
);
create table projects
(
    id_project   int(10) AUTO_INCREMENT primary key,
    name         varchar(100) NOT NULL,
    completeness bool default (false),
    supervisor   int          NOT NULL,
    FOREIGN KEY (supervisor) REFERENCES employees (id_employee) ON UPDATE CASCADE ON DELETE CASCADE
);
create table files
(
    id_file     int(10) AUTO_INCREMENT primary key,
    id_project  int,
    type        enum ('audio','animation','video','picture') default ('picture'),
    name        varchar(100),
    link        varchar(500) NOT NULL,
    version     varchar(35),
    date        date,
    id_employee int,
    FOREIGN KEY (id_project) REFERENCES projects (id_project) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_employee) REFERENCES employees (id_employee) ON UPDATE CASCADE ON DELETE CASCADE
);


create table teams_employees
(
    id_team     int(10),
    id_employee int(10),
    position    varchar(500) NOT NULL,
    FOREIGN KEY (id_team) REFERENCES teams (id_team) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_employee) REFERENCES employees (id_employee) ON UPDATE CASCADE ON DELETE CASCADE,
    primary key (id_team, id_employee)
);
create table projects_teams
(
    id_project int(10),
    id_team    int(10),
    profile    varchar(500) NOT NULL,
    FOREIGN KEY (id_team) REFERENCES teams (id_team) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_project) REFERENCES projects (id_project) ON UPDATE CASCADE ON DELETE CASCADE,
    primary key (id_team, id_project)
);

show databases;
show tables;

describe employees;
describe teams;
describe projects;
describe files;
describe teams_employees;
describe projects_teams;


INSERT INTO employees (full_name, telephone, birthday, password)
VALUES ('Кошелев Даниил Георгиевич', '8005553535', '1976-07-19', '1234'),
       ('Калашников Илья Михайлович', '8023222235', '1978-12-11', '1234'),
       ('Захарова Елена Робертовна', '8003565477', '1988-11-21', '1234');
INSERT INTO employees (full_name, telephone, email, birthday, password)
VALUES ('Мартынов Савва Филиппович', '8003957944', 'zyue8brv@outlook.com', '1986-10-01', '1234'),
       ('Колесникова Виктория Васильевна', '8002568846', 'pxacl@mail.ru', '2000-01-10', '1234'),
       ('Гусев Лев Маркович', '8005666353', 'x@mail.ru', '2000-05-05', '1234'),
       ('Архипов Арсений Матвеевич', '8003457455', 'lrsdy5p@yandex.ru', '1977-10-25', '1234'),
       ('Литвинов Иван Кириллович', '8005435533', 't3i@outlook.com', '1999-09-09', '1234'),
       ('Евсеев Арсений Давидович', '8043243355', 'emhzysf2@yandex.ru', '1986-10-07', '1234'),
       ('Королев Андрей Андреевич', '8007776452', 'f245n@outlook.com', '1986-10-08', '1234'),
       ('Грачев Лев Тимофеевич', '8001233344', 'f@outlook.com', '1995-09-09', '1234'),
       ('Севастьянова Ксения Платоновна', '8003566635', 'wrts90puk@yandex.ru', '1987-10-19', '1234');
INSERT INTO employees (full_name, telephone, email, password)
VALUES ('Денисова Юлия Кирилловна', '8005353535', 'rv7bp@gmail.com', '1234'),
       ('Захарова Сафия Артёмовна', '8005464235', 'jiwaddeiffolou-6402@yopmail.com', '1234'),
       ('Федоров Максим Данилович', '8006613655', 'ThePartyAnimals@domain.com', '1234'),
       ('Артемова Мария Борисовна', '8005456655', 'SillyBilly@domain.com', '1234'),
       ('Васильева Мила Павловна', '8005525655', 'SunnySally@domain.com', '1234'),
       ('Самсонов Матвей Тимофеевич', '8078034655', 'ButterflyLover@domain.com', '1234'),
       ('Троицкий Андрей Фёдорович', '8064243655', 'Foodie4Life@domain.com', '1234'),
       ('Фролов Андрей Леонович', '8008763555', 'BingeWatchingExpert@domain.com', '1234'),
       ('Софронов Даниил Львович', '8004573655', 'LocoLola@domain.com', '1234'),
       ('Демин Фёдор Даниэльевич', '8005513754', 'DizzyDaffodil@domain.com', '1234'),
       ('Симонова Ксения Романовна', '8005517547', 'PetSuppliesCT@domain.com', '1234');
INSERT INTO employees (full_name, password)
VALUES ('Козлова Алиса Ильинична', '1234'),
       ('Антонова Кристина Давидовна', '1234'),
       ('Васильева Виктория Матвеевна', '1234'),
       ('Селиванова Арина Ярославовна', '1234'),
       ('Уткин Арсений Арсентьевич', '1234'),
       ('Гордеева Софья Максимовна', '1234');


INSERT INTO teams (leader, name)
VALUES (1, 'Аниматоры, команда 1'),
       (2, 'Аниматоры, команда 2'),
       (3, 'Анимация - цвет'),
       (3, 'Фоновики'),
       (4, 'Дизайнеры'),
       (6, 'Звуковики'),
       (1, 'Универсальная команда');

INSERT INTO projects (name, supervisor)
VALUES ('Совиный дом', 1),
       ('С приветом по планетам', 5),
       ('Головоломки', 7);
INSERT INTO projects (name, supervisor, completeness)
VALUES ('Самурай Джек', 2, true);

INSERT INTO files (id_project, type, name, link, version, id_employee, date)
VALUES (1, 'animation', 'Сцены 1-3', 'https://bipbap.ru/krasivye-kartinki/krasivye-kartinki-kotov-35-foto.html', 'v1',
        2, '2020-10-01'),
       (1, 'animation', 'Сцены 4-7', 'https://lifeglobe.net/entry/1032', 'v1', 9, '2021-11-29'),
       (1, 'audio', 'Песня концовки', 'https://bigpicture.ru/30-sposobov-ispolzovaniya-kotov-v-xozyajstve/', 'v1', 27,
        '2021-11-23'),
       (1, 'audio', 'Вступительная песня', 'https://tlum.ru/news/19-multfilmov-pro-kotov-i-kosek/', 'v2', 27,
        '2021-11-29'),
       (1, 'picture', 'Сцена 5, фон', 'https://klike.net/1899-koty-krasivye-kartinki-50-foto.html', 'v1', 1,
        '2022-03-17'),
       (2, 'animation', 'Сцена 2, gif',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTU0glfHGZz8fi0vm1OdXwapDHSnVeu7ZpG8HqSMhTd4Q&s', 'v1',
        3, '2022-06-21'),
       (3, 'video', 'Финальный проект', '', 'v1.0', 2, '2022-05-11'),
       (3, 'video', 'Финальный проект', '', 'v1.1', 2, '2022-03-18'),
       (3, 'audio', 'Песня концовки', '', 'v1', 26, '2022-03-17'),
       (4, 'audio', 'Вступительная песня', '', 'v1', 26, '2022-03-17'),
       (4, 'picture', 'Сцена 1', '', 'v1', 20, '2022-03-17'),
       (3, 'picture', 'Сцена 2', '', 'v2', 21, '2019-01-01'),
       (4, 'animation', 'Сцены 4-7', 'https://lifeglobe.net/entry/1032', 'v1', 14, '2021-12-07'),
       (4, 'audio', 'Песня концовки', 'https://bigpicture.ru/30-sposobov-ispolzovaniya-kotov-v-xozyajstve/', 'v1', 28,
        '2020-09-01');
INSERT INTO files (id_project, type, name, link, version, id_employee)
values (4, 'audio', 'Вступительная песня', 'https://tlum.ru/news/19-multfilmov-pro-kotov-i-kosek/', 'v2', 28),
       (4, 'picture', 'Сцена 5, фон', 'https://klike.net/1899-koty-krasivye-kartinki-50-foto.html', 'v1', 23);

INSERT INTO teams_employees (id_team, id_employee, position)
VALUES (1, 8, 'Раскадровщик'),
       (1, 9, 'Раскадровщик'),
       (1, 10, 'Аниматор'),
       (1, 11, 'Аниматор'),
       (1, 12, 'Аниматор'),
       (2, 13, 'Аниматор'),
       (2, 14, 'Аниматор'),
       (2, 15, 'Аниматор'),
       (3, 17, 'Художник по покарсу'),
       (3, 18, 'Художник по покарсу'),
       (3, 19, 'Художник по покарсу'),
       (3, 20, 'Дизайнер'),
       (5, 21, 'Дизайнер'),
       (5, 22, 'Дизайнер'),
       (4, 23, 'Фоновик'),
       (5, 24, 'Дизайнер'),
       (4, 25, 'Фоновик'),
       (5, 26, 'Звуковой директор'),
       (6, 27, 'Звуковой режиссер'),
       (6, 16, 'Музыкант'),
       (6, 28, 'Музыкант'),
       (6, 29, 'Артист'),
       (7, 9, 'Раскадровщик'),
       (7, 10, 'Аниматор'),
       (7, 22, 'Дизайнер'),
       (7, 23, 'Фоновик'),
       (7, 27, 'Звуковой режиссер'),
       (7, 16, 'Музыкант');

INSERT INTO projects_teams (id_project, id_team, profile)
VALUES (1, 1, 'Анимация'),
       (1, 6, 'Звук'),
       (2, 1, 'Анимация'),
       (2, 6, 'Музыка'),
       (3, 5, 'Дизайн'),
       (3, 3, 'Анимация'),
       (4, 4, 'Анимация'),
       (4, 7, 'Постановка и режиссура'),
       (1, 7, 'Звукорежиссура');



SELECT *
FROM employees;
SELECT *
FROM teams;
SELECT *
FROM projects;
SELECT *
FROM files;
SELECT *
FROM teams_employees;
SELECT *
FROM projects_teams;

select id_employee, full_name
from employees
where telephone like '________35';
select *
from projects
where id_project in (1, 2)
  and supervisor != 5
  and completeness = 0;
select *
from employees
where id_employee in (1, 3, 5)
  and (email like 's%' or birthday < '1988-01-01');
select *
from employees
where (id_employee in (1, 3, 5) and email like 's%')
   or birthday < '1988-01-01';
select full_name, birthday
from employees
order by full_name asc, birthday desc;
ALTER TABLE projects
    ADD COLUMN link varchar(500) after name;


select teams.id_team, teams.name, employees.full_name, teams_employees.position
from employees
         inner join teams_employees on employees.id_employee = teams_employees.id_employee
         inner join teams on teams.id_team = teams_employees.id_team;


# proc and funcs
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_projects_and_supervisors`()
BEGIN
    select projects.id_project, projects.name, employees.full_name
    from projects inner join employees on employees.id_employee = projects.supervisor;
END

CREATE
    DEFINER = `root`@`localhost` PROCEDURE `get_files_of_employee`(in id_empl INT)
BEGIN
    select id_file, name from files where id_employee = id_empl;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_people_in_team`(in id_team_in INT)
BEGIN
select teams.id_team, teams.name, employees.full_name, teams_employees.position
from employees
         inner join teams_employees on employees.id_employee = teams_employees.id_employee
         inner join teams on teams.id_team = teams_employees.id_team
where teams.id_team = id_team_in;
END

CREATE
    DEFINER = `root`@`localhost` PROCEDURE `get_projects_of_employee`(in empl_id INT)
BEGIN
    select projects.id_project, projects.name
    from employees
             inner join teams_employees on employees.id_employee = teams_employees.id_employee
             inner join teams on teams.id_team = teams_employees.id_team
             inner join projects_teams on projects_teams.id_team = teams.id_team
             inner join projects on projects.id_project = projects_teams.id_project
    where employees.id_employee = empl_id
       or teams.leader = empl_id
    group by projects.id_project;
END


CREATE DEFINER=`root`@`localhost` FUNCTION `count_people_in_team`(id_team_in INT) RETURNS int
    DETERMINISTIC
BEGIN DECLARE amount INT;
select COUNT(*)
INTO amount
from employees
         inner join teams_employees on employees.id_employee = teams_employees.id_employee
         inner join teams on teams.id_team = teams_employees.id_team
where teams.id_team = id_team_in;
RETURN amount+1;
END

CREATE DEFINER=`root`@`localhost` FUNCTION `count_people_in_project`(id_pr INT) RETURNS int
    DETERMINISTIC
BEGIN DECLARE amount INT;
select SUM(count_people_in_team(id_team)) INTO amount
from projects_teams where id_project=id_pr;
RETURN amount;
END

CREATE
    DEFINER = `root`@`localhost` FUNCTION `count_files_in_time_period`(date_from DATE, date_to DATE) RETURNS int
    DETERMINISTIC
BEGIN
    DECLARE amount INT;
    select COUNT(*)
    INTO amount
    from files
    where date > date_from
      and date < date_to;
    RETURN amount;
END


CREATE DEFINER=`root`@`localhost` TRIGGER `employees_BEFORE_INSERT` BEFORE INSERT ON `employees` FOR EACH ROW BEGIN DECLARE len INT;
DECLARE i INT;
DECLARE charnum INT;
declare SortedName varchar(100);
declare input varchar(100);

SET input = LOWER(new.full_name);
SET len = LENGTH(input);
SET i = 1;
set charnum = 1;
set SortedName = '';

WHILE
    (i <= len)
    DO
        if charnum = 1 then
set SortedName = concat(SortedName, upper(mid(input, i, 1)));
set charnum = charnum + 1;
else
            if mid(input,i,1) = ' ' then
set SortedName = concat(SortedName, ' ');
set charnum = 1;
else
set SortedName = concat(SortedName, mid(input, i, 1));
set charnum = charnum + 1;
end if;
end if;
SET i = i + 1;
END WHILE;
SET new.full_name = SortedName;
END


CREATE DEFINER=`root`@`localhost` TRIGGER `files_BEFORE_INSERT` BEFORE INSERT ON `files` FOR EACH ROW BEGIN
    if new.date is null then
        SET new.date=current_date();
    end if;
END