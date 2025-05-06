import database as db
from datetime import datetime

import report
import config

# Вывести список студентов
def student_list():
    list_student = db.db_get_all_sort_student_list()

    out_str = f"```nix\nID¦ИМЯ\n"
    for i in list_student:
        out_str += f"{i[0]:^2}¦{i[1]}\n"
    out_str += "```"
    return out_str

# Получить информацию о студенте
def student_info(student_id):
    student_info = db.db_get_student(student_id)
    out_str = f"*ID:* {student_info[0]}\n*ИМЯ:* {student_info[1]}"
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

    out_str = f"```nix\n{"ДАТА":<10}¦КОЛ¦{"ТИП":<8}¦ID¦ИМЯ\n"
    for i in list_truancy:
        out_str += f"{i[0]}¦{i[3]:^3}¦{i[4]:<8}¦{i[1]:^2}¦{i[2]}\n"
    out_str += "```"
    return out_str

# Список прогулов за месяц
def truancy_list_month(month):
    truancy_date = datetime.strptime(month, "%m-%y")
    truancy_date = int(truancy_date.timestamp())

    list_truancy = db.db_get_all_truancy_for_month(truancy_date)

    out_str = f"```nix\n{"ДАТА":<10}¦КОЛ¦{"ТИП":<8}¦ID¦ИМЯ\n"
    for i in list_truancy:             
        out_str += f"{i[0]}¦{i[3]:^3}¦{i[4]:<8}¦{i[1]:^2}¦{i[2]}\n"
    out_str += "```"
    return out_str

# Добавить прогул
def truancy_add(student_id, truancy_date, truancy_number, truancy_type):
    truancy_date = datetime.strptime(truancy_date, "%d-%m-%y")
    truancy_date = int(truancy_date.timestamp())
    db.db_add_truancy(int(student_id), truancy_number, truancy_type, truancy_date)

# Удалить прогул
def truancy_del(student_id, truancy_date):
    truancy_date = datetime.strptime(truancy_date, "%d-%m-%y")
    truancy_date = int(truancy_date.timestamp())
    db.db_del_truancy(truancy_date, int(student_id))

# Генерация отчёта за месяц
def generate_report(date, group: str):
    truancy_date = datetime.strptime(date, "%m-%y")

    # Создание заголовка
    title = "Сводная ведомость посещаемости учебных занятий группы"
    report_info = f"{group} за {config.month[truancy_date.month]} {truancy_date.year} года"

    pdf = report.Report()
    pdf.create_headers(title, report_info)

    # Получение всех записей
    list_truancy = db.db_get_all_truancy_for_month(int(truancy_date.timestamp()))
    
    # Создание таблицы
    pdf.create_table(list_truancy)

    # Создание файла
    pdf.output(config.data["report_file"])
