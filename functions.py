import json
import platform
import subprocess
import sys
import pytz

from datetime import datetime
from requests.exceptions import ConnectionError, ReadTimeout
from urllib3.exceptions import MaxRetryError, NewConnectionError


def getting_message_via_os():
    """Получение сообщение(в данном случае комманду) в соответсвии с операционной системой"""
    os = platform.system()
    if os == 'Linux':
        return 'python3'
    if os == 'Windows':
        return 'python'


def do_command(command=None, file='register.py'):
    """
    Выполнение комманд.
    В данном случае используется для открытия файл с регистрацией данных для работы программы
    """
    if command:
        subprocess.run([command, file])
    else:
        command = getting_message_via_os()
        subprocess.run([command, file])


def handling_connection_error(function_for_handling):
    """
    Обработка ошибок связанных с подключением сети:
    Отсутствие или не стабильная сеть,
    максимальное количество попыток,
    новое подключение,
    """
    try:
        function_for_handling()
    except (ConnectionError, MaxRetryError, NewConnectionError, TypeError) as error:
        message = "\n - Подключения к сети не стабильно или отсутствует!"
        print(message + "\n")

        logging(message, error)
        logging(' -Бот не был запущен', 'Ошибка описана в предыдущем логе', 'Запуск бота управления автоответчиком')
        sys.exit()
    except TimeoutError as error:
        message = "\n - Тайм-аут"
        print(message + "\n")
        logging(message, error)
        sys.exit()

    else:
        print(" - Бот управления автоответчиком запущен!")


def handling_error(function_for_handling):
    """Обработка основной ошибки: 'Отсутствия необходимых файлов, для работы программы'"""
    try:
        function_for_handling()
    except TypeError as error:
        message = "\nНекорректная работа в связи с незавершёнными действиями!"\
                        "\nПредположительно, вы не завершили регистрацию данных"\
                        "\nПерезапустите программу и зарегестрируйте недостающие данные "\
                        "для корректной работы программы"\
                        " или сперва зарегестрируйте данные, а потом запускайте программу."
        print(message + "\n")

        logging(message, error)
        logging(' -Бот не был запущен', 'Ошибка описана в предыдущем логе', 'Запуск бота управления автоответчиком')
        sys.exit()


def logging(message, error, status='Ошибка'):
    """Логирование"""
    path = 'data/logs.txt'
    timezone = load_data('data/config-bot.json')['my_TZ']
    number = int(get_number_of_log()[1:])

    logged = "\n#{}" \
             "\nСТАТУС: {}" \
             "\nДАТА: {}" \
             "\nСООБЩЕНИЕ: '{}'" \
             "\nОШИБКА: {}" \
             "\n".format(number + 1, status, datetime.now().strftime("%d.%m.%Y - %H:%M:%S"), message[2:], error)

    if timezone:
        logged = "\n#{}" \
                 "\nСТАТУС: {}" \
                 "\nДАТА: {}" \
                 "\nСООБЩЕНИЕ: '{}'" \
                 "\nОШИБКА: {}" \
                 "\n".format(number + 1,
                             status,
                             datetime.now(tz=pytz.timezone(timezone)).strftime("%d.%m.%Y - %H:%M:%S"),
                             message[2:],
                             error)

    write_data('rw', path, logged)


def load_logs():
    with open('data/logs.txt', 'r') as file:
        return file.readlines()[-29:]


def show_logs():
    text = ''
    logs = load_logs()
    for item in logs:
        text += item
    return text


def creating_files(*args):
    """Автоматическое создание нужных для работы программы файлов"""
    files = list(args)
    for filename in files:
        if '.json' in filename:
            with open(filename, 'w') as file:
                json.dump(file, '')
        if '.txt' in filename:
            with open(filename, 'w') as file:
                file.write("")


def creating_file(filename, t_json='', t_txt=''):
    """Автоматическое создание одного файла, требуемого для работы программы"""
    if '.json' in filename:
        with open(filename, 'w') as file:
            json.dump(file, t_json)
    if '.txt' in filename:
        with open(filename, 'a') as file:
            file.write(t_txt)


# - Для управляющего бота


def load_data(filename):
    """Загрузка данных с файла типа json"""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError as error:
        message = "\n - Файл не найден!"
        print(message + "\n")

        logging(message, error)


def get_number_of_log():
    """Получение номера последнего лога"""
    try:
        with open('data/logs.txt', 'r') as file:
            return file.readlines()[-5]
    except IndexError:
        return "#0"


def write_data(status, filename, data=''):
    """Запись данных"""
    if status == 'w':
        with open(filename, 'w') as file:
            file.write(data)
    if status == 'rw':
        with open(filename, 'a') as file:
            file.write(data)


def formatting_dictionary_data(dictionary):
    """Форматирование данных списка друзей, для удобного отображения ботом"""
    text = ""
    i = 1
    for user_name, user_id in dictionary.items():
        text += "\n👤<b>Пользователь №{}</b>\n📃Имя: {}\n🔔ID: {}\n".format(i, user_name, user_id)
        i += 1
    return text


def formatting_list_data(list_):
    """Форматирование чёрного списка, для удобного отображения его ботом"""
    amount = len(list_)
    if amount == 0:
        return "Чёрный список пуст!"
    else:
        text = 'В чёрном списке %s человек\n' % amount
        i = 1
        for item in list_:
            text += "\nID №{}\n{}\n".format(i, item)
            i += 1
        return text


# - Для автоответчика


def formatting_time_answer(got_time, status='s'):
    """ Определение корректного ответа"""
    if got_time in range(11, 15):
        f_time = int(str(got_time)[-2:])
    else:
        f_time = int(str(got_time)[-1])

    seconds = ['секунда', 'секунды', 'секунд']
    minutes = ['минута', 'минуты', 'минут']
    hours = ['час', 'часа', 'часов']
    days = ['день', 'дня', 'дней']

    def handling(item, g_time):
        """Обработка"""
        if g_time == 1:
            return item[0]
        if g_time in range(2, 5):
            return item[1]
        if g_time in range(11, 15):
            return item[2]
        else:
            return item[2]

    if status == 's':
        result = handling(seconds, f_time)
        return "{} {}".format(got_time, result)
    if status == 'm':
        result = handling(minutes, f_time)
        return "{} {}".format(got_time, result)
    if status == 'h':
        result = handling(hours, f_time)
        return "{} {}".format(got_time, result)
    if status == 'd':
        result = handling(days, f_time)
        return "{} {}".format(got_time, result)


def flood_wait_error(error_time):
    """Определение времени ожидания"""
    if error_time < 60:
        return formatting_time_answer(error_time, 's')
    if 60 < error_time < 3600:
        error_time = error_time // 60
        return formatting_time_answer(error_time, 'm')
    if 3600 < error_time < 86400:
        error_time = error_time // 60 // 60
        return formatting_time_answer(error_time, 'h')
    if 86400 <= error_time:
        error_time = error_time // 60 // 60 // 24
        return formatting_time_answer(error_time, 'd')


