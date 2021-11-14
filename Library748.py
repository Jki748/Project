import sqlite3

db = sqlite3.connect("lib.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS library (
    date DATE,
    number INTEGER,
    name VARCHAR(100), 
    author VARCHAR(100),
    datee DATE,
    price INTEGER,
    dateee INTEGER
    ) """)



def fill():

    print('Сколько книг хотите вписать?')
    a = int(input())
    for i in range(a):
        date = input('Дата: ')
        number = input('Инвентарный номер: ')
        name = input('Название: ')
        author = input('Автор: ')
        datee = input('Год выпуска: ')
        price = input ('Цена: ')
        dateee = input('Дата списания: ')

        if cursor.fetchone() is None:
            cursor.execute("INSERT OR IGNORE INTO library (date, number, name, author, datee, price, dateee ) VALUES (?, ?, ?, ?, ?, ?, ?)", (date, number, name, author, datee, price, dateee))
            db.commit()
            print("Записано"
                  "\n"
                  )
        else:
            print("Такая запись уже имеется")
    rer()

def ab():
    for value in cursor.execute("SELECT * FROM library"):
        print(value)
    rer()





#
# def choto():
#
#     def pn():
#         cursor.execute("""DROP TABLE IF EXISTS vrem """)
#
#         cursor.execute("""CREATE TABLE IF NOT EXISTS vrem (
#                         nomer INTEGER ) """)
#
#
#         nomer = input('Инвентарный номер: ')
#
#         if cursor.fetchone() is None:
#             cursor.execute("INSERT OR IGNORE INTO vrem (nomer) VALUES (?)", (nomer))
#             db.commit()
#         else:
#             pass
#
#
#         qw = cursor.execute("SELECT name FROM library WHERE number == '1234567' ").fetchone()
#         print(qw)
#
#
#     print('Как будем искать?'
#           '\n1) По инвентаризационному номеру '
#           '\n2) '
#           '\n3) ')
#
#     r = int(input("Введите номер: "))
#
#     if r == 1:
#         pn()











def rer():
    print ('список команд:'
    '\n1) Заполнить базу книгами '
    '\n2) Вывести список всех книг '
    '\n3) Поиск книг по базе '
    '\n4) Что-то еще')

    m = int(input("Введите номер: "))

    if m == 1:
        fill()
    elif m == 2:
        ab()
    elif m == 3:
        # choto()
        print('не написана пока эта команда')
    else:
        print('не написана пока эта команда')
rer()