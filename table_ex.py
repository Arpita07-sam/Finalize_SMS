from img2table.document import Image
from img2table.ocr import TesseractOCR

# 1. Initialize the OCR engine
ocr = TesseractOCR(n_threads=1, lang="eng")

# 2. Load your image
img = Image(src="signatures\sample\sample7.jpeg")

# 3. Extract tables (returns a list of ExtractedTable objects)
extracted_tables = img.extract_tables(ocr=ocr, implicit_rows=True)

# 4. Get the first table as a Pandas DataFrame
if extracted_tables:
    df = extracted_tables[0].df
    print(df)
else:
    print("No table detected!")