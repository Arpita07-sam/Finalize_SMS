import pandas as pd
from img2table.document import Image
from img2table.ocr import TesseractOCR

# 1. SETUP OCR 
# Note: If you are on Windows, you might need to specify the path to tesseract.exe:
# ocr = TesseractOCR(n_threads=1, lang="eng", tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
ocr = TesseractOCR(n_threads=1, lang="eng")

# 2. LOAD IMAGE
try:
    doc = Image("signatures\location\loc18.jpeg") # Ensure this filename matches yours!
except FileNotFoundError:
    print("Error: Could not find 'timetable.png'. Please check the file path.")
    exit()

# 3. EXTRACTION
# We use borderless_tables=True because many timetables don't have thick outer borders
extracted_tables = doc.extract_tables(ocr=ocr, 
                                     implicit_rows=True, 
                                     borderless_tables=True, 
                                     min_confidence=50)

# 4. DATA PROCESSING
if extracted_tables:
    # Get the dataframe attribute (.df) from the first table found
    df = extracted_tables[0].df
    
    if df is not None and not df.empty:
        # Basic Clean: Drop empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        print("--- EXTRACTED TIMETABLE ---")
        print(df.to_string()) # to_string() prevents the text from being cut off
        
        # --- GENERATE SUMMARY ---
        print("\n" + "="*30)
        print("SUMMARY REPORT")
        print(f"Detected {len(df)} rows of schedule.")
        
        # Flatten and count subjects
        content = df.iloc[:, 1:].values.flatten()
        summary = pd.Series([str(x).strip() for x in content if pd.notna(x) and str(x).strip() != ""]).value_counts()
        
        print("\nMost Frequent Subjects:")
        print(summary.head(5))
        
        # Export
        df.to_excel("my_timetable.xlsx", index=False)
        print("\nData saved to 'my_timetable.xlsx'")
    else:
        print("Table detected, but no text could be read. Check your OCR/Tesseract installation.")
else:
    print("No tables detected. Try a clearer image or one with visible grid lines.")