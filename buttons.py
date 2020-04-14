from telebot import types


def main_menu():
    """Главное меню (закреплённое снизу"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_bot_management = types.KeyboardButton('Управление автоответчиком🎮')
    button_registration = types.KeyboardButton('Регистрация⚙️')
    button_help = types.KeyboardButton('Помощь🔔')
    markup.add(button_bot_management, button_registration, button_help)
    return markup


def bot_management():
    """Меню раздела 'Управление автоответчиком'"""
    markup = types.InlineKeyboardMarkup()
    button_activity = types.InlineKeyboardButton(text='🕹', callback_data='set_activity')
    button_status = types.InlineKeyboardButton(text='💡', callback_data='get_status')
    button_mode = types.InlineKeyboardButton(text='🎛', callback_data='set_mode')
    button_session = types.InlineKeyboardButton(text='📰', callback_data='get_session_name')
    button_full_info = types.InlineKeyboardButton(text='🖥', callback_data='show_all_info')
    markup.add(button_activity, button_status, button_mode, button_session, button_full_info)
    return markup


def registration_data():
    """Меню раздела 'Регистрация'"""
    markup = types.InlineKeyboardMarkup()
    button_registration_data = types.InlineKeyboardButton(text='1️⃣',
                                                          callback_data='registration_data')
    button_registration_user = types.InlineKeyboardButton(text='2️⃣',
                                                          callback_data='registration_user')
    button_registration_to_blacklist = types.InlineKeyboardButton(text='3️⃣',
                                                                  callback_data='registration_to_blacklist')
    button_show_registered_users = types.InlineKeyboardButton(text='4️⃣',
                                                              callback_data='get_registered_users')
    button_show_blocked_users = types.InlineKeyboardButton(text='5️⃣',
                                                           callback_data='get_blocked_users')
    markup.add(button_registration_data, button_registration_user, button_registration_to_blacklist,
               button_show_registered_users, button_show_blocked_users)
    return markup


def help_section():
    """Меню раздела 'Помощь'"""
    markup = types.InlineKeyboardMarkup()
    button_faq = types.InlineKeyboardButton(text='📚', callback_data='help_faq')
    button_logs = types.InlineKeyboardButton(text='📝', callback_data='help_logs')
    button_documentation = types.InlineKeyboardButton(text='📄', callback_data='help_documentation')
    button_communication = types.InlineKeyboardButton(text='📨', callback_data='help_communication')
    markup.add(button_faq, button_documentation, button_communication, button_logs)
    return markup
