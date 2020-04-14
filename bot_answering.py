import json
import time
import random
import datetime
import pytz

import functions

from pyrogram import Client, MessageHandler
from pyrogram import errors


from cryptography.fernet import Fernet, InvalidToken


class AnsweringBot:
    """Класс представляющий автоответчик"""
    def __init__(self, session='Автоответчик'):
        """Инициализация основных данных, для работы автоответчика"""
        self.session = session
        self.status = False
        self.mode = 'friends'

        self.__ID = None
        self.__HASH = None
        self.__PHONE = None
        self.__PASSWORD = None

        self.PATH = 'data/'
        self.BOT_CONFIG = self.PATH + 'config-bot.json'
        self.CONFIG = self.PATH + 'config-auth.json'
        self.SETUPS = self.PATH + 'setups.json'
        self.BLACKLIST = self.PATH + 'blacklist.json'
        self.USERS = self.PATH + 'users.json'

        self.MY_ID = self.__load_file(self.BOT_CONFIG)['my_ID']
        self.BOT_ID = self.__load_file(self.BOT_CONFIG)['ID']
        self.TIMEZONE = self.__load_file(self.BOT_CONFIG)['my_TZ']
        self.DISABLED = []

    # ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ

    @staticmethod
    def __load_file(file):
        """Загрузка файлов"""
        try:
            with open(file, 'r') as of:
                return json.load(of)
        except FileNotFoundError as error:
            message = "\n -Отсутствуют файлы для входа в аккаунт, пожалуйста зарегестрируйте их!"
            print(message + "\n")

            functions.logging(message, error)
            functions.do_command()

    #  ГЛАВНЫЕ МЕТОДЫ

    def __auth(self):
        """Авторизация автоответчика в Телеграм-аккаунте, с которого нужно отправлять сообщения"""
        message = "\n-Ошибка авторизации! Некорректные данные для входа (ID/HASH/PHONE or PASSWORD)" \
                  "\nПопробуйте зарегестрировать данные ещё раз!!"

        if self.__PASSWORD:
            try:
                return Client(session_name=self.session,
                              api_id=self.__ID,
                              api_hash=self.__HASH,
                              phone_number=self.__PHONE,
                              password=self.__PASSWORD)
            except errors.RPCError as error:
                print(message + "\n")

                functions.logging(message, error)
        else:
            try:
                return Client(session_name=self.session,
                              api_id=self.__ID,
                              api_hash=self.__HASH,
                              phone_number=self.__PHONE)
            except errors.RPCError as error:
                print(message + "\n")

                functions.logging(message, error)

    def __decrypt(self):
        """Расшифровка данных"""

        def organize(got_dict):
            """Получение ключей словаря с данными, для дальнейшей работы с ними, добавление ключей в список"""
            organized_list = []
            for item in got_dict.keys():
                organized_list.append(item)
            return organized_list

        def key_definition(keys_list, config_list):
            """Определение ключа для расшифровки"""
            random_number = random.randint(0, 1)
            if random_number == 0:
                return config_list[keys_list[-2]]
            if random_number == 1:
                key_number = config_list[keys_list[-1]] - (config_list[keys_list[-1]] - config_list[keys_list[-2]])

                return key_number

        config = self.__load_file(self.CONFIG)
        setups = self.__load_file(self.SETUPS)

        organized = organize(config)

        i = 0
        c = len(organized) - 2

        while i < c:

            number = key_definition(organized, config)
            key = organized[i]

            decrypted_item = Fernet(setups[number + i].encode('utf-8')).decrypt(config[key].encode('utf-8')).decode(
                'utf-8')

            if key == 'id'.upper():
                self.__ID = decrypted_item
            if key == 'hash'.upper():
                self.__HASH = decrypted_item
            if key == 'phone'.upper():
                self.__PHONE = decrypted_item
            if key == 'password'.upper():
                self.__PASSWORD = decrypted_item
            i += 1

    # ЗАПУСК

    def run(self):
        """Запуск автоответчика"""
        def auto_blocking():
            """
            Автоматическое блокирование себя и управляющего бота для того,
            чтоб автоответчик не отвечал на наши сообщения
            """
            black_list = self.__load_file(self.BLACKLIST)
            if self.MY_ID and self.BOT_ID in black_list:
                pass
            else:
                black_list.append(self.MY_ID)
                black_list.append(self.BOT_ID)
                with open(self.BLACKLIST, 'w') as file:
                    json.dump(black_list, file)

        def handling_errors(function_for_handling):
            """Обработка основных ошибок: превышен лимит запросов, остутствие API ключа"""
            try:
                function_for_handling()
            except errors.FloodWait as error:
                message = "- Ошибка авторизации! Слишком много запросов,"\
                          " чтоб попробовать ещё раз ожидайте %s" % functions.flood_wait_error(error.x)
                print(message + "\n")

                functions.logging(message, error)

            except AttributeError as error:
                message = "- Не найдет ключ API"
                print(message + "\n")

                functions.logging(message, error)

        def handling_message(msg):
            """Обработка сообщения: отсортировка ID пользователя от ID группы"""
            if len(str(msg)) < 11:
                return msg
            else:
                return False

        def check_for_friend(user, user_dict):
            """Проверка отправителя, находится ли он в списке друзей"""
            if user in user_dict.values():
                return True
            else:
                return False

        def check_for_banned(sender, black_list):
            """Проверка отправителя, находится ли он в чёрном списке"""
            if sender in black_list:
                return True
            else:
                return False

        def main_check(user, bl, ul):
            """Основная проверка: на наличие пользователя в чёрном списке и списке друзей"""
            try:
                banned = check_for_banned(user, bl)
                in_friend_list = check_for_friend(user, ul)
                return banned, in_friend_list
            except AttributeError as error:
                functions.logging("Неизвестно", error)
                return 0

        def get_message_via_time():
            """Получение характерного сообщения в зависимости от времни"""
            if self.TIMEZONE:
                current_time = int(datetime.datetime.now(tz=pytz.timezone(self.TIMEZONE)).strftime('%H'))
            else:
                current_time = int(datetime.datetime.now().strftime('%H'))
            if 0 <= current_time <= 9 or 21 <= current_time <= 23:
                return "Я сплю, пожалуйста напиши позже!"
            else:
                return "Я сейчас занят, пожалуйста напиши позже!🤷‍♂️"

        def scenario_all(uid, msg):
            message = get_message_via_time()
            application.send_message(uid, message)
            time.sleep(1)

        def scenario_friends(uid, msg, login):
            if ('ВАЖНО' or '!ВАЖНО') in msg.upper():
                if len(msg) > 6:
                    message = "Отлично! Это сообщение я прочту первым, как освобожусь."
                    important_message = "👤: {}\n📩: {}".format(("@" + login), msg[6:])
                    application.send_message(uid, message)
                    application.send_message('me', important_message)
                    functions.logging('  Получено важное сообщение от @{}'.format(login),
                                      'Отсутствует',
                                      'Получено важное сообщение')
                else:
                    message = "Ты забыл ввести текст, после пометки '!ВАЖНО'. Попробуй ещё раз!"
                    application.send_message(uid, message)
            else:
                message = get_message_via_time()
                message += "\nЕсли у тебя что-то важное, отправь: \n'!ВАЖНО <Текст сообщения>'"
                application.send_message(uid, message)
                time.sleep(1)

        def handling_notifications(status):
            if status:
                # disable notifications
                #
                # application.forward_messages()
                pass
            else:
                # enable notifications
                pass

        # расшифровка данных
        self.__decrypt()

        # загрузка списка с друзьями и чёрного списка
        users = self.__load_file(self.USERS)
        blacklist = self.__load_file(self.BLACKLIST)

        # авторизация
        application = self.__auth()

        # блокируем себя и бота, чтоб не получать сообщения
        auto_blocking()

        while True:
            if self.status:
                application.start()
                functions.logging(' -Автоответчик запущен', 'Отсутствует', 'Запуск автоответчика')
                break

        while True:
            if self.status:

                @handling_errors
                def handled_answering():
                    @application.on_message()
                    def answering(client, message):
                        try:

                            user_id = handling_message(message.from_user.id)
                            banned, in_friend_list = main_check(user_id, blacklist, users)

                        except AttributeError:
                            pass
                        else:
                            if self.mode == 'friends':
                                if not banned and in_friend_list:
                                    scenario_friends(user_id, message.text, message.from_user.username)
                                    print(message)

                            if self.mode == 'all':
                                if not banned:
                                    if in_friend_list:
                                        scenario_friends(user_id, message.text, message.from_user.username)
                                    else:
                                        scenario_all(user_id, message.text)

            time.sleep(2)

            if not self.status:
                application.stop()
                functions.logging(' -Автоответчик остановлен', 'Отсутствует', 'Выключение автоответчика')
                break
