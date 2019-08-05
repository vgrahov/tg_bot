# -*- coding: utf-8 -*-

import config
import telebot
import cherrypy
#from telebot import apihelper


#apihelper.proxy = {'https': config.socks_proxy}
bot = telebot.TeleBot(config.token)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.header and \
            'content-type' in cherrypy.request.headers and \
             cherrypy.request.headers['content-type'] == 'application/json':
            length = int (cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates(update)
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL_BASE+config.WEBHOOK_URL_PATH)
cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin' #,
#    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
#    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})




#if __name__ == '__main__':
#    bot.polling(none_stop=True)