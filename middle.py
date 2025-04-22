import database

def add_student(msg):
    database.db_add_student(msg.text)

def get_all_students():
    list_student = database.db_get_all_sort_studnet_list()

    out_str = "ID, NAME\n---\n"
    for i in list_student:
        out_str += f"{i[0]}, {i[1]}\n---\n"

    return out_str