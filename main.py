import os 
from dotenv import load_dotenv
import telebot
from telebot import types 
import psycopg2


load_dotenv()
token_api = os.getenv("TOKEN_KEY")

conn = psycopg2.connect(
    dbname="telebot12_7217"
    user="telebot12_7217"
    password="postgres://telebot12_7217:sCq5QyGp3_Ky49L1Zd2io_IBXWY7BqvjYGVm5lBM1749Un4m_j60o2eNVJ0lGeky@telebot12-7217.postgresql.c.osc-fr1.scalingo-dbs.com:34742/telebot12_7217?sslmode=prefer"
    host="telebot12-7217.postgresql.c.osc-fr1.scalingo-dbs.com"
    port="34742"
    sslmode="prefer" 
)

conn.autocommit = True
cursor =conn.cursor()
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS tele_users(
            ID SERIAL PRIMARY KEY,
            Name varchar(30),
            Age integer
        )
    """
)



bot = telebot.TeleBot(token_api)
# print(bot)

name = ""
surname = ""
age = 0


@bot.message_handler(content_types=["text"])
def start(message, res = False):
    chat_id = message.chat.id
    if message.text == "/reg":
        bot.send_message(chat_id, "Напиши свое имя")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(chat_id, "Напиши /reg")

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у тебя Фамилия")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Напиши возраст")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age 

    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, "Цифрами пожалуста")

    keyboar = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="yes", callback_data="yes")
    keyboar.add(key_yes)
    key_no = types.InlineKeyboardButton(text = "no", callback_data="no")
    keyboar.add(key_no)
    question = f"тебе {str(age)} лет, тебя зовут{name} {surname}?"
    bot.send_message(message.chat.id, question, reply_markup=keyboar)

@bot.callback_query_handler(func=lambda call: True)
def call_back(call):

    if call.data == "yes":
            user_name = name + surname
            # код добавления в базу
    cursor.execute(
        """
                    INSERT INTO tele_users(name, age)
                    VALUES(%s, %s)
""",
            (user_name, age),
)


    bot.send_message(call.message.chat.id, text="вы успешно зарегистрированы")
#elif call.data == "no":
#переспрашиваем










# @bot.message_handler(content_types=["text",])
# def handle_text(message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, text=f"Вы написали: {message.text}")

    # if message.text.lower() == 'привет':
    #     bot.send_message(chat_id, "Привет что я могу для вас сделать")



#работай алоо

bot.polling(none_stop=True, interval=0)






