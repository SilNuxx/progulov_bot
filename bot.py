import telebot, middle, config

API_TOKEN = config.data["token"]

bot = telebot.TeleBot(API_TOKEN)

# Список аргументов команды
args = []

# Приветственное сообщение, кратко о назначении бота и основных функциях
@bot.message_handler(commands=["start", "help"]) 
def bot_starting_msg(message):
    # Записано в таком виде, чтобы корректно видеть отступы в сообщении.
    help_message = r"""
*Доступные команды:*

/start - Список команд
/help - Список команд
/report - Создать отчёт за месяц
/truancy\_list\_all - Список всех прогулов
/truancy\_list\_month - Список прогулов за месяц
/truancy\_add - Добавить прогул
/truancy\_del - Удалить прогул
/student\_list - Список всех студентов
/student\_add - Добавить студента
/student\_del - Удалить студента
/stop - Прервать действие
"""
    
    bot.send_message(chat_id=message.chat.id, text=help_message, parse_mode="markdown")

# Вывести список студентов
@bot.message_handler(commands=["student_list"]) 
def bot_student_list(message):
    bot.send_message(chat_id=message.chat.id, text=middle.student_list(), parse_mode="markdown")

# Добавить студента
@bot.message_handler(commands=["student_add"]) 
def bot_student_add_get_id(message):
    if len(message.text.strip().split()) > 1:
        student_name = " ".join(message.text.strip().split()[1:])
        out_str = middle.student_add(student_name)
        bot.send_message(chat_id=message.chat.id, text="Студент добавлен")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ФИО* студента\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_student_add)

def bot_student_add(message):
    student_name = message.text.strip()
    if student_name == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        middle.student_add(student_name)
        bot.send_message(chat_id=message.chat.id, text="Студент добавлен")

# Удалить студента
@bot.message_handler(commands=["student_del"]) 
def bot_student_del_get_id(message):
    if len(message.text.strip().split()) > 1:
        student_id = message.text.strip().split()[1]
        out_str = middle.student_del(student_id)
        bot.send_message(chat_id=message.chat.id, text="Студент удалён")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ID* студента\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_student_del)

def bot_student_del(message):
    student_id = message.text.strip()
    if student_id == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        middle.student_del(student_id)
        bot.send_message(chat_id=message.chat.id, text="Студент удалён")

#  Список всех прогулов
@bot.message_handler(commands=["truancy_list_all"]) 
def bot_truancy_list_all(message):
    bot.send_message(chat_id=message.chat.id, text=middle.truancy_list_all(), parse_mode="markdown")
    
#  Список прогулов за месяц
@bot.message_handler(commands=["truancy_list_month"]) 
def bot_truancy_list_month_get_month(message):
    if len(message.text.strip().split()) > 1:
        truancy_month = message.text.strip().split()[1]
        out_student_info = middle.truancy_list_month(truancy_month)
        bot.send_message(chat_id=message.chat.id, text=out_student_info, parse_mode="markdown")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ММ-ГГ*\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_list_month)

def bot_truancy_list_month(message):
    truancy_month = message.text.strip().lower()
    if truancy_month == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        bot.send_message(chat_id=message.chat.id, text=middle.truancy_list_month(truancy_month), parse_mode="markdown")

# Добавить прогул
@bot.message_handler(commands=["truancy_add"]) 
def bot_truancy_add_get_id(message):
    if len(message.text.strip().split()) > 1:
        args = message.text.strip().split()[1:]
        out_student_info = middle.truancy_add(*args)
        bot.send_message(chat_id=message.chat.id, text="Пропуск добавлен")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ID* студента\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add_get_truancy_date)

def bot_truancy_add_get_truancy_date(message):
    global args
    student_id = message.text.strip()
    if student_id == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(student_id)
        bot.send_message(chat_id=message.chat.id, text="Введите *ДД-ММ-ГГ* пропуска\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add_get_truancy_count)
    
def bot_truancy_add_get_truancy_count(message):
    global args
    truancy_date = message.text.strip()
    if truancy_date == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(truancy_date)
        bot.send_message(chat_id=message.chat.id, text="Введите *КОЛИЧЕСТВО* пропущенных занятий\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add_get_truancy_type)

def bot_truancy_add_get_truancy_type(message):
    global args
    truancy_count = message.text.strip()
    if truancy_count == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(truancy_count)
        bot.send_message(
            chat_id=message.chat.id, 
            # Записано в таком виде, чтобы корректно видеть отступы в сообщении.
            text="""
Введите *ПРИЧИНУ* пропуска цифрой
*0* - Уважительная
*1* - По болезни
*2* - Не уважительная
_(/stop - Прервать действие)_""", 
            parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add)

def bot_truancy_add(message):
    global args
    truancy_type = message.text.strip()
    if truancy_type == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(truancy_type)
        middle.truancy_add(*args)
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Пропуск добавлен")

# Удалить прогул
@bot.message_handler(commands=["truancy_del"]) 
def bot_truancy_del_get_id(message):
    if len(message.text.strip().split()) > 1:
        args = message.text.strip().split()[1:]
        out_student_info = middle.truancy_del(*args)
        bot.send_message(chat_id=message.chat.id, text="Пропуск удалён")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ID* студента\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_del_get_truancy_date)

def bot_truancy_del_get_truancy_date(message):
    global args
    student_id = message.text.strip()
    if student_id == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(student_id)
        bot.send_message(chat_id=message.chat.id, text="Введите *ДД-ММ-ГГ* пропуска\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_del)

def bot_truancy_del(message):
    global args
    truancy_date = message.text.strip()
    if truancy_date == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(truancy_date)
        middle.truancy_del(*args)
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Пропуск удалён")

# Создать отчёт за месяц
@bot.message_handler(commands=["report"]) 
def bot_report_get_date(message):
    if len(message.text.strip().split()) > 1:
        args = message.text.strip().split()[1:]
        middle.generate_report(*args)
        report_file = open(config.data["report_file"], "rb")
        bot.send_document(message.chat.id, report_file)
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ММ-ГГ*\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_report_get_group_name)

def bot_report_get_group_name(message):
    global args
    truancy_date = message.text.strip()
    if truancy_date == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(truancy_date)
        bot.send_message(chat_id=message.chat.id, text="Введите *ГРУППА*\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_report)

def bot_report(message):
    global args
    group_name = message.text.strip()
    if group_name == "/stop":
        args.clear()
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        args.append(group_name)
        middle.generate_report(*args)
        args.clear()
        report_file = open(config.data["report_file"], "rb")
        bot.send_document(message.chat.id, report_file)

bot.infinity_polling()
