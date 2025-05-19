import sys
from PIL import Image
import pytesseract

def decode_code39_barcode(image_path):
    try:
        # Load the image
        image = Image.open(image_path)

        # Use Tesseract OCR to extract text from the image
        text = pytesseract.image_to_string(image)

        # Clean up the result (remove whitespace and newlines)
        decoded_text = text.strip()

        # Print the decoded string
        if decoded_text:
            print(decoded_text)
        else:
            print("No barcode text found.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    image_file = input().strip()
    decode_code39_barcode(image_file)
