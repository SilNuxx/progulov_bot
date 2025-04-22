import telebot

import middle
import config

API_TOKEN = config.data["token"]

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start", "help"]) # Приветственное сообщение, кратко о назначении бота и основных функциях
def bot_starting_msg(message):
    help_message = """
Доступные команды:

/start Список команд
/help - Список команд
/new_student - Добавить студента в БД
/del_student - Удалить студента из БД
/list_students - Список всех студентов
/info_student - Информация о студенте
/add_truancy - Добавить прогул
/del_truancy - Удалить прогул
    """
    
    bot.send_message(chat_id=message.chat.id, text=help_message)

@bot.message_handler(commands=["new_student"]) # Добавить нового студента
def bot_add_new_student(message):
    bot.send_message(chat_id=message.chat.id, text="Введите имя студента")
    bot.register_next_step_handler(message, middle.add_student)

@bot.message_handler(commands=["del_student"]) # Удалить студента
def bot_del_student(message):
    pass

@bot.message_handler(commands=["list_students"]) # Вывести список студентов
def bot_print_list_students(message):
    bot.send_message(chat_id=message.chat.id, text=middle.get_all_students())

@bot.message_handler(commands=["info_student"]) # Информация о студенте
def bot_print_info_student(message):
    pass

@bot.message_handler(commands=["add_truancy"]) # Добавить  прогул
def bot_register_truancy(message):
    pass

@bot.message_handler(commands=["del_truancy"]) # Удалить прогул
def bot_unregister_truancy(message):
    pass


bot.infinity_polling()