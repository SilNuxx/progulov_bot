import sqlite3

import config

with sqlite3.connect(config.data["database_file"]) as db:
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Student(
    student_id INTEGER NOT NULL,
    student_name TEXT NOT NULL UNIQUE,
    PRIMARY KEY(student_id AUTOINCREMENT)
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Truancy (
	truancy_date INTEGER NOT NULL,
	student_id INTEGER FOREGIN KEY NOT NULL,
    truancy_count INTEGER NOT NULL,
	truancy_type INTEGER NOT NULL,
	PRIMARY KEY(truancy_date,student_id),
	FOREIGN KEY(student_id) REFERENCES Student(student_id)
    );""")

# Работа со списком студентов
def db_add_student(student_name): # Добавить студента в список
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute(f"""INSERT INTO Student(student_name) VALUES ('{student_name}');""")

def db_del_student(student_id): # Удалить студента из списка
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute(f"""DELETE FROM Student WHERE student_id = {student_id}""")

def db_get_all_sort_student_list(): # Вывести информацию по всем студентам в сортированном по алфавиту виде
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute("""SELECT * FROM Student ORDER BY student_name ASC;""")
        return cur.fetchall()

def db_get_student(student_id): # Вывести информацию по одному из студентов
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT * FROM Student WHERE student_id = {student_id};""")
        return cur.fetchone()

# Работа с учётом прогулов

def db_add_truancy(student_id, number, truancy_type, unixepoch):
    if truancy_type >= 0 and truancy_type < 3: # Отметить прогул
        with sqlite3.connect(config.data["database_file"]) as db:
            cur = db.cursor()

            cur.execute(f"""INSERT INTO Truancy(truancy_date, student_id, truancy_count, truancy_type) VALUES ({unixepoch}, {student_id}, {number}, '{truancy_type}');""")
    else:
        print("Error: truancy_type is out of range")

def db_del_truancy(unixepoch, student_id): # Отменить прогул
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute(f"""DELETE FROM Truancy WHERE truancy_date = {unixepoch} AND student_id = {student_id}""")

def db_change_truancy():
    pass

def db_list_truancy(): # Вывод всех прогулов
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute("""SELECT strftime("%d-%m-%Y", date(truancy_date, 'unixepoch', 'localtime')), Truancy.student_id, student_name, truancy_count, truancy_type FROM Truancy INNER JOIN Student ON Student.student_id = Truancy.student_id""")
        return cur.fetchall()

def db_get_all_truancy_for_month(unixepoch): # Вывод прогулов от начала и до конца указанного месяца
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT strftime("%d-%m-%Y", date(truancy_date, 'unixepoch', 'localtime')), Truancy.student_id, student_name, truancy_count, truancy_type FROM Truancy INNER JOIN Student ON Student.student_id = Truancy.student_id WHERE date(truancy_date, 'unixepoch') BETWEEN date({unixepoch}, 'unixepoch', 'localtime', 'start of month') AND date({unixepoch}, 'unixepoch', 'localtime', 'start of month', '+1 month')""")
        return cur.fetchall()

def console(command): # Для проверки, чтобы не городить миллион ненужных функций
    with sqlite3.connect(config.data["database_file"]) as db:
        cur = db.cursor()
        if "SELECT" in command:
            cur.execute(command)
            return cur.fetchall()
        else:
            cur.execute(command)