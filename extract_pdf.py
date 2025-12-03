import sys
try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not installed.")
    sys.exit(1)

def extract_text(pdf_path, output_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return "Text extracted to " + output_path
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    pdf_path = "Project-1-revised.docx.pdf"
    output_path = "extracted_text.txt"
    print(extract_text(pdf_path, output_path))
