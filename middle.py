import database as db

last_user_massage = ""

# Добавить студента
def add_student(msg):
    student_name = msg.text
    db.db_add_student(student_name.strip())

# Удалить студента
def del_student(msg):
    db.db_del_student(msg.text)

# Вывести список студентов
def get_all_students():
    list_student = db.db_get_all_sort_student_list()

    out_str = "ID | NAME\n\n"
    for i in list_student:
        out_str += f"{i[0]} | {i[1]}\n"

    return out_str

def get_last_user_message(msg):
    last_user_massage = msg.text

def return_user_message():
    return last_user_massage
