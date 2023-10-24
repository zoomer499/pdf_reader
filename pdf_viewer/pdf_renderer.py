import fitz
from PIL import Image

class PDFRenderer:
    def __init__(self):
        self.current_page = 0
        self.pdf_document = None
        self.pdf_pages = []

    def open_pdf(self, file_path):
        # Открываем PDF-файл с использованием PyMuPDF (fitz)
        self.pdf_document = fitz.open(file_path)
        self.pdf_pages = []

    def close_pdf(self):
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None

    def load_pages(self):
        if self.pdf_document:
            for page_number in range(self.pdf_document.page_count):
                page = self.pdf_document.load_page(page_number)
                image = page.get_pixmap()
                pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
                self.pdf_pages.append(pil_image)

    def show_page(self, page_number):
        if 0 <= page_number < len(self.pdf_pages):
            return self.pdf_pages[page_number]
