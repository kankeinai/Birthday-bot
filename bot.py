if __name__ == '__main__':
    from handlers import dp
    from aiogram import executor
    from config import mycursor, mydb
    from my_db import create_base, create_table
    
    create_base(mydb, mycursor) 
    create_table(mydb, mycursor)
    
    executor.start_polling(dp)