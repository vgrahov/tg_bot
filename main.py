import os
import config
from flask import Flask, request
import telebot


token = config.token

bot = telebot.TeleBot(token)

server = Flask(__name__)

@server.route("/")
def webhook():
    bot.remove_webhook()

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8443)

