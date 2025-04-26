import database as db
from datetime import datetime, timezone, timedelta

# Вывести список студентов
def student_list():
    list_student = db.db_get_all_sort_student_list()

    out_str = f"```\n{"ID":^2}¦ИМЯ\n"
    for i in list_student:
        out_str += f"{i[0]:^2}¦{i[1]}\n"
    out_str += "```"
    return out_str

# Получить информацию о студенте
def student_info(student_id):
    student_info = db.db_get_student(student_id)
    out_str = f"ID: {student_info[0]}\nИМЯ: {student_info[1]}"
    return out_str

# Добавить студента
def student_add(student_name):
    db.db_add_student(student_name)

# Удалить студента
def student_del(student_id):
    db.db_del_student(student_id)


# Список всех прогулов
def truancy_list_all():
    list_truancy = db.db_list_truancy()

    out_str = f"```\n{"ДАТА":<10}¦КОЛ¦{"ТИП":<8}¦{"ID":^2}¦ИМЯ\n"
    for i in list_truancy:
        out_str += f"{i[0]}¦{i[3]:^3}¦{i[4]:<8}¦{i[1]:^2}¦{i[2]}\n"
    out_str += "```"
    return out_str

# Список прогулов за месяц
def truancy_list_month(month):
    truancy_date = datetime.strptime(month, r"%m-%y")
    # truancy_date = truancy_date.replace(tzinfo=timezone(timedelta(hours=3)))
    truancy_date = int(truancy_date.timestamp())

    list_truancy = db.db_get_all_truancy_for_month(truancy_date)

    out_str = f"```\n{"ДАТА":<10}¦КОЛ¦{"ТИП":<8}¦{"ID":^2}¦ИМЯ\n"
    for i in list_truancy:             
        out_str += f"{i[0]}¦{i[3]:^3}¦{i[4]:<8}¦{i[1]:^2}¦{i[2]}\n"
    out_str += "```"
    return out_str

# Добавить прогул
def truancy_add(student_id, truancy_number, truancy_type, truancy_date):
    truancy_date = datetime.strptime(truancy_date, r"%d-%m-%y")
    # truancy_date = truancy_date.replace(tzinfo=timezone(timedelta(hours=3)))
    truancy_date = int(truancy_date.timestamp())
    db.db_add_truancy(int(student_id), truancy_number, truancy_type, truancy_date)

# Удалить прогул
def truancy_del(truancy_date, student_id):
    truancy_date = datetime.strptime(truancy_date, r"%d-%m-%y")
    # truancy_date = truancy_date.replace(tzinfo=timezone(timedelta(hours=3)))
    truancy_date = int(truancy_date.timestamp())
    db.db_del_truancy(truancy_date, int(student_id))