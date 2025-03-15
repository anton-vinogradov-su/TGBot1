from aiogram import types

button_1 = types.KeyboardButton(text='/start')
button_2 = types.KeyboardButton(text='/fox')
button_3 = types.KeyboardButton(text='/chatgpt')
button_4 = types.KeyboardButton(text='/random')
button_5 = types.KeyboardButton(text='/talk')
button_6 = types.KeyboardButton(text='/quiz')
# button_6 = types.KeyboardButton(text='/prof')


keyboard_1 = [
    [button_1, button_2],
    [button_3, button_4],
    [button_5, button_6],
]

keyboard_2 = [
    [button_1, button_2, button_3, button_4],
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)
kb2 = types.ReplyKeyboardMarkup(keyboard=keyboard_2, resize_keyboard=True)
