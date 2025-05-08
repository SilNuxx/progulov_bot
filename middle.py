import database as db
from datetime import datetime
from prettytable import PrettyTable

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

# Добавить студента
def student_add(student_name):
    db.db_add_student(student_name)

# Удалить студента
def student_del(student_id):
    db.db_del_student(int(student_id))


# Список всех прогулов или за конкретный месяц
def truancy_list(month=None):
    if month != None:
        truancy_date = datetime.strptime(month, "%m-%y")
        truancy_date = int(truancy_date.timestamp())
        list_truancy = db.db_get_all_truancy_for_month(truancy_date)
    else:
        list_truancy = db.db_list_truancy()
    
    table = PrettyTable()
    table.align = "l"
    table.field_names = ["ID", "ИМЯ", "КОЛ", "ТИП", "ДАТА"] 
    for i in list_truancy:
        truancy_date, student_id, student_name, truancy_count, truancy_type = i
        match truancy_type:
            case 0:
                truancy_type = "уваж"
            case 1:
                truancy_type = "болезнь"
            case 2:
                truancy_type = "неуваж"
            case _:
                pass
        table.add_row([student_id, student_name, truancy_count, truancy_type, truancy_date])
    out_str = f"```nix\n{table.get_formatted_string("text")}\n```"
    return out_str

# Добавить прогул
def truancy_add(student_id, truancy_date, truancy_count, truancy_type):
    truancy_date = datetime.strptime(truancy_date, "%d-%m-%y")
    truancy_date = int(truancy_date.timestamp())
    db.db_add_truancy(int(student_id), int(truancy_count), int(truancy_type), truancy_date)

# Изменить запись прогула
def truancy_upd(student_id, truancy_date, truancy_count, truancy_type):
    if truancy_count == "/empty": truancy_count = None
    if truancy_type == "/empty": truancy_type = None
    truancy_date = datetime.strptime(truancy_date, "%d-%m-%y")
    truancy_date = int(truancy_date.timestamp())
    db.db_update_truancy(truancy_date, int(student_id), truancy_count, truancy_type)

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

generate_report("03-25", "A2289")