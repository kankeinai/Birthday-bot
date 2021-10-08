from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

quest = CallbackData("quest", "action")

start = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=False)
start.add(KeyboardButton('Начать'))
start.add(KeyboardButton('Правила'))


cont = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=False)
cont.add(KeyboardButton('Продолжить'))
cont.add(KeyboardButton('Правила'))

test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да",
                                 callback_data = quest.new(action = "new_game")),
            InlineKeyboardButton(text="Нет",
                                 callback_data = quest.new(action = "bye"))
        ]
    ]
)

choice = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=False)
choice.add(KeyboardButton('Угадать'))
choice.add(KeyboardButton('Задать вопросы'))
choice.add(KeyboardButton('Камень, ножницы, бумага'))

end = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True)
end.add(KeyboardButton('Спасибо за игру'))

answer = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=False)
answer.add(KeyboardButton('Да'))
answer.add(KeyboardButton('Нет'))

new_q = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True)
new_q.add(KeyboardButton('Новый вопрос'))
new_q.add(KeyboardButton('Сдаться'))