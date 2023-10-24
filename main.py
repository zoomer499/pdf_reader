import tkinter as tk
from pdf_viewer.pdf_gui import PDFViewer  # Обратите внимание на измененный импорт

def main():
    root = tk.Tk()
    root.title("PDF Reader")

    canvas = tk.Canvas(root)  # Создаем canvas здесь
    canvas.pack(fill="both", expand=True)

    pdf_viewer = PDFViewer(root, canvas)  # Передаем canvas в качестве аргумента

    open_button = tk.Button(root, text="Открыть PDF-файл", command=pdf_viewer.open_pdf_file)
    open_button.pack()

    root.bind("<Configure>", pdf_viewer.resize_pdf_page)

    root.mainloop()

if __name__ == "__main__":
    main()