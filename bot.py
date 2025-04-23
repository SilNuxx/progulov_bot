import telebot

import middle, config

API_TOKEN = config.data["token"]

bot = telebot.TeleBot(API_TOKEN)

# Приветственное сообщение, кратко о назначении бота и основных функциях
@bot.message_handler(commands=["start", "help"]) 
def bot_starting_msg(message):
    # Записано в таком виде, чтобы корректно видеть отступы в сообщении.
    help_message = """
Доступные команды:

/start Список команд
/help - Список команд
/list_students - Список всех студентов
/info_student - Информация о студенте
/add_truancy - Добавить прогул
/del_truancy - Удалить прогул
/add_student - Добавить студента
/del_student - Удалить студента
    """
    
    bot.send_message(chat_id=message.chat.id, text=help_message)

# Вывести список студентов
@bot.message_handler(commands=["list_students"]) 
def bot_print_list_students(message):
    bot.send_message(chat_id=message.chat.id, text=middle.get_all_students())

# Информация о студенте
@bot.message_handler(commands=["info_student"]) 
def bot_print_info_student(message):
    pass

# Добавить прогул
@bot.message_handler(commands=["add_truancy"]) 
def bot_add_truancy(message):
    pass

# Удалить прогул
@bot.message_handler(commands=["del_truancy"]) 
def bot_del_truancy(message):
    pass

# Добавить студента
@bot.message_handler(commands=["add_student"]) 
def bot_add_student(message):
    bot.send_message(chat_id=message.chat.id, text="Введите имя студента")
    bot.register_next_step_handler(message, middle.add_student)

# Удалить студента
@bot.message_handler(commands=["del_student"]) 
def bot_del_student(message):
    pass

bot.infinity_polling()
