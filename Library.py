import sqlite3

db = sqlite3.connect("lib.db")
cursor = db.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS library (
    id INT NOT NULL,
    date DATE,
    number INTEGER,
    name VARCHAR(100), 
    author VARCHAR(100),
    datee DATE,
    price INTEGER,
    dateee INTEGER
    ) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS State (
lib_id INT NOT NULL,
in_lib BOOLEAN NOT NULL,
stud BOOLEAN NOT NULL,
sp BOOLEAN NOT NULL,
lost INT NOT NULL,
FOREIGN KEY(lib_id) REFERENCES library (id));
    """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Category (
lib_id INT NOT NULL, 
uch INT NOT NULL,
hud INT NOT NULL,
pol INT NOT NULL,
ec INT NOT NULL,
en INT NOT NULL,
na INT NOT NULL,
fil INT NOT NULL,
med INT NOT NULL,
istor INT NOT NULL,
npop INT NOT NULL,
urid INT NOT NULL,
FOREIGN KEY(lib_id) REFERENCES library (id));""")





def fill():

    print('Сколько книг хотите вписать?')
    a = int(input())
    for i in range(a):
        date = input('Дата: ')
        number = input('Инвентарный номер или ISBN: ')
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

def kolvoknig():
    a = cursor.execute("SELECT COUNT(*) FROM library")
    print(a)

def delete():
    b = input('Введите название книги(ее номер или ISBN), которую хотите удалить из библиотеки: ')
    a = cursor.execute("DELETE FROM library where name like '%{0}%' or number like '%{0}%' ".format(b))
    print(a)
    rer()

def ab():
    for value in cursor.execute("SELECT * FROM library"):
        print(value)
    rer()


def poiskpoinnomeru():
    cursor.execute("""DROP TABLE IF EXISTS vrem """)
    cursor.execute(""" CREATE TABLE vrem (
                    inventnum INTEGER)
                """)

    aut = input('Введите автора, название, инвентаризационный номер или ISBN: ')
    sr = cursor.execute("SELECT * FROM library where name like '%{0}%' or author like '%{0}%' or number like '%{0}%'".format(aut)).fetchall()

    print(sr)
    rer()




def rer():
    print ('список команд:'
    '\n1) Заполнить базу книгами '
    '\n2) Вывести список всех книг '
    '\n3) Поиск книг по базе '
    '\n4) Количество книг в библиотеке'
    '\n5) Удалить книгу из библиотеки')

    m = int(input("Введите номер: "))

    if m == 1:
        fill()
    elif m == 2:
        ab()
    elif m == 3:
        poiskpoinnomeru()
    elif m == 4:
        kolvoknig()
    elif m == 5:
       delete()
    else:
        print('не написана пока эта команда')
rer()