import sqlite3

database_file = r"database.db"

# Создание БД
with sqlite3.connect(database_file) as db:
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Student(
    student_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    PRIMARY KEY(student_id AUTOINCREMENT)
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Truancy (
	truancy_date INTEGER NOT NULL,
	student_id INTEGER FOREGIN KEY NOT NULL,
    truancy_number INTEGER NOT NULL,
	truancy_type TEXT NOT NULL,
	PRIMARY KEY(truancy_date,student_id),
	FOREIGN KEY(student_id) REFERENCES Student(student_id)
    );""")

# Добавить студента
def db_add_student(student_name):
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute(f"""INSERT INTO Student(student_name) VALUES ('{student_name}');""")

def db_del_student(student_id): # Удалить студента из списка
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute(f"""DELETE FROM Student WHERE student_id = {student_id};""")

# Получить сортированный по именам список студентов
def db_get_all_sort_student_list(): 
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute("""SELECT * FROM Student ORDER BY student_name ASC;""")
        return cur.fetchall()

def db_get_student(student_id): # Вывести информацию по одному из студентов
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT * FROM Student WHERE student_id = {student_id};""")
        return cur.fetchone()

# Работа с учётом прогулов

def db_add_truancy(student_id, number, truancy_type, unixepoch): # Отметить прогул
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute(f"""INSERT INTO Truancy(truancy_date, student_id, truancy_number, truancy_type) VALUES ({unixepoch}, {student_id}, {number}, '{truancy_type}');""")

def db_del_truancy(unixepoch, student_id): # Отменить прогул
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute(f"""DELETE FROM Truancy WHERE truancy_date = {unixepoch} AND student_id = {student_id};""")

def db_list_truancy():
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute("""SELECT date(truancy_date, 'unixepoch', '+3 hours'), Truancy.student_id, student_name, truancy_number, truancy_type FROM Truancy INNER JOIN Student ON Student.student_id = Truancy.student_id;""")
        return cur.fetchall()
