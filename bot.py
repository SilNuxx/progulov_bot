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
    help_message = """
Доступные команды:

/start - Список команд
/help - Список команд
/truancy_list - Список прогулов
/truancy_add - Добавить прогул
/truancy_del - Удалить прогул
/student_list - Список всех студентов
/student_info - Информация о студенте
/student_add - Добавить студента
/student_del - Удалить студента
"""
    
    bot.send_message(chat_id=message.chat.id, text=help_message)

# Вывести список студентов
@bot.message_handler(commands=["student_list"]) 
def bot_student_list(message):
    bot.send_message(chat_id=message.chat.id, text=middle.student_list())

# Информация о студенте
@bot.message_handler(commands=["student_info"]) 
def bot_student_info(message):
    bot.send_message(chat_id=message.chat.id, text="Введите ID студента")
    bot.register_next_step_handler(message, bot_student_info_print)
    
def bot_student_info_print(message):
    out_student_info = middle.student_info(message.text)
    bot.send_message(chat_id=message.chat.id, text=out_student_info)

# Добавить студента
@bot.message_handler(commands=["student_add"]) 
def bot_student_add_get_id(message):
    bot.send_message(chat_id=message.chat.id, text="Введите имя студента")
    bot.register_next_step_handler(message, bot_student_add)

def bot_student_add(message):
    student_name = message.text.strip()
    middle.student_add(student_name)
    bot.send_message(chat_id=message.chat.id, text="Студент добавлен")

# Удалить студента
@bot.message_handler(commands=["student_del"]) 
def bot_student_del_get_id(message):
    bot.send_message(chat_id=message.chat.id, text="Введите ID студента")
    bot.register_next_step_handler(message, bot_student_del)

def bot_student_del(message):
    student_id = message.text.strip()
    middle.student_del(student_id)
    bot.send_message(chat_id=message.chat.id, text="Студент удалён")

#  Список прогулов
@bot.message_handler(commands=["truancy_list"]) 
def bot_truancy_list(message):
    bot.send_message(chat_id=message.chat.id, text=middle.truancy_list())

# Добавить прогул
@bot.message_handler(commands=["truancy_add"]) 
def bot_truancy_add_get_id(message):
    bot.send_message(chat_id=message.chat.id, text="Введите ID студента")
    bot.register_next_step_handler(message, bot_truancy_add_get_truancy_date)

def bot_truancy_add_get_truancy_date(message):
    global student_id
    student_id = message.text.strip()
    bot.send_message(chat_id=message.chat.id, text="Введите дату пропуска\nДД-ММ-ГГ")
    bot.register_next_step_handler(message, bot_truancy_add_get_truancy_number)
    
def bot_truancy_add_get_truancy_number(message):
    global truancy_date
    truancy_date = message.text.strip()
    bot.send_message(chat_id=message.chat.id, text="Введите количество пропущенных занятий")
    bot.register_next_step_handler(message, bot_truancy_add_get_truancy_type)

def bot_truancy_add_get_truancy_type(message):
    global truancy_number
    truancy_number = int(message.text)
    bot.send_message(chat_id=message.chat.id, text="Введите тип/причину пропуска")
    bot.register_next_step_handler(message, bot_truancy_add_get_truancy)

def bot_truancy_add_get_truancy(message):
    global truancy_type
    truancy_type = message.text.strip()
    middle.truancy_add(student_id, truancy_number, truancy_type, truancy_date)
    bot.send_message(chat_id=message.chat.id, text="Пропуск добавлен")

# Удалить прогул
@bot.message_handler(commands=["truancy_del"]) 
def bot_truancy_del_get_id(message):
    bot.send_message(chat_id=message.chat.id, text="Введите ID студента")
    bot.register_next_step_handler(message, bot_truancy_del_get_truancy_date)

def bot_truancy_del_get_truancy_date(message):
    global student_id
    student_id = message.text.strip()
    bot.send_message(chat_id=message.chat.id, text="Введите дату пропуска\nДД-ММ-ГГ")
    bot.register_next_step_handler(message, bot_truancy_del)

def bot_truancy_del(message):
    global truancy_date
    truancy_date = message.text.strip()
    middle.truancy_del(truancy_date, student_id)
    bot.send_message(chat_id=message.chat.id, text="Пропуск удалён")

bot.infinity_polling()
