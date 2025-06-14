import os
import json
import pandas as pd
import PyPDF2

# 📂 Set data folder
data_folder = r'E:\project1\data'
print(f"🔍 Starting conversion for folder: {data_folder}")

# Check if folder exists
if not os.path.exists(data_folder):
    print(f"❌ Folder not found: {data_folder}")
    exit()

files = os.listdir(data_folder)
if not files:
    print("⚠️ No files found in the data folder!")
else:
    print(f"📄 Found {len(files)} file(s): {files}")

for filename in files:
    file_path = os.path.join(data_folder, filename)
    print(f"➡️ Processing file: {filename}")

    if filename.lower().endswith('.pdf'):
        print(f"📄 Attempting to convert PDF: {filename}")
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                json_data = {'filename': filename, 'content': text.strip()}
                json_filename = filename.replace('.pdf', '.json')
                json_path = os.path.join(data_folder, json_filename)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                print(f"✅ JSON created: {json_filename}")
            else:
                print(f"⚠️ No text extracted from {filename}")
        except Exception as e:
            print(f"❌ Error with PDF {filename}: {e}")

    elif filename.lower().endswith('.xlsx'):
        print(f"📈 Attempting to convert Excel: {filename}")
        try:
            excel_data = pd.read_excel(file_path)
            if not excel_data.empty:
                json_data = excel_data.to_dict(orient='records')
                json_filename = filename.replace('.xlsx', '.json')
                json_path = os.path.join(data_folder, json_filename)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                print(f"✅ JSON created: {json_filename}")
            else:
                print(f"⚠️ Excel file {filename} is empty")
        except Exception as e:
            print(f"❌ Error with Excel {filename}: {e}")

    else:
        print(f"ℹ️ Skipping unsupported file type: {filename}")

print("🎉 Conversion completed!")

