import config
from flask import Flask, request
import telebot



token = config.token

bot = telebot.TeleBot(token)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Some message to ' + message.fr)

@server.route('/'+token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.WEBHOOK_URL_BASE+config.WEBHOOK_URL_PATH)
    return "!", 200

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=443)

