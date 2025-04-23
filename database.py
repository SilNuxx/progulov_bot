import sqlite3

database_file = r"database.db"

with sqlite3.connect(database_file) as db:
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Student(
    student_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    PRIMARY KEY(student_id AUTOINCREMENT)
    );""")
    cur.execute("""
    CREATE TABLE Truancy (
	truancy_date INTEGER NOT NULL,
	student_id INTEGER FOREGIN KEY NOT NULL,
    truancy_number INTEGER NOT NULL,
	truancy_type TEXT NOT NULL,
	PRIMARY KEY(truancy_date,student_id),
	FOREIGN KEY(student_id) REFERENCES Student(student_id)
    );""")

# Работа со списком студентов
def db_add_student(student_name): # Добавить студента в список
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute(f"""INSERT INTO Student(student_name) VALUES ('{student_name}');""")

def db_del_student(student_id): # Удалить студента из списка
    pass

def db_get_all_sort_student_list(): # Вывести информацию по всем студентам в сортированном по алфавиту виде
    with sqlite3.connect(database_file) as db:
        cur = db.cursor()

        cur.execute("""SELECT * FROM Student ORDER BY student_name ASC;""")
        return cur.fetchall()

def db_get_student(student_id): # Вывести информацию по одному из студентов
    pass

# Работа с учётом прогулов

def db_add_truancy(student_id, reason, type, unixpoch): # Отметить прогул
    pass

def db_del_truancy(truancy_id): # Отменить прогул
    pass


# '''
# Таблица: Прогулы

# Столбцы: 
# '''

# '''
# Сортировка по алфавиту только при выводе
# '''

# /add 1 1 12.
# command, int(student), int(count), datetime.date(date), args = message.split(" ") 