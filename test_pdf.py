from pdf.pdf_generator import (
    PDFGenerator
)

generator = PDFGenerator()

generator.generate_folder_pdf(
    "data/output/sorted/Pharmacology/Theory",
    "pharmacology_theory.pdf"
)

print("Done")