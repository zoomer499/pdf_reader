import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF для открытия PDF-страниц
from PIL import Image, ImageTk  # Pillow для конвертации изображений

# Глобальные переменные
current_page = 0
pdf_document = None  # Добавим переменную для хранения PDF-документа
pdf_pages = []  # Добавим список для хранения изображений страниц PDF
pdf_window = None  # Добавим переменную для хранения окна PDF-просмотра

# Функция для отображения текущей страницы
def show_page(page_number, canvas):
    if 0 <= page_number < len(pdf_pages):
        canvas.delete("all")  # Очищаем Canvas
        canvas.create_image(0, 0, anchor="nw", image=pdf_pages[page_number])
        canvas.update_idletasks()

# Функция для закрытия окна PDF-просмотра
def close_pdf_window():
    global pdf_document, pdf_window
    pdf_document.close()  # Закрываем PDF-документ
    pdf_window.destroy()  # Закрываем окно PDF-просмотра
    pdf_window = None  # Сбрасываем ссылку на окно

# Функция для открытия и отображения PDF-файла
def open_pdf_file():
    global current_page, pdf_document, pdf_pages, pdf_window

    # Закрываем предыдущее окно PDF-просмотра, если оно есть
    if pdf_window:
        close_pdf_window()

    # Запрашиваем у пользователя путь к PDF-файлу
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    # Проверяем, что файл выбран
    if file_path:
        try:
            # Открываем PDF-файл с использованием PyMuPDF (fitz)
            pdf_document = fitz.open(file_path)

            # Очищаем список изображений страниц PDF
            pdf_pages.clear()

            # Создаем новое окно для отображения PDF
            pdf_window = tk.Toplevel(root)
            pdf_window.title("PDF Viewer")

            # Создаем Canvas для отображения страниц PDF
            canvas = tk.Canvas(pdf_window)
            canvas.pack(fill="both", expand=True)

            # Функция для перелистывания на следующую страницу
            def next_page():
                global current_page
                if 0 <= current_page < len(pdf_pages) - 1:
                    current_page += 1
                    show_page(current_page, canvas)

            # Функция для перелистывания на предыдущую страницу
            def prev_page():
                global current_page
                if 0 < current_page <= len(pdf_pages) - 1:
                    current_page -= 1
                    show_page(current_page, canvas)

            # Создаем кнопки "Следующая страница" и "Предыдущая страница"
            next_button = tk.Button(pdf_window, text="Следующая страница", command=next_page)
            prev_button = tk.Button(pdf_window, text="Предыдущая страница", command=prev_page)
            next_button.pack(side="right")
            prev_button.pack(side="right")

            # Загружаем изображения всех страниц PDF
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)
                image = page.get_pixmap()
                pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
                photo = ImageTk.PhotoImage(pil_image)
                pdf_pages.append(photo)

            # Показываем первую страницу
            show_page(current_page, canvas)

        except Exception as e:
            # Выводим сообщение об ошибке, если не удалось открыть файл
            print(f"Ошибка при открытии файла: {e}")

# Функция для обновления размера страницы PDF при изменении размера окна программы
def resize_pdf_page(event):
    if pdf_pages:
        show_page(current_page, canvas)

# Создание главного окна приложения
root = tk.Tk()
root.title("PDF Reader")

# Кнопка для открытия PDF-файла
open_button = tk.Button(root, text="Открыть PDF-файл", command=open_pdf_file)
open_button.pack()

# Создаем Canvas для отображения страниц PDF
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

# Подключаем обработчик изменения размера окна
root.bind("<Configure>", resize_pdf_page)

# Запуск главного цикла приложения
root.mainloop()