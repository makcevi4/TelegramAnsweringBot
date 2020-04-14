import time

import buttons
import functions

from telebot import types


# @functions.handling_error
def run(bot, registration, answering_bot, my_id):
    """Главный запуск управляющего бота"""
    functions.logging('\n-Бот запущен', 'Отсутствует', 'Запуск бота управления автоответчиком')

    @bot.message_handler(commands=['start'])
    def greeting(message):
        """Приветствие, отображение главного меню (закреплённого снизу)"""

        if message.chat.id == my_id:
            bot.send_photo(chat_id=my_id, photo='https://imgur.com/a/we3FSop')

            text = "Привет!\nДля максимально правильного использования бота, " \
                   "рекомендуем ознакомиться с документацией по использованию бота в разделе <b>'Помощь'</b>" \
                   ""
            bot.send_message(chat_id=my_id, text=text, parse_mode='HTML', reply_markup=buttons.main_menu())
        else:
            bot.send_message(message.chat.id, "Вы не являетесь владельцем бота!")
            time.sleep(2)

    @bot.message_handler(content_types=['text'])
    def main_menu_handling(message):
        """Обработка главного меню (закреплённого снизу)"""

        # При переходе в раздел 'Управление автоответчиком'
        if message.text == 'Управление автоответчиком🎮':
            text = "<b>Панель управления автоответчиком</b>" \
                   "\n🕹 - Включить/Выключить" \
                   "\n💡 - Статус" \
                   "\n🎛 - Выбор режима (Друзья/Все)" \
                   "\n📰 - Название сессии" \
                   "\n🖥 - Вывести всю информацию в сообщение"
            bot.send_message(chat_id=my_id,
                             text=text,
                             parse_mode='HTML',
                             reply_markup=buttons.bot_management())

        # при переходе в раздел 'Регистрация'
        if message.text == 'Регистрация⚙️':
            text = "<b>Регистрация данных</b>" \
                   "\n1️⃣ - Регистрация данных для авторизации" \
                   "\n2️⃣ - Добавить человека в список друзей" \
                   "\n3️⃣ - Добавить человека в чёрный список" \
                   "\n4️⃣ - Показать пользователей из списка друзей" \
                   "\n5️⃣ - Показать пользователей из чёрного списка"
            bot.send_message(chat_id=my_id,
                             text=text,
                             parse_mode='HTML',
                             reply_markup=buttons.registration_data())

        # при переходе в раздел 'Помощь'
        if message.text == 'Помощь🔔':
            text = "<b>Помощь</b>" \
                   "\n📚 - ЧаВО" \
                   "\n📄 - Документация" \
                   "\n📨 - Связь с разработчиком" \
                   "\n📝 - Посмотреть логи"
            bot.send_message(chat_id=my_id,
                             text=text,
                             parse_mode='HTML',
                             reply_markup=buttons.help_section())

    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        """Обработка запросов"""
        # ПАНЕЛЬ УПРАВЛЕНИЯ АТООТВЕТЧИКОМ

        # - включение/выключение автоответчика
        if call.data == 'set_activity':
            if not answering_bot.status:
                bot.answer_callback_query(callback_query_id=call.id, text='Запущено')
                answering_bot.status = True
                answering_bot.run()
                # activity = "Запущено"
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Приостановлено')
                answering_bot.status = False
                # activity = "Приостановлено"
            # bot.answer_callback_query(callback_query_id=call.id, text=activity)

        if call.data == 'set_mode':
            if answering_bot.mode == 'friends':
                answering_bot.mode = 'all'
                mode = "Режим 'ВСЕ' активирован"
            else:
                answering_bot.mode = 'friends'
                mode = "Режим 'ДРУЗЬЯ' активирован"
            bot.answer_callback_query(callback_query_id=call.id, text=mode)

        # - получение статуса автоответчика
        if call.data == 'get_status':
            if answering_bot.status:
                status = 'Автоответчик включен'
            else:
                status = 'Автоответчик выключен'
            bot.answer_callback_query(callback_query_id=call.id, text=status)

        # - получение имени сессии
        if call.data == 'get_session_name':
            session_name = "Название сессии: %s" % answering_bot.session
            bot.answer_callback_query(callback_query_id=call.id, text=session_name)

        # - вывод полной информации в сообщение
        if call.data == 'show_all_info':
            # статус
            if answering_bot.status:
                info = "Статус: Работает\n"
            else:
                info = "Статус: Выключен\n"

            if answering_bot.mode == 'friends':
                info += 'Режим: Друзья\n'
            else:
                info += 'Режим: Все\n'

            # сессия
            info += "Название сессии: %s" % answering_bot.session
            bot.send_message(chat_id=my_id, text=info)

        # РЕГИСТРАЦИЯ
        # - регистрация данных для авторизациия бота
        if call.data == 'registration_data':
            bot.answer_callback_query(callback_query_id=call.id, text='Недоступно!')
            bot.send_message(chat_id=my_id, parse_mode='HTML',
                             text="❗️Недоступно❗\n️"
                                  "К сожалению, данная функция пока что <b>недоступна</b> в приложении Телеграма."
                                  " Чтоб зарегистрировать данные для входа, <b>воспользуйтесь консолью</b> "
                                  "(больше информации в разделе <b>'Помощь'</b>).")

        # - добавление пользователя в список друзей
        if call.data == 'registration_user':
            bot.answer_callback_query(callback_query_id=call.id, text='Недоступно!')
            bot.send_message(chat_id=my_id, parse_mode='HTML',
                             text="❗Недоступно❗️\n️"
                                  "К сожалению, данная функция пока что <b>недоступна</b> в приложении Телеграма."
                                  " Чтоб добавить пользователя в список друзей, <b>воспользуйтесь консолью</b> "
                                  "(больше информации в разделе <b>'Помощь'</b>).")

        # - добавление пользователя в чёрный список
        if call.data == 'registration_to_blacklist':
            bot.answer_callback_query(callback_query_id=call.id, text='Недоступно!')
            bot.send_message(chat_id=my_id, parse_mode='HTML',
                             text="❗Недоступно❗️\n️"
                                  "К сожалению, данная функция пока что <b>недоступна</b> в приложении Телеграма."
                                  " Чтоб добавить пользователя в чёрный список, <b>воспользуйтесь консолью</b> "
                                  "(больше информации в разделе <b>'Помощь'</b>).")

        # - получение информации о всех зарегестрированных пользователях
        if call.data == 'get_registered_users':
            users = functions.load_data('data/users.json')
            text = functions.formatting_dictionary_data(users)
            bot.send_message(chat_id=my_id, text=text, parse_mode='HTML')
            bot.answer_callback_query(callback_query_id=call.id, text='Успешно!')

        if call.data == 'get_blocked_users':
            blacklist = functions.load_data('data/blacklist.json')
            text = functions.formatting_list_data(blacklist)
            bot.send_message(chat_id=my_id, text=text, parse_mode='HTML')
            bot.answer_callback_query(callback_query_id=call.id, text='Успешно!')

        # ПОМОЩЬ
        # - частые вопросы и ответы
        if call.data == 'help_faq':
            bot.answer_callback_query(callback_query_id=call.id, text='В разработке')
            text = "<b>Частые вопросы - ответы</b>" \
                   "\nПримечание: В - Вопрос, О - Ответ" \

        # - документация
        if call.data == 'help_documentation':
            bot.answer_callback_query(callback_query_id=call.id, text='В разработке')
            text = "<b>Документация</b>" \
                   "\nПолная документация по автоответчику доступна к прочтению по ссылке:" \
                   "\nhttps://github.com/makcevi4/TelegramAnsweringBot"

        # - связь с разработчиком
        if call.data == 'help_communication':
            text = "<b>Для вопросов, жалоб и предложений:</b>" \
                   "\nTelegram: @Makcevi4" \
                   "\nMail: bohynskyimaksym@gmail.com" \
                   "\nGitHub: https://github.com/makcevi4"
            bot.send_message(chat_id=my_id, text=text, parse_mode='HTML')
            bot.answer_callback_query(callback_query_id=call.id, text='✅')

        # - просмотр логов
        if call.data == 'help_logs':
            text = "<b>ЛОГИ</b>\n\n"
            text += functions.show_logs()
            bot.send_message(chat_id=my_id, text=text, parse_mode='HTML')
            bot.answer_callback_query(callback_query_id=call.id, text='✅')

    bot.polling(none_stop=True)
