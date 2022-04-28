import sqlite3
from tkinter import ttk
import tkinter as tk
from tkinter import *
from datetime import datetime

class Library_db():
    def __init__(self):
        self.db = sqlite3.connect("lib.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            number INTEGER,
            name VARCHAR(100), 
            author VARCHAR(100),
            datee DATE,
            price INTEGER,
            dateee DATE,
            izd VARCHAR(100)
            ) """)


        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Inv (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inv_num INTEGER
                    ) """)

    def create(self, date, number, name, author, datee, price, dateee, izd):
        self.cursor.execute(
            "INSERT OR IGNORE INTO library (date, number, name, author, datee, price, dateee, izd) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (date, number, name, author, datee, price, dateee, izd))
        self.db.commit()


    def list(self):
        for value in self.cursor.execute("SELECT * FROM library"):
            print(value)



    def delete_sec_table(self):
        self.cursor.execute("""DROP TABLE Inv""")
        self.db.commit()


class App:
    frames = []

    def frames_clear(self):
        for i in self.frames:
            i.destroy()

    def __init__(self):
        self.library = Library_db()
        self.window = Tk()
        self.window.geometry('850x370')
        self. window.title("A'books")
        self.menu()


        self.window.mainloop()

    def menu(self):
        mainmenu = Menu(self.window)
        self.window.config(menu=mainmenu)
        mainmenu.add_command(label='Создать книгу', command=self.fill)
        mainmenu.add_command(label='Список всех книг', command=self.all_books)
        mainmenu.add_command(label='Поиск книг по автору', command=self.search_book)
        mainmenu.add_command(label='Поиск книг по номеру', command=self.search_book_n)
        mainmenu.add_command(label='Список потерянных книг', command=self.spisok)


    def spisok(self):
        self.frames_clear()

        frame_fill_1 = tk.Frame()
        self.frames.append(frame_fill_1)

        def add_to_Inv():
            inv_num = num_entry.get()
            self.library.cursor.execute("INSERT OR IGNORE INTO Inv (inv_num) VALUES (?)", (inv_num,))
            self.library.db.commit()


        def list_lost_books():
            self.library.cursor.execute("")
            for i in tree.get_children():
                tree.delete(i)
            rows=self.library.cursor.execute(
                "select * from library left outer join Inv on library.number = Inv.inv_num where Inv.inv_num is NULL and library.izd = ''").fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
            self.library.db.commit()

        def spisat():
            num_akta = num_akta_entry.get()
            year = datetime.today().date()
            sql1 = "update library set izd = {0}, dateee = datetime('now') where library.id in (select library.id from library left outer join Inv on library.number = Inv.inv_num where Inv.inv_num is NULL and library.izd = '')".format(num_akta, year)
            self.library.cursor.execute(sql1)
            self.library.db.commit()
            delete_spisok()

        def delete_spisok():
            self.library.cursor.execute("DROP TABLE Inv")
            self.library.db.commit()

        tree = ttk.Treeview(master=frame_fill_1, column=(
        "column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "coloumn9"),
                            show='headings')
        tree.heading("#1", text="id")
        tree.heading("#2", text="дата")
        tree.heading("#3", text="инвентарный номер")
        tree.heading("#4", text="название")
        tree.heading("#5", text="автор")
        tree.heading("#6", text="год выпуска")
        tree.heading("#7", text="цена")
        tree.heading("#8", text="дата списания")
        tree.heading("#9", text="номер акта списания")

        tree.column("#1", width=3)
        tree.column("#2", width=80)
        tree.column("#3", width=109)
        tree.column("#4", width=150)
        tree.column("#5", width=100)
        tree.column("#6", width=100)
        tree.column("#7", width=50)
        tree.column("#8", width=118)
        tree.column("#9", width=129)

        tree.grid()

        inv_num = StringVar()
        num_lab = Label(master=frame_fill_1, text="Введите инвентарный номер:")
        num_lab.grid(sticky="w")
        num_entry = Entry(master=frame_fill_1, textvariable=inv_num)
        num_entry.grid(sticky="w")

        button = Button(master=frame_fill_1, text="Добавить в список", command=add_to_Inv)
        button.grid(sticky="w")

        button2 = Button(master=frame_fill_1, text="Показать список утерянных книг", command=list_lost_books)
        button2.grid(sticky="w")


        num_akta = StringVar()
        num_akta_lab = Label(master=frame_fill_1, text="Введите номер акта списания:")
        num_akta_lab.grid(sticky="w")
        num_akta_entry = Entry(master=frame_fill_1, textvariable=num_akta)
        num_akta_entry.grid(sticky="w")

        button3 = Button(master=frame_fill_1, text="Списать утерянные", command=spisat)
        button3.grid(sticky="w")

        frame_fill_1.pack()


    def fill(self):
        self.frames_clear()
        def save():
            self.library.create(date.get(), number.get(), name.get(), author.get(), datee.get(), price.get(),
                                dateee.get(), izd.get())
            save.config(text="Сохранено")

        date = StringVar()
        number = StringVar()
        name = StringVar()
        author = StringVar()
        datee = StringVar()
        price = StringVar()
        dateee = StringVar()
        izd = StringVar()

        frame_fill = tk.Frame()
        self.frames.append(frame_fill)

        btn = Button(master=frame_fill, text="Сохранить", command=save)
        btn.grid(row=15, column=4, sticky="w")

        lb = Label(master=frame_fill, text="")
        lb.grid(row=14, column=4, sticky="w")

        save = Label(master=frame_fill, text="")
        save.grid(row=30, column=4, sticky="w")

        date_label = Label(master=frame_fill, text="Дата:")
        number_label = Label(master=frame_fill, text="Инвентарный номер:")
        name_label = Label(master=frame_fill, text="Название:")
        author_label = Label(master=frame_fill, text="Автор:")
        datee_label = Label(master=frame_fill, text="Год выпуска:")
        price_label = Label(master=frame_fill, text="Цена:")
        dateee_label = Label(master=frame_fill, text="Дата списания:")
        izd_label = Label(master=frame_fill, text="Номер акта списания:")

        date_entry = Entry(master=frame_fill, textvariable=date)
        number_entry = Entry(master=frame_fill, textvariable=number)
        name_entry = Entry(master=frame_fill, textvariable=name)
        author_entry = Entry(master=frame_fill, textvariable=author)
        datee_entry = Entry(master=frame_fill, textvariable=datee)
        price_entry = Entry(master=frame_fill, textvariable=price)
        dateee_entry = Entry(master=frame_fill, textvariable=dateee)
        izd_entry = Entry(master=frame_fill, textvariable=izd)

        date_label.grid(row=0, column=0, sticky="w")
        number_label.grid(row=4, column=0, sticky="w")
        name_label.grid(row=5, column=0, sticky="w")
        author_label.grid(row=6, column=0, sticky="w")
        datee_label.grid(row=7, column=0, sticky="w")
        price_label.grid(row=8, column=0, sticky="w")
        dateee_label.grid(row=9, column=0, sticky="w")
        izd_label.grid(row=10, column=0, sticky="w")

        date_entry.grid(row=0, column=4, sticky="w")
        number_entry.grid(row=4, column=4, sticky="w")
        name_entry.grid(row=5, column=4, sticky="w")
        author_entry.grid(row=6, column=4, sticky="w")
        datee_entry.grid(row=7, column=4, sticky="w")
        price_entry.grid(row=8, column=4, sticky="w")
        dateee_entry.grid(row=9, column=4, sticky="w")
        izd_entry.grid(row=10, column=4, sticky="w")
        frame_fill.pack(fill='both')

    def search_book(self):
        self.frames_clear()

        frame_search_books = tk.Frame()
        self.frames.append(frame_search_books)

        s = StringVar()
        s_label = Label(master=frame_search_books, text="Введите автора или название:")
        s_entry = Entry(master=frame_search_books, textvariable=s)
        var = IntVar()
        var.set(0)

        def delete_book_a():
            to_delete = s_entry.get()
            self.library.cursor.execute("DELETE FROM library where name like '%{0}%' or author like '%{0}%'".format(to_delete))
            self.library.db.commit()

            lol15 = Label(master=frame_search_books, text="")
            lol15.grid(row=2, )
            lol15.config(text="Удалено")

        def show_book(s):
            for i in tree.get_children():
                tree.delete(i)
            # conn = sqlite3.connect("lib.db")
            cur = self.library.cursor
            cur.execute("SELECT * FROM library where name like '%{0}%' or author like '%{0}%'".format(s))
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        def show_boooook():
            show_book(s.get())

        tree = ttk.Treeview(master=frame_search_books, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "coloumn9"), show='headings')
        tree.heading("#1", text="id")
        tree.heading("#2", text="дата")
        tree.heading("#3", text="инвентарный номер")
        tree.heading("#4", text="название")
        tree.heading("#5", text="автор")
        tree.heading("#6", text="год выпуска")
        tree.heading("#7", text="цена")
        tree.heading("#8", text="дата списания")
        tree.heading("#9", text="номер акта списания")

        tree.column("#1", width=3)
        tree.column("#2", width=80)
        tree.column("#3", width=109)
        tree.column("#4", width=150)
        tree.column("#5", width=100)
        tree.column("#6", width=100)
        tree.column("#7", width=50)
        tree.column("#8", width=118)
        tree.column("#9", width=129)

        tree.grid()

        s_label.grid(sticky="w")
        s_entry.grid(sticky="w")

        b2 = Button(master=frame_search_books, text="Поиск", command=show_boooook)
        b2.grid(sticky="w")

        slabel = Label(master=frame_search_books, text="") # Чтоб было расстояние между кнопками
        slabel.grid(sticky="w")

        b7 = Button(master=frame_search_books, text="Удалить книгу", command = delete_book_a )
        b7.grid(sticky="w")

        frame_search_books.pack()

    def search_book_n(self):
        self.frames_clear()

        frame_search_books = tk.Frame()
        self.frames.append(frame_search_books)

        s = StringVar()
        s_label = Label(master=frame_search_books, text="Введите инвентарный номер:")
        s_entry = Entry(master=frame_search_books, textvariable=s)

        def delete_book_n():
            to_delete = s_entry.get()
            self.library.cursor.execute(
                "DELETE FROM library where number like '%{0}%' or date like '%{0}%'".format(to_delete))
            self.library.db.commit()

            lol15 = Label(master=frame_search_books, text="")
            lol15.grid(row=2, )
            lol15.config(text="Удалено")

        def show_book_n(s):
            for i in tree.get_children():
                tree.delete(i)
            self.library.cursor.execute("SELECT * FROM library where number like '%{0}%' or date like '%{0}%' ".format(s))
            rows = self.library.cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)

        def show_boooook_n():
            show_book_n(s.get())

        tree = ttk.Treeview(master=frame_search_books, column=(
        "column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "coloumn9"),
                            show='headings')
        tree.heading("#1", text="id")
        tree.heading("#2", text="дата")
        tree.heading("#3", text="инвентарный номер")
        tree.heading("#4", text="название")
        tree.heading("#5", text="автор")
        tree.heading("#6", text="год выпуска")
        tree.heading("#7", text="цена")
        tree.heading("#8", text="дата списания")
        tree.heading("#9", text="номер акта списания")

        tree.column("#1", width=3)
        tree.column("#2", width=80)
        tree.column("#3", width=109)
        tree.column("#4", width=150)
        tree.column("#5", width=100)
        tree.column("#6", width=100)
        tree.column("#7", width=50)
        tree.column("#8", width=118)
        tree.column("#9", width=129)

        tree.grid()

        s_label.grid(sticky="w")
        s_entry.grid(sticky="w")

        b2 = Button(master=frame_search_books, text="Поиск", command=show_boooook_n)
        b2.grid(sticky="w")

        slabel = Label(master=frame_search_books, text="")  # Чтоб было расстояние между кнопками
        slabel.grid(sticky="w")

        b7 = Button(master=frame_search_books, text="Удалить книгу", command= delete_book_n)
        b7.grid(sticky="w")

        frame_search_books.pack()

    def all_books(self):
        self.frames_clear()

        def show_books():
            for i in tree.get_children():
                tree.delete(i)
            self.library.cursor.execute("SELECT * FROM library")
            rows = self.library.cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)

            a = self.library.cursor.execute("SELECT SUM(price) FROM library").fetchall()
            pr = "цена:", a
            lol = Label(master=frame_all_books, text="")
            lol.grid(row=1, )
            lol.config(text= pr)

            b = self.library.cursor.execute("SELECT COUNT(*) FROM library ").fetchall()
            count = 'количество', b
            lol1 = Label(master=frame_all_books, text="")
            lol1.grid(row=2, )
            lol1.config(text=count)

        def in_library():
            for i in tree.get_children():
                tree.delete(i)

            cur = self.library.cursor
            cur.execute("SELECT * FROM library where dateee = '' ")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)

            a = self.library.cursor.execute("SELECT SUM(price) FROM library where dateee = '' ").fetchall()

            pr = "цена:", a
            lol = Label(master=frame_all_books, text="")
            lol.grid(row=1, )
            lol.config(text=pr)

            b = self.library.cursor.execute("SELECT COUNT(*) FROM library WHERE dateee = ''").fetchall()
            count = 'количество', b
            lol1 = Label(master=frame_all_books, text="")
            lol1.grid(row=2, )
            lol1.config(text=count)

        def not_in_library():
            for i in tree.get_children():
                tree.delete(i)
            self.library.cursor.execute("SELECT * FROM library where dateee not in('')")
            rows = self.library.cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)

            a = self.library.cursor.execute("SELECT SUM(price) FROM library where dateee not in('')").fetchall()
            pr = "цена:", a
            lol = Label(master=frame_all_books, text="")
            lol.grid(row=1,  )
            lol.config(text=pr)

            b = self.library.cursor.execute("SELECT COUNT(*) FROM library WHERE dateee not in('')").fetchall()
            count = 'количество', b
            lol1 = Label(master=frame_all_books, text="")
            lol1.grid(row=2, )
            lol1.config(text=count)

        frame_all_books = tk.Frame()
        self.frames.append(frame_all_books)
        tree = ttk.Treeview(master=frame_all_books, column=(
        "column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "coloumn9"),
                            show='headings')
        tree.heading("#1", text="id")
        tree.heading("#2", text="дата")
        tree.heading("#3", text="инвентарный номер")
        tree.heading("#4", text="название")
        tree.heading("#5", text="автор")
        tree.heading("#6", text="год выпуска")
        tree.heading("#7", text="цена")
        tree.heading("#8", text="дата списания")
        tree.heading("#9", text="номер акта списания")

        tree.column("#1", width=3)
        tree.column("#2", width=80)
        tree.column("#3", width=109)
        tree.column("#4", width=150)
        tree.column("#5", width=100)
        tree.column("#6", width=100)
        tree.column("#7", width=50)
        tree.column("#8", width=118)
        tree.column("#9", width=129)

        tree.grid()

        b2 = Button(master=frame_all_books, text="Вывести книги в библиотеке", command=in_library)
        b2.grid(sticky="w")

        b3 = Button(master=frame_all_books, text="Вывести списанные книги", command=not_in_library)
        b3.grid(sticky="w")

        b4 = Button(master=frame_all_books, text="Вывести все книги", command=show_books)
        b4.grid(sticky="w")

        frame_all_books.pack()
App()
