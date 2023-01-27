import sqlite3
from api.utils import Register
from datetime import datetime

connection = sqlite3.connect('quize.db')
sql = connection.cursor()


sql.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_phone_number TEXT,'
            'username TEXT, reg_date DATETIME);')

sql.execute('CREATE TABLE IF NOT EXISTS questions(question_id INTEGER PRIMARY KEY AUTOINCREMENT, main_question TEXT,'
            'variant_1 TEXT,variant_2 TEXT,variant_3 TEXT,variant_4 TEXT,correct_answer TEXT,q_type TEXT,q_set TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS user_answer(user_id INTEGER,question_id INTEGER,answer TEXT,correctness BOOLEAN);')

sql.execute('CREATE TABLE IF NOT EXISTS user_statistic(user_id INTEGER,stat INTEGER,level TEXT,q_set TEXT,date DATETIME);')



# print leaders table

def get_table_of_leaders(level = None):
    connection = sqlite3.connect('quize.db')
    sql = connection.cursor()

    if not level:
        results = sql.execute('SELECT users.username,user_statistic.stat FROM users INNER JOIN user_statistic '
                              'ORDER BY user_statistic.stat DESC LIMIT(5);')

        return results.fetchall()

    results = sql.execute('SELECT users.username,user_statistic.stat FROM users INNER JOIN user_statistic '
                              'WHERE user_statistic.q_set=? ORDER BY user_statistic.stat DESC LIMIT(5);',(level,))
    return results.fetchall()


# User registration or id
def register_or_get_user_id(user:Register):
    connection = sqlite3.connect('quize.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT user_id FROM users WHERE user_phone_number=?',(user.phone_number,)).fetchone()

    if checker:
        return checker
    else:
        sql.execute('INSERT INTO users (user_phone_number,username,reg_date) VALUES(?,?,?);',(user.phone_number,user.name,datetime.now()))
        connection.commit()
        return register_or_get_user_id(user)


# Get questions
def get_guestions(level:str,q_set:str):
    connection = sqlite3.connect('quize.db')
    sql = connection.cursor()

    questions = sql.execute('SELECT * FROM questions WHERE q_type = ? AND q_set=?;',(level,q_set))

    return questions.fetchall()


# Check user_answer

def check_answer(q_id:int,user_id:int,user_answer:str):
    connection = sqlite3.connect('quize.db')
    sql = connection.cursor()
    question_answer = sql.execute('SELECT correct_answer FROM questions WHERE question_id=?;',(q_id,)).fetchone()
    sql.execute('INSERT INTO user_answer VALUES(?,?,?,?);',(user_id,q_id,question_answer[0],1 if question_answer[0]==user_answer else 0 ))
    connection.commit()
    status = 1 if question_answer[0]==user_answer else 0
    return status


# Test Completing
def test_complete_get_positions(user_id:int,corrects:int,level:str,q_set:str):
    connection = sqlite3.connect('quize.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO user_statistic VALUES(?,?,?,?,?);',(user_id,corrects,level,q_set,datetime.now()))
    connection.commit()

    position  = sql.execute('SELECT user_id FROM user_statistic ORDER BY DESC;').fetchall()
    return position.index((user_id,))+1