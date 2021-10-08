from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import message
from aiogram.types.callback_query import CallbackQuery

from loader import dp, bot
from time import sleep
from random import randint
from keybords import start, test, quest, cont, choice, end, answer, new_q


from config import mydb, mycursor, QUEST, PASS, START, RULES, GUESER, QUESTIONS, END_PHRASES, STICKERS 

class my_state(StatesGroup):
    login = State()
    send = State()
    accept = State()
    password = State()
    choice = State()
    judge = State()
    question = State()
    give_points = State()
    test = State()
    rules = State()
    answer = State()
    
admin_id  = 658415666
player_id = admin_id #temporary


#BOT DIALOGS SETTINGS
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
quest_names = QUEST.copy()
end_p = END_PHRASES.copy()
stick = STICKERS.copy()
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  



# START 
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['yes_no'] = False
    global quest_names, end_p, stick 
    quest_names = QUEST.copy() 
    end_p = END_PHRASES.copy()
    stick = STICKERS.copy()
    if (message.from_user.id == admin_id):
        await message.answer("C возвращением сенсей! Чтобы войти введите пароль:")
        await my_state.login.set()
    else:
        await message.answer("Привет!")
        await message.answer_sticker(r'CAACAgEAAxkBAAEBG0tfHq7a9x7k7JLAcBVg0oeBetR3WQACwCIAAnj8xgWCnglbp1nzEhoE')
        for str in START:
            sleep(2)
            await message.answer(str)
        await my_state.login.set()
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––         



# AUTHORIZATION 
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(state = my_state.login)
async def process_password(message: types.Message, state: FSMContext):
    mycursor.execute(f"SELECT * FROM users where user_id={message.from_user.id}")
    result = mycursor.fetchone()
    user =  (message.from_user.id, message.from_user.first_name, 0, "HappyBirthday", False, True)
    if not result:
        mycursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", user)
        mydb.commit()   
    print(user)
    mycursor.execute(f"SELECT password FROM users where user_id={message.from_user.id}")
    result = mycursor.fetchone()[0]
    password = message.text
    
    if password == result:
        global player_id
        player_id =message.from_user.id
        await state.finish()  
        if message.from_user.id != admin_id:
            await message.answer(f"{user[1]}, ты успешно справился! Теперь можно начать игру", reply_markup = start)
        else:
            await message.answer("Вы всегда можете сменить пароль командой /pass")
            await message.answer("Хотите провести тест квеста?", reply_markup = test)    
    else:
        await message.answer(PASS[randint(0,len(PASS)-1)])   
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   



# ADMIN ACCEPT GAME ABILITY       
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   

@dp.callback_query_handler(quest.filter(action="new_game"))       
async def admin_start_quest(call: CallbackQuery, state: FSMContext):
    global player_id
    player_id = admin_id
    await bot.send_message(player_id, "Сенсей вы лучший! Можете начинать:", reply_markup = start)   
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   


           
# ADMIN CHANGE PASSWORD ABILITY
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(commands=['pass'])
async def process_send_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer(text="Введите новый пароль") 
        await my_state.password.set()
    else:
       await message.answer(text="Нет доступа")   
        
@dp.message_handler(state = my_state.password)
async def admin_inform(message: types.Message, state: FSMContext):
    new_pass = message.text
    mycursor.execute(f"""UPDATE users set password = '{new_pass}'""")
    mydb.commit()
    await message.answer("Пароль успешно изменен")
    await state.finish()
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
               
               
               
# ADMIN SEND MESSAGES ABILITY
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(commands=['send'])
async def process_send_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer(text="Введите текст пиcьма", reply_markup = answer) 
        await my_state.send.set()
    else:
       await message.answer(text="Нет доступа")  
    

@dp.message_handler(state = my_state.send)
async def admin_inform(message: types.Message, state: FSMContext):
    await bot.send_message(player_id, "Семпай-чан: "+ message.text, reply_markup = new_q)   
    mycursor.execute(f"""UPDATE users set active = True where user_id = {player_id}""")
    mydb.commit()
    await state.finish()    
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
   
   
    
#ADMIN PAPER SCISSORS ROCK
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(commands=['psr'])
async def process_psr_command(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await message.answer(text="Выиграл?", reply_markup = answer)
        async with state.proxy() as data:
            data['points'] = 5
        await my_state.judge.set()
    else:
       await message.answer(text="Нет доступа")  
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––    



#ADMIN GUESSER    
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––      
@dp.message_handler(commands=['guess'])
async def process_guess_command(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await message.answer(text="Угадал?", reply_markup = answer)
        async with state.proxy() as data:
            data['points'] = 20
        await my_state.judge.set()
    else:
       await message.answer(text="Нет доступа")  
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– 


#ADMIN YES/NO   
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––     
@dp.message_handler(commands=['quest'])
async def process_guest_command(message: types.Message, state: FSMContext):
    mycursor.execute(f"""UPDATE users set active = False where user_id = {player_id}""")
    mydb.commit()
    if message.from_user.id == admin_id:
        await bot.send_message(admin_id, "Введите нужное число баллов")
        await my_state.give_points.set()
    else:
       await message.answer(text="Нет доступа")    
       
@dp.message_handler(state = my_state.give_points)
async def if_points_given(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = int(message.text)
        await message.answer(text="Присудить баллы?", reply_markup = answer)
        await my_state.judge.set()
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––     


    
#END GAME FUNCTION    
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(state = my_state.judge)
async def points_giver_func(message: types.Message, state: FSMContext):
    mycursor.execute(f"""UPDATE users set new_game = True where user_id = {player_id}""")
    mydb.commit()
    
    mycursor.execute(f"Select points from users where user_id = {player_id}")
    cur_points = mycursor.fetchone()[0]
    async with state.proxy() as data:
        if message.text == 'Да' and data['points']>0:
            mycursor.execute(f"Select points from users where user_id = {player_id}")
            cur_points+=data['points']
            await bot.send_message(player_id, f"Ты выиграл и получаешь {data['points']} баллов. Текущий счет: {cur_points}", reply_markup = cont)
            mycursor.execute(f"UPDATE users set points = {cur_points} where user_id = {player_id}")
            mydb.commit()
            try:
                await bot.send_message(player_id, end_p.pop(0))
            except:
                pass
            
        else:
            await bot.send_message(player_id, f"Ты проиграл и твой счет не изменился. Текущий счет: {cur_points}", reply_markup = cont)
            try:
                end_p.pop(0)
            except:
                pass
    
    await state.finish()
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––            
    
@dp.message_handler(text = "Продолжить")
@dp.message_handler(text = "Начать")
async def points_giver_func(message: types.Message, state: FSMContext):
    mycursor.execute(f"Select new_game from users where user_id = {message.from_user.id}")
    result = mycursor.fetchone()[0]
    print(result)
    if result == True:
        global quest_names 
        if len(quest_names)==5:
            mycursor.execute(f"UPDATE users set points = 0 where user_id = {message.from_user.id}")
            mydb.commit()
            mycursor.execute(f"Select user_name from users where user_id = {message.from_user.id}")
            result = mycursor.fetchone()[0]
            await bot.send_message(admin_id, f"{result} начал квест")
        if len(quest_names)>0:
            try:
                await bot.send_sticker(message.from_user.id, stick.pop(0))
            except:
                pass
            for msg in quest_names.pop(0):
                await bot.send_message(message.from_user.id, text = msg)
                sleep(0.5)
            await bot.send_message(message.from_user.id, text = "Выбери действие в меню:", reply_markup = choice)
            await my_state.choice.set()
        else:
            mycursor.execute(f"Select points from users where user_id = {message.from_user.id}")
            result = mycursor.fetchone()[0]
            print(quest_names)
            await bot.send_message(message.from_user.id, text=f"Игра закончена! Твоя удача {result}%", reply_markup=end)  
            await state.finish() 
        
# START OF QUEST  
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––     
        
@dp.message_handler(state = my_state.choice)
async def game_choicer(message: types.Message, state: FSMContext):
    mycursor.execute(f"UPDATE users set new_game = False where user_id = {player_id}")
    mydb.commit()
    if message.text == "Камень, ножницы, бумага":
        await message.answer("Начинайте игру")
        await bot.send_message(admin_id, f"{message.from_user.first_name} начал играть в \"Камень, ножницы, бумагу\".\nСообщите о результатах воспользовавшись командой /psr")
        await state.finish()
    
    elif message.text == "Угадать":
        await bot.send_message(admin_id, f"{message.from_user.first_name} начал играть в \"Угадайку\"")
        await message.answer("Напиши свой вариант:")
        await my_state.answer.set() 
    
    elif message.text == "Задать вопросы":
        mycursor.execute(f"""UPDATE users set active = True where user_id = {message.from_user.id}""")
        mydb.commit()
        await bot.send_message(admin_id, f"{message.from_user.first_name} решил позадавать вопросы")
        await message.answer("Задавай свой вопрос:")
        await my_state.question.set()
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––           


#GUESER USER ABILITY
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(state = my_state.answer)
async def check_answer(message: types.Message, state: FSMContext):
    await message.answer(GUESER[randint(0, len(GUESER)-1)])
    await bot.send_message(admin_id, f"{message.from_user.first_name} думает, что это:\n\"{message.text}\"\nВведите /guess и скажите верно или нет")
    await state.finish()
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   



#YES/NO USER ABILITY  
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
@dp.message_handler(state = my_state.question)    
async def quiz_starter(message: types.Message, state: FSMContext):
    q = message.text
    await message.answer(QUESTIONS[randint(0,len(QUESTIONS)-1)])
    await bot.send_message(admin_id, f"{message.from_user.first_name} спросил:\n\"{q}\".\nВведите /send чтобы ответить.\nВведите /quest если игрок угадал")
    mycursor.execute(f"""UPDATE users set active = False where user_id = {message.from_user.id}""")
    mydb.commit()
    await state.finish()   
    
@dp.message_handler(text="Новый вопрос")
async def ask_new_question(message: types.Message, state: FSMContext):
    mycursor.execute(f"""Select active from users where user_id={message.from_user.id}""")
    result = mycursor.fetchone()[0]
    if result:
        await message.answer("Введите вопрос:")
        await my_state.question.set()
    
@dp.message_handler(text="Сдаться")
async def accept_defeat(message: types.Message, state: FSMContext):
    mycursor.execute(f"""Select active from users where user_id={message.from_user.id}""")
    result = mycursor.fetchone()[0]
    if result:
        await bot.send_message(admin_id, f"{message.from_user.first_name} хочет сдаться /quest")
        mycursor.execute(f"""UPDATE users set active = False where user_id = {message.from_user.id}""")
        mydb.commit()
    
 #–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   
 
 
 
# USER/ADMIN ABILITIES 
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––    
@dp.message_handler(text="Спасибо за игру")
@dp.message_handler(commands=['end'])
@dp.callback_query_handler(quest.filter(action="bye"))
async def end_quest(message: types.Message):
    global quest_names
    global end_p
    global stick
    quest_names = QUEST.copy()
    end_p = END_PHRASES.copy()
    stick = STICKERS.copy()
    mycursor.execute(f"""UPDATE users set new_game =  False where user_id = {player_id}""")
    mydb.commit()
    await message.answer("И тебе спасибо за приятное время!")     

#–––
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

@dp.message_handler(text = "Правила")
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(text = "Правила:\n")  
    await message.answer(text = RULES )  