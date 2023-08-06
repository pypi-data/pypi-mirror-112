from pdf2image import convert_from_path
import os
from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)

#pdf_path = "/Users/zero/Desktop/m6A regulator-mediated methylation modification patterns and characteristics of immunity and stemness in low-grade glioma.pdf"

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        fname = os.path.dirname(pdf_path) + "/image" + str(i) + ".png"
        image.save(fname, "PNG")


#pdf_to_images(pdf_path = pdf_path)
