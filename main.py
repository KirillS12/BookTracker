import tkinter as tk
from tkinter import messagebox
import json

books = []


def load_books():
    
    global books
    try:
        with open("books.json", "r", encoding="utf-8") as file:
            books = json.load(file)
            update_list(books)
    except (FileNotFoundError, json.JSONDecodeError):
        books = []


def save_books():
    
    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)





def add_book():
    
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    pages = entry_pages.get()

    if title == "" or author == "" or genre == "" or pages == "":
        messagebox.showwarning("Ошибка", "Заполните все поля!")
        return

    try:
        int(pages) 
    except ValueError:
        messagebox.showwarning("Ошибка", "Количество страниц введено неверно!")
        return

    new_book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }

    books.append(new_book)
    save_books()
    update_list(books)
    
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)






def update_list(list_to_show):
    listbox_books.delete(0, tk.END)
    for book in list_to_show:
        info = f"{book['title']} - {book['author']} ({book['genre']}, {book['pages']} стр.)"
        listbox_books.insert(tk.END, info)



def filter_books():
    
    find_genre  = box_find_genre.get().lower()
    find_pages = box_find_pages.get()
    result = books

    filtered_by_genre = []
    for book in books:
        if find_genre in book['genre'].lower():
            filtered_by_genre.append(book)
            
    
    final_result = []
    for book in filtered_by_genre:
        if find_pages == "": 
            final_result.append(book)
        else:
             try:
                 min_pages = int(find_pages)
                 if book['pages'] >= min_pages:
                     final_result.append(book)
             except ValueError:
                messagebox.showwarning("Ошибка", "Введите целое число в поле страниц!")
                return
            
            
    update_list(final_result)





window = tk.Tk()
window.title("Book Tracker")
window.geometry("600x600")

tk.Label(window, text="Название книги:").pack()
entry_title = tk.Entry(window)
entry_title.pack()

tk.Label(window, text="Автор:").pack()
entry_author = tk.Entry(window)
entry_author.pack()

tk.Label(window, text="Жанр книги:").pack()
entry_genre = tk.Entry(window)
entry_genre.pack()

tk.Label(window, text="Количество страниц:").pack()
entry_pages = tk.Entry(window)
entry_pages.pack()

tk.Button(window, text="Добавить книгу", command=add_book).pack(pady=10)

tk.Label(window, text="--- ФИЛЬТРЫ ---").pack(pady=5)

tk.Label(window, text="Поиск по жанру:").pack()
box_find_genre = tk.Entry(window, width=20)
box_find_genre.pack()

tk.Label(window, text="Минимум страниц:").pack()
box_find_pages = tk.Entry(window, width=10)
box_find_pages.pack()

tk.Button(window, text="Отфильтровать", command=filter_books).pack(pady=10)
tk.Button(window, text="Показать все", command=lambda: update_list(books)).pack(pady=5)

tk.Label(window, text="Все книги:").pack(pady=5)
listbox_books = tk.Listbox(window, width=50)
listbox_books.pack(padx=10, pady=10)

load_books()
window.mainloop()
