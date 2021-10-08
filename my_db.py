
def create_base(mydb, mycursor):
    try:
        sql = 'CREATE DATABASE bd_quest'
        mycursor.execute(sql)
    except:
        print("База данных существует")

def create_table(mydb, mycursor):
    sql = """CREATE TABLE IF NOT EXISTS users(
                user_id INT PRIMARY KEY,
                user_name TEXT,
                points INT,
                password TEXT,
                active BOOL,
                new_game BOOL
            );
        """
    mycursor.execute(sql)
    mydb.commit()