import functions
import time
import os

from cryptography.fernet import Fernet
from json import dump, load
from random import randint
from pytz import UnknownTimeZoneError, timezone


class Register:
    """Класс представляющий регистратор данных, конфигураций, пользователей"""
    def __init__(self):
        """Инициализация путя и название файлов"""
        self.PATH = 'data/'
        self.SETUPS = self.PATH + 'setups.json'
        self.USERS = self.PATH + 'users.json'
        self.BLACKLIST = self.PATH + 'blacklist.json'
        self.CONFIG_AUTH = self.PATH + 'config-auth.json'
        self.CONFIG_BOT = self.PATH + 'config-bot.json'
        self.LOGS = self.PATH + 'logs.txt'

    @staticmethod
    def __get_data_from_console():
        """Получени ID, HASH, PHONE, PASSWORD(не обязательно) с консоли"""
        def get_data(name, status):
            """Получение данных"""
            question = "Пожалуйста, введите %s: " % name.upper()
            while True:
                if status == 0:
                    try:
                        return int(input(question))
                    except ValueError:
                        print("\n - Ваш %s должен быть состоять только из чисел!" % name.upper())
                if status == 1:
                     return input(question)

        def password_handler(password):
            """Проверка пароля на простоту"""
            if password == '':
                return None
            if password == '':
                return None
            if len(password) < 6:
                return None
            else:
                return password

        while True:
            app_id = get_data('id', 0)
            app_hash = get_data('hash', 1)
            user_phone = get_data('phone', 0)

            print("\n{}!ВНИМАНИЕ!"
                  "\n{}Если вы не хотите вводить свой пароль от двухфакторной аутентификации (если есть),"
                  " просто нажмите 'ENTER'!"
                  "\n{}Так же ваш пароль не должен быть короче, чем 6 символов!\n".format(' ' * 43, ' ' * 15, ' ' * 18))

            user_password = get_data('password', 1)
            user_password = password_handler(user_password)
            return app_id, app_hash, user_phone, user_password

    @staticmethod
    def __get_config_data_from_console():
        """Получение конфигурационных данных с консоли"""
        def get_my_id():
            """Получение ID"""
            while True:
                try:
                    return int(input("Введите свой ID в Телеграме: "))
                except ValueError:
                    print("\n- ID должен состоять только из цифер!")

        def get_bot_token():
            """Получение TOKEN'а от Телеграм бота"""
            while True:
                got_token = input("Введите TOKEN вашего Телеграм-бота: ")
                if 40 < len(got_token) < 50:
                    return got_token
                else:
                    print("\n - Не корректный TOKEN!")

        def get_timezone():
            """Получение временного пояса (временной зоны)"""
            while True:
                got_timezone = input("Введите вашу временную зону (Пример: 'Europe/Kiev'): ")
                try:
                    return str(timezone(got_timezone))
                except UnknownTimeZoneError:
                    print("\n - Вы ввели некорректную временную зону! Будет использовано время сервера.\n"
                          "Чтоб попробовать ещё раз, пройдите данную регистрацию заново")
                    return None

        my_id = get_my_id()
        bot_token = get_bot_token()
        bot_id = bot_token[:9]
        timezone_ = get_timezone()
        return my_id, bot_token, bot_id, timezone_

    @staticmethod
    def __get_user_from_console():
        """
        Получение ID и имени пользователя с консоли.
        Данные пользователя, который будет добавлен в список друзей"""
        def get_id():
            """Получение ID пользователя"""
            while True:
                try:
                    uid = int(input("Введите ID пользователя: "))
                    if len(str(uid)) == 9:
                        return uid
                    else:
                        print("\n - ID должен состоять из 9 цифер\n")
                except ValueError:
                    print("\n - ID должен состоять только из цифер!\n")

        def get_user_name():
            """Получение имени пользователя"""
            return input("Введите Имя пользователя: ")

        user_id = get_id()
        user_name = get_user_name()
        return user_id, user_name

    @staticmethod
    def __get_id_for_blocking_from_console():
        """Получение ID пользователя с консоли для добавление его в чёрный список"""
        while True:
            try:
                got_id = int(input("Введите ID пользователя для внесения его в чёрный список: "))
                if len(str(got_id)) != 9:
                    print("\n - Короткий ID!")
                else:
                    return got_id
            except ValueError:
                print("\n - ID должен состоять только из цифер!")

    @staticmethod
    def __registration(status, filename, info):
        """Запись данных в файл формата json"""
        if status == 'w':
            with open(filename, 'w') as file:
                dump(info, file)
        if status == 'rw':
            with open(filename, 'a') as file:
                dump(info, file)

    # Регистрация
    # - данные для входа

    def __registration_data(self):
        """
        Регистрация данных для входа, которые будут использоваться автоответчиком,
        для входа в аккаунт пользователя, для автоматического ответа пользователям.
        Под словом 'Регистрация' имеется ввиду получение пользовательские ID, HASH, PHONE и PASSWORD(не обязательно),
        которые нужны автоответчику для использования и запись этих данных в файл типа json
        """
        def encrypt_and_organize_to_dict(keys, values):
            """Шифровка и сортировка данных"""
            def action(num):
                """Шифровка и сортировка"""
                organized, crypto_keys = {}, []
                i = 0
                while i < num:
                    key = Fernet.generate_key()
                    encrypted_key = Fernet(key).encrypt(str(values[i]).encode('utf-8'))
                    organized[keys[i].upper()] = encrypted_key.decode('utf-8')
                    crypto_keys.append(key.decode('utf-8'))
                    i += 1
                return organized, crypto_keys

            #
            if not values[-1]:
                organized_dictionary, cryptographic_keys_list = action(3)
                return organized_dictionary, cryptographic_keys_list
            else:
                organized_dictionary, cryptographic_keys_list = action(4)
                return organized_dictionary, cryptographic_keys_list

        def generation(to_generate=20):
            """Генерация дополнительных ключей"""
            i = 0
            keys_list = []
            number = randint(to_generate, 100)
            while i < number:
                key = Fernet.generate_key()
                keys_list.append(key.decode('utf-8'))
                i += 1
            return number, keys_list

        def joining_lists(list_from, list_to):
            """Сложение списков"""
            for item in list_from:
                list_to.append(item)
            return list_to

        # получение данных с консоли
        app_id, app_hash, user_phone, user_password = self.__get_data_from_console()

        # шифровка данных и сортировка их в словаре
        dict_keys = ['id', 'hash', 'phone', 'password']
        dict_values = [app_id, app_hash, user_phone, user_password]
        organized_data, cryptographic_keys = encrypt_and_organize_to_dict(dict_keys, dict_values)

        # генерация криптографических ключей
        f_count, f_generated_keys = generation()
        l_count, l_generated_keys = generation(f_count)

        # Слияние двух списков
        appended_list = joining_lists(cryptographic_keys, f_generated_keys)

        finally_list = joining_lists(l_generated_keys, appended_list)

        # добавление идентификаторов
        organized_data['IDN0'] = f_count
        organized_data['IDN1'] = l_count

        # регистрация
        self.__registration('w', self.CONFIG_AUTH, organized_data)
        self.__registration('w', self.SETUPS, finally_list)

        # уведомление
        message = "\n- Успешно зарегистрировано!"
        print(message + "\n")

        # логирование
        functions.logging(message, 'Отсутствует', 'Успешная регистрация данных для входа')
        time.sleep(3)

    # - конфигурации бота

    def __registration_bot_config(self):
        """Регистрация конфигураций: TOKEN'а бота (управляющего), ID, Часового пояса"""
        config = {}

        # получение данных с консоли
        my_id, bot_token, bot_id, my_timezone = self.__get_config_data_from_console()

        # добавление данных
        config['my_ID'] = my_id
        config['TOKEN'] = bot_token
        config['ID'] = int(bot_id)
        config['my_TZ'] = str(my_timezone)

        # регистрация
        self.__registration('w', self.CONFIG_BOT, config)

        # уведомление
        message = "\n - Успешно зарегистрированно!"
        print(message + "\n")

        # логирование
        functions.logging(message, 'Отсутствует', 'Успешная регистрация конфигураций')
        time.sleep(3)

    # Добавление
    # - список друзей

    def __adding_friend(self):
        """Добавление пользователя (друга) в список друзей, который будет использоваться автоответчиком."""
        def load_users():
            """
            Попытка загрузить файл со списком друзей, если он создан и найден.
            Если файл не найден - возвращается словарь, для дальнейшего создания файла со списком друзей
            """
            try:
                with open(self.USERS, 'r') as file:
                    return load(file)
            except FileNotFoundError:
                return {}

        # попытка загрузить файл
        users = load_users()

        # получение ID и Имя пользователя, который будет добавлен в список друзей
        user_id, user_name = self.__get_user_from_console()

        # добавление пользователя
        users[user_name.capitalize()] = user_id

        # регистрация
        self.__registration('w', self.USERS, users)

        # уведомление
        message = "\n- Успешно добавлено!"
        print(message + "\n")

        # логирование
        functions.logging(message, 'Отсутствует', 'Успешное добавление пользователя в список друзей')
        time.sleep(3)

    # - чёрный список

    def __adding_blocked_user(self):
        """Добавление пользователя в чёрный список, который будет использован автоответчиком"""
        def load_blacklist():
            """
            Попытка загрузить файл с чёрным списком, если он создан.
            Если файл не найден, возвращается список для дальнейшего использования в создании файла с чёрным списком
            """
            try:
                with open(self.BLACKLIST) as file:
                    return load(file)
            except FileNotFoundError:
                return []

        # попытка загрузить файл
        blacklist = load_blacklist()

        # получение ID пользователя, который будет добавлен в чёрный список
        user = self.__get_id_for_blocking_from_console()

        # добавление пользователя
        blacklist.append(user)

        # регистрация
        self.__registration('w', self.BLACKLIST, blacklist)

        # уведомление
        message = "\n - Успешно добавлено!"
        print(message + "\n")

        # логирование
        functions.logging(message, 'Отсутствует', 'Успешное добавление пользователя в чёрный список')
        time.sleep(3)

    # Удаление
    # - список друзей

    def __removing_from_user_list(self):
        """Удаление пользователя со списка друзей"""
        def find_key_via_value(uid, got_list):
            """Поиск ключа с помощью значения, для получения пользователя"""
            if type(uid) == int:
                if uid in got_list.values():
                    i = 0
                    for value in got_list.values():
                        if value == uid:
                            return list(got_list.keys())[i]
                        else:
                            i += 1
                else:
                    return None
            else:
                return uid

        def get_user_from_console():
            """Получение данных (ID или Имя) пользователя, который будет удалён со списка друзей"""
            got_user = input("\nВедите ID или имя пользователя, которого хотите удалить: ")
            try:
                got_user = int(got_user)
                if len(str(got_user)) == 9:
                    return got_user
                else:
                    print("\n - ID должен состоять из 9 чисел")
                    return None
            except ValueError:
                return got_user

        def remove_user(user_id, users_list):
            person = find_key_via_value(user_id, users_list)
            if not person:
                print("\n - Пользователь с данным ID не найден!")
            else:
                if person.capitalize() in users_list.keys():
                    del users_list[person.capitalize()]

                    # уведомление
                    message = "\n - Пользователь успешно удалён!"
                    print(message + "\n")

                    # логирование
                    functions.logging('{} Удалён: {}'.format(message, person.capitalize()),
                                      'Отсутствует', 'Успешное удаление пользователя со списка друзей')
                else:
                    print("\n - Пользователь с данным Именем не найден!")
            time.sleep(3)

        while True:
            try:
                user_list = functions.load_data(self.USERS)
            except FileNotFoundError as error:
                message = "\n - Файл не найден"
                print(message + "\n")

                # логирование
                functions.logging(message, error)
                time.sleep(3)
            else:
                user = get_user_from_console()
                if user:
                    # удаление пользователя
                    remove_user(user, user_list)

                    # обновление списка друзей
                    self.__registration('w', self.USERS, user_list)
                    break

    # - чёрный список

    def __removing_from_blacklist(self):
        """Удаление пользователя с чёрного списка"""
        def remove_user(uid, black_list):
            """Удаление пользователя"""
            if uid in black_list:
                black_list.remove(uid)

                # уведомление
                message = "\n - Пользователь успешно удалён!"
                print(message + "\n")

                # логирование
                functions.logging('{} Удалён (ID): {}'.format(message, uid),
                                  'Отсутствует', 'Успешное удаление пользователя с чёрного листа')

            else:
                print("\n - Пользователь с данным ID не найден!\n")
            time.sleep(3)

        def get_id_from_console():
            """Получение ID пользователя с консоли, который будет удалён """
            try:
                got_id = int(input("\nВведите ID пользователя, которого хотите удалить: "))
                if len(str(got_id)) == 9:
                    return got_id
                else:
                    print("\n - ID должен состоять из 9 чисел")
                    return None
            except ValueError:
                print("\n - ID должен состоять только из чисел")

        while True:
            try:
                blacklist = functions.load_data(self.BLACKLIST)
            except FileNotFoundError as error:
                message = "\n - Файл не найден!"
                print(message + "\n")

                functions.logging(message, error)
                time.sleep(3)
            else:
                user_id = get_id_from_console()
                if user_id:

                    # удаление пользователя
                    remove_user(user_id, blacklist)

                    # обновление чёрного списка
                    self.__registration('w', self.BLACKLIST, blacklist)

                    break

    # Запуск

    def run(self):
        """Запуск регистратора"""
        # проверка наличия необходимых файлов, при их остсутствии, файлы создаются автоматически
        if not os.path.exists(self.LOGS):
            functions.creating_file(self.LOGS)

        # отображение меню
        print("\n{} {} {}".format('=' * 15, 'РЕГИСТРАЦИЯ', '=' * 15))
        print("  Чтоб выбрать пункт, введите его номер!\n\n".upper())
        while True:
            menu = "0 - Выход\n" \
                   "\n{0}[РЕГИСТРАЦИЯ]\n" \
                   "1 - Регистрация данных для входа (ID/HASH/PHONE/PASSWORD)\n" \
                   "2 - Регистрация конфигураций\n" \
                   "\n{0}[ДОБАВЛЕНИЕ]\n" \
                   "3 - Добавить польователя в список друзей\n" \
                   "4 - Добавить пользователя в чёрный список\n" \
                   "\n{0}[УДАЛЕНИЕ]\n" \
                   "5 - Удалить пользователя со списка друзей\n" \
                   "6 - Удалить пользователя с чёрного списка\n".format(" " * 15)
            print(menu)
            try:
                chosen = int(input("-> "))
            except ValueError:
                print("\n- Вы должны вводить только числа!")
            else:
                if chosen == 0:
                    print("Работа с регистратором завершена!")
                    break
                if chosen == 1:
                    self.__registration_data()
                if chosen == 2:
                    self.__registration_bot_config()
                if chosen == 3:
                    self.__adding_friend()
                if chosen == 4:
                    self.__adding_blocked_user()
                if chosen == 5:
                    self.__removing_from_user_list()
                if chosen == 6:
                    self.__removing_from_blacklist()


if __name__ == '__main__':
    register = Register()
    register.run()

