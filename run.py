#! /usr/bin/env python
# -*- coding: utf-8 -*-

import bot_control
import functions
import os
import daemon

from functions import handling_connection_error

from telebot import TeleBot
from bot_answering import AnsweringBot
from register import Register


def main_definition():
    """Определение управляющего бота, регистрации, автоответчика"""
    try:
        configs = functions.load_data('data/config-bot.json')
        bot_token, my_id = configs['TOKEN'], configs['my_ID']

    except FileNotFoundError as error:
        message = "\n - Файл с конфигурациями для бота не найден! Зарегестрируйте данные!"
        print(message + "\n")

        functions.logging(message, error)
        functions.do_command()
    else:
        bot = TeleBot(bot_token)
        bot.remove_webhook()

        registration = Register()
        answering_bot = AnsweringBot()

        if not os.path.exists(registration.LOGS):
            functions.creating_file(registration.LOGS)

        return bot, registration, answering_bot, my_id


@functions.handling_connection_error
def run():
    """Основной запуск программы (запуск управляющего бота)"""
    bot, registration, answering_bot, my_id = main_definition()
    bot_control.run(bot, registration, answering_bot, my_id)



if __name__ == '__main__':
    run()
