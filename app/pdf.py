import fitz
from deep_translator import GoogleTranslator

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
    return text

def translate_text(text, target_language="ru"):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_text = translator.translate(text)
    return translated_text

def save_to_html(text, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"<html><body><p>{text.replace('\n', '<br>')}</p></body></html>")

def pdf_to_translated_html(pdf_path, output_html_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    # translated_text = translate_text(extracted_text, "ru")
    save_to_html(extracted_text, output_html_path)
    print(f"Translated HTML saved to {output_html_path}")

pdf_path = "c:\\Users\\pavlo_poliak\\Downloads\\DesignPatterns.pdf"
output_html_path = "translated_output.html"
pdf_to_translated_html(pdf_path, output_html_path)
