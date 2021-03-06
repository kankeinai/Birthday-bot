import os
import dotenv

START = ["Меня зовут Cемпай-чан и я приготовила для тебя пару подарков, но их не получить просто так!",
         "Перед тем как мы начнем, попробуй найти какие-нибудь полезные вещи или зацепки в переднем и боковых карманах.",
         "Среди них есть шифр. Тебе нужно решить его и ввести сюда, чтобы начать:"]
QUEST = [
        ["Так как это твое первое испытание, я буду чуть детальнее", 
        "Вначале ты должен был найти некоторые инструменты и подсказки. Возможно они могут как-то пригодиться, особенно если вспомнить правила",
        "Думаю нет смысла проверять передний карман, ты же там уже все нашел или нет?",
        "Задание: проверить карман тщательнее если все еще не нашел и догадаться что это"], 
        ["Семпай-чан гордится тобой :з",
         "Думаю первый предмет был довольно легким, учитывая что не все можно поместить в такой плоский конверт.",
         "Теперь все будет немного сложнее, ведь пора открывать средний карман!", "Что же там? Два... Давай выберем тот что поменьше",  ], 
        ["Ты еще не устал?", "Терпи, я же тебе тут подарки раздаю :p",
         "Теперь можно и со вторым разобраться, он такой большой", 
            ], 
        [ "Ты почти закончил!", "Пора заглянуть в карман для ноутбука", "Что же там?", "Думаю тебе это точно пригодится"],
        ["Так, больше подсказок не будет!", "Пускай это испытание будет самым сложным", "Ищи внимательнее :з"]
        ]
STICKERS = [r'CAACAgEAAxkBAAECoH5g_B7_JP-TPrSfX_4-woJzwN536QACviIAAnj8xgXlUHBREO72ZCAE', 
            r'CAACAgEAAxkBAAECoIBg_B8TwM2HP6oUuR5GiHG27AbSZwACuiIAAnj8xgXAcxWeRGOe3SAE',
            r'CAACAgEAAxkBAAECoIJg_B9g709-Mbzgn7QHgEFxxfPSWAACuyIAAnj8xgUXSvngAAG7tXsgBA',
            r'CAACAgEAAxkBAAECoIRg_B-v1U1kYr2nhNEC1gR_m105_QACvSIAAnj8xgVcziBWXaPv5iAE',
            r'CAACAgEAAxkBAAECoIZg_B_ALX3ZHVeJ4a9iVPuVVDFQqAACvyIAAnj8xgUFN31pn88_jSAE'
            ]
END_PHRASES = [
        "А кохай очень догадливый, ловко справился и ноут станет поярче",
        "Я знаю, что ты бы сам его не купил :p попробуй хоть для разнообразия",
        "Я официально признаю тебя корги повелителем!",
        "Теперь лапки всегда будут в тепле",
        "Ну же открой, что там написано?"
    ]

GUESER = ["Неплохой вариант, погоди", "Точно уверен?", "А ты не передумал?", 
          "Ну наверно твой вариант имеет смысл", "Я спрошу у сенсея, погоди"]

QUESTIONS = ["Мне нужно спросить у знакомой", "Дай мне секундочку подумать", "Ну если подумать, скорее...", 
              "Какой каверзный вопрос однако", "Я передам этот вопрос сенсею-сама",
             "Слишком сложно"]

PASS = ["Нельзя просто так его угадать", "Подсказка: Шифр Цезаря", "Думаешь это так просто?", 
        "Ты точно уверен, что нашел тот шифр?","Внимательно проверь написание", 
        "Когда-нибудь ты точно справишься, надеюсь", "Неправильный пароль"]

if os.path.isfile(".env"):
    dotenv.load_dotenv(".env")
    
    # UPDATE secret key
TOKEN = os.environ['TOKEN'] # Instead of your actual secret key


RULES = "Тебе предстоит угадать что это за подарки. Это можно сделать несколькими способами.\n\
    1. Можно сразу попробовать дать ответ, тогда ты получишь 20 очков если угадаешь и 0 если нет.\n\
    2. Сыграть в игру да/нет, где можно задавать наводящие вопросы. Aдмин дает число баллов по своему усмотрению (макс 20).\n \
    3. Cыграть в камень ножницы бумага. Если выиграешь 2/3 получишь 5 баллов и я скажу что внутри. Если проиграешь, получишь 0 баллов.\n\
    Всего можно получить 100 баллов. В конце ты узнаешь свой perfomance и насколько ты удачливый.\n\
    Примечание: Запрещено трогать нитки руками или рвать бумагу.\n\
    Остальные правила можно будет понять в процессе игры."
import sqlite3 
mydb = sqlite3.connect("bd_quest.db")
mycursor = mydb.cursor()