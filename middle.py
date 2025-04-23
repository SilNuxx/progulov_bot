import database

# Добавить студента
def add_student(msg):
    database.db_add_student(msg.text)

# Вывести список студентов
def get_all_students():
    list_student = database.db_get_all_sort_student_list()

    out_str = "ID | NAME\n\n"
    for i in list_student:
        out_str += f"{i[0]} | {i[1]}\n"

    return out_str