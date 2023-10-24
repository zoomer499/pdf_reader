import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
from pdf_viewer.pdf_renderer import PDFRenderer

class PDFViewer:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas  # Принимаем canvas в качестве аргумента
        self.pdf_renderer = PDFRenderer()
        self.pdf_window = None

    def open_pdf_file(self):
        # Закрываем предыдущее окно PDF-просмотра, если оно есть
        if self.pdf_window:
            self.close_pdf_window()
    
        # Запрашиваем у пользователя путь к PDF-файлу
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
        # Проверяем, что файл выбран
        if file_path:
            try:
                self.pdf_renderer.open_pdf(file_path)
                self.pdf_renderer.load_pages()
    
                # Создаем новое окно для отображения PDF
                self.pdf_window = tk.Toplevel(self.root)
                self.pdf_window.title("PDF Viewer")
    
                # Удалите предыдущий canvas, если он существует и не был удален ранее
                if self.canvas and self.canvas.winfo_exists():  # Добавляем проверку на существование canvas
                    self.canvas.destroy()
    
                # Создаем Canvas для отображения страниц PDF
                self.canvas = tk.Canvas(self.pdf_window)
                self.canvas.pack(fill="both", expand=True)
    
                # Создаем кнопки "Следующая страница" и "Предыдущая страница"
                next_button = tk.Button(self.pdf_window, text="Следующая страница", command=self.next_page)  # Добавляем команду next_page
                prev_button = tk.Button(self.pdf_window, text="Предыдущая страница", command=self.prev_page)  # Добавляем команду prev_page
                next_button.pack(side="right")
                prev_button.pack(side="right")
    
                # Показываем первую страницу
                self.show_page(self.pdf_renderer.current_page)
            except Exception as e:
                # Выводим сообщение об ошибке, если не удалось открыть файл
                print(f"Ошибка при открытии файла: {e}")

    def close_pdf_window(self):
        self.pdf_renderer.close_pdf()
        if self.pdf_window:
            # Удалите текущий canvas, если он существует и не был удален ранее
            if self.canvas and self.canvas.winfo_exists():  # Добавляем проверку на существование canvas
                self.canvas.destroy()
            self.pdf_window.destroy()
            self.pdf_window = None

    def show_page(self, page_number):
        if self.pdf_renderer.pdf_pages:
            image = self.pdf_renderer.show_page(page_number)
            if self.canvas and self.canvas.winfo_exists():  # Добавляем проверку на существование canvas
                self.canvas.delete("all")  # Очищаем Canvas
                photo = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor="nw", image=photo)
                self.canvas.photo = photo  # Сохраняем ссылку на PhotoImage
                self.canvas.update_idletasks()

    def next_page(self):
        if 0 <= self.pdf_renderer.current_page < len(self.pdf_renderer.pdf_pages) - 1:
            self.pdf_renderer.current_page += 1
            self.show_page(self.pdf_renderer.current_page)

    def prev_page(self):
        if 0 < self.pdf_renderer.current_page <= len(self.pdf_renderer.pdf_pages) - 1:
            self.pdf_renderer.current_page -= 1
            self.show_page(self.pdf_renderer.current_page)

    def resize_pdf_page(self, event):
        if self.pdf_renderer.pdf_pages:
            self.show_page(self.pdf_renderer.current_page)
