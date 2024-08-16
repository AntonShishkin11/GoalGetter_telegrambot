import telebot
import datetime

from telebot import types

TOKEN = 'token'
bot = telebot.TeleBot(TOKEN)

last_user_date = {}

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    welcome_message = f'<b>👋 Hello {message.from_user.first_name}</b>\n✍️Welcome to GoalGetter\n\n' \
                      '✅GoalGetter is here to help you achieve your goals! ' \
                      'To get started, write your tasks in the chat.\n\n'

    bot.send_message(message.chat.id, welcome_message, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in last_user_date or last_user_date[chat_id] != datetime.date.today():
        # сообщение с текущей датой
        today_date = datetime.date.today().strftime("%d/%m/%Y")
        welcome_message = f'<b>🗓Task list from {today_date}</b>'
        bot.send_message(chat_id, welcome_message, parse_mode='HTML')

        last_user_date[chat_id] = datetime.date.today()


    copied_text = f"✍️{message.text}"

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("✔️ Complete", callback_data='execute')
    markup.add(button)
    bot.send_message(chat_id, copied_text, reply_markup=markup)

    bot.delete_message(message.chat.id, message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'execute')
def execute_message(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.message.text

    executed_text = f'<s>{text}</s>'.replace("✍️", "✅")

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Completed", callback_data='completed')
    markup.add(button)

    bot.edit_message_text(executed_text, chat_id, message_id, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'completed')
def mark_as_completed(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.message.text

    original_text = text.replace("✅", "✍️")

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("✔️ Complete", callback_data='execute')
    markup.add(button)

    bot.edit_message_text(original_text, chat_id, message_id, reply_markup=markup, parse_mode='HTML')

bot.polling()