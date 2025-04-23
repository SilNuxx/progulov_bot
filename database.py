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

# Удалить студента
def db_del_student(student_id): 
    pass

# Получить сортированный по именам список студентов
def db_get_all_sort_student_list(): 
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute("""SELECT * FROM Student ORDER BY student_name ASC;""")
        return cur.fetchall()

# Вывести информацию по одному из студентов
def db_get_student_info(student_id): 
    pass

# Добавить прогул
def db_add_truancy(student_id, reason, type, unixpoch): # Отметить прогул
    pass

# Удалить прогул
def db_del_truancy(truancy_id): # Отменить прогул
    pass
