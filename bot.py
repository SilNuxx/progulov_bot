import telebot, middle, config

API_TOKEN = config.data["token"]

bot = telebot.TeleBot(API_TOKEN)

# Переменные для добавления прогулов
student_id = ""
truancy_date = ""
truancy_number = ""
truancy_type = ""

# Приветственное сообщение, кратко о назначении бота и основных функциях
@bot.message_handler(commands=["start", "help"]) 
def bot_starting_msg(message):
    # Записано в таком виде, чтобы корректно видеть отступы в сообщении.
    help_message = r"""
*Доступные команды:*

/start - Список команд
/help - Список команд
/truancy\_list\_all - Список всех прогулов
/truancy\_list\_month - Список прогулов за месяц
/truancy\_add - Добавить прогул
/truancy\_del - Удалить прогул
/student\_list - Список всех студентов
/student\_info - Информация о студенте
/student\_add - Добавить студента
/student\_del - Удалить студента
/stop - Прервать действие
"""
    
    bot.send_message(chat_id=message.chat.id, text=help_message, parse_mode="markdown")

# Вывести список студентов
@bot.message_handler(commands=["student_list"]) 
def bot_student_list(message):
    bot.send_message(chat_id=message.chat.id, text=middle.student_list(), parse_mode="markdown")

# Информация о студенте
@bot.message_handler(commands=["student_info"]) 
def bot_student_info(message):
    bot.send_message(chat_id=message.chat.id, text="Введите *ID* студента", parse_mode="markdown")
    bot.register_next_step_handler(message, bot_student_info_print)
    
def bot_student_info_print(message):
    out_student_info = middle.student_info(message.text)
    bot.send_message(chat_id=message.chat.id, text=out_student_info)

# Добавить студента
@bot.message_handler(commands=["student_add"]) 
def bot_student_add_get_id(message):
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
    bot.send_message(chat_id=message.chat.id, text="Введите *ММ-ГГ*\n_(/stop - Прервать действие)_", parse_mode="markdown")
    bot.register_next_step_handler(message, bot_truancy_list_month)

def bot_truancy_list_month(message):
    month = message.text.strip().lower()
    if month == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        bot.send_message(chat_id=message.chat.id, text=middle.truancy_list_month(month), parse_mode="markdown")

# Добавить прогул
@bot.message_handler(commands=["truancy_add"]) 
def bot_truancy_add_get_id(message):
    bot.send_message(chat_id=message.chat.id, text="Введите *ID* студента\n_(/stop - Прервать действие)_", parse_mode="markdown")
    bot.register_next_step_handler(message, bot_truancy_add_get_truancy_date)

def bot_truancy_add_get_truancy_date(message):
    global student_id
    student_id = message.text.strip()
    if student_id == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ДД-ММ-ГГ* пропуска\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add_get_truancy_number)
    
def bot_truancy_add_get_truancy_number(message):
    global truancy_date
    truancy_date = message.text.strip()
    if truancy_date == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *КОЛИЧЕСТВО* пропущенных занятий\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add_get_truancy_type)

def bot_truancy_add_get_truancy_type(message):
    global truancy_number
    truancy_number = message.text
    if truancy_number == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ПРИЧИНУ* пропуска\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_add_get_truancy)

def bot_truancy_add_get_truancy(message):
    global truancy_type
    truancy_type = message.text.strip()
    if truancy_type == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        middle.truancy_add(student_id, truancy_number, truancy_type, truancy_date)
        bot.send_message(chat_id=message.chat.id, text="Пропуск добавлен")

# Удалить прогул
@bot.message_handler(commands=["truancy_del"]) 
def bot_truancy_del_get_id(message):
    bot.send_message(chat_id=message.chat.id, text="Введите *ID* студента\n_(/stop - Прервать действие)_", parse_mode="markdown")
    bot.register_next_step_handler(message, bot_truancy_del_get_truancy_date)

def bot_truancy_del_get_truancy_date(message):
    global student_id
    student_id = message.text.strip()
    if student_id == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите *ДД-ММ-ГГ* пропуска\n_(/stop - Прервать действие)_", parse_mode="markdown")
        bot.register_next_step_handler(message, bot_truancy_del)

def bot_truancy_del(message):
    global truancy_date
    truancy_date = message.text.strip()
    if truancy_date == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие прервано")
    else:
        middle.truancy_del(truancy_date, student_id)
        bot.send_message(chat_id=message.chat.id, text="Пропуск удалён")

bot.infinity_polling()
