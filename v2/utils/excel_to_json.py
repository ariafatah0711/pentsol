import pandas as pd
import json
import os
from config import EXCEL_FOLDER

def log_success(message):
    print(f"[+] {message}")

def log_failure(message):
    print(f"[X] {message}")

def log_info(message):
    print(f"[!] {message}")

def convert_excel_to_json(excel_files, json_file):
    """Mengkonversi beberapa file Excel dari folder tertentu ke satu file JSON"""
    try:
        all_data = []
        current_id = 1
        
        # Pastikan direktori output JSON ada
        output_dir = os.path.dirname(json_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            log_success(f"Created directory: {output_dir}")
            
        # Pastikan folder input Excel ada
        if not os.path.exists(EXCEL_FOLDER):
            log_failure(f"Folder input Excel '{EXCEL_FOLDER}' tidak ditemukan.")
            return False

        processed_files_count = 0
        for excel_filename in excel_files:
            # Ekstrak nama kategori dari nama file (misal: network_security.xlsx -> Network Security)
            category_name_raw = os.path.splitext(excel_filename)[0]  # network_security
            formatted_category_name = category_name_raw.replace('_', ' ').title()  # Format nama kategori

            # Buat path lengkap ke file Excel
            excel_filepath = os.path.join(EXCEL_FOLDER, excel_filename)
            
            if not os.path.exists(excel_filepath):
                log_info(f"Warning: File {excel_filepath} tidak ditemukan, dilewati.")
                continue

            log_success(f"Processing {excel_filepath}...")
            # Baca file Excel
            df = pd.read_excel(excel_filepath)
            processed_files_count += 1
            
            # Konversi ke format yang diinginkan
            for _, row in df.iterrows():
                # Tangani nilai NaN atau float sebelum split
                symptoms = str(row['gejala']).split('|') if pd.notna(row['gejala']) else []
                solutions = str(row['solusi']).split('|') if pd.notna(row['solusi']) else []
                tools = str(row['tools']).split('|') if pd.notna(row['tools']) else []
                references = str(row['referensi']).split('|') if pd.notna(row['referensi']) else []
                problems = str(row['masalah']).split('|') if pd.notna(row['masalah']) else []
                attack_signs = str(row['tanda_serangan']).split('|') if pd.notna(row['tanda_serangan']) else []

                technique = {
                    'id': str(current_id),
                    'name': str(row['teknik']),
                    'category': formatted_category_name,
                    'description': str(row['deskripsi']),
                    'symptoms': [s.strip() for s in symptoms],
                    'solutions': [s.strip() for s in solutions],
                    'tools': [t.strip() for t in tools],
                    'references': [r.strip() for r in references],
                    'priority': str(row['prioritas']),
                    'problems': [p.strip() for p in problems],
                    'attack_signs': [a.strip() for a in attack_signs]
                }
                all_data.append(technique)
                current_id += 1
        
        if processed_files_count == 0:
            log_failure(f"Tidak ada file Excel yang ditemukan di folder {EXCEL_FOLDER}")
            return False
            
        # Simpan ke file JSON
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            log_success(f"Data berhasil dikonversi dari {processed_files_count} file Excel di '{EXCEL_FOLDER}' ke {json_file}")
        except Exception as e:
            log_failure(f"Error saat menyimpan ke file JSON: {e}")
            return False
        return True
    except FileNotFoundError as e:
        log_failure(f"File tidak ditemukan - {e}")
        return False
    except Exception as e:
        log_failure(f"Error converting Excel to JSON: {str(e)}")
        return False

# Definisikan fungsi utama untuk konversi
def convert_all_excel_to_json():
    # --- Start Perubahan ---
    # Secara dinamis cari semua file .xlsx di folder input
    try:
        if not os.path.exists(EXCEL_FOLDER):
            log_failure(f"Folder input Excel '{EXCEL_FOLDER}' tidak ditemukan saat mencari file.")
            return False
        
        all_files_in_folder = os.listdir(EXCEL_FOLDER)
        excel_files_to_convert = [
            f for f in all_files_in_folder 
            if f.lower().endswith('.xlsx') and not f.startswith('~$')
        ]
        
        if not excel_files_to_convert:
            log_failure(f"Tidak ada file .xlsx yang ditemukan di folder '{EXCEL_FOLDER}'. Konversi dibatalkan.")
            return False  # Anggap ini sebagai kondisi gagal
    except Exception as e:
        log_failure(f"Error saat mencari file Excel di '{EXCEL_FOLDER}': {str(e)}")
        return False
    # --- Akhir Perubahan ---
   
    # Nama file JSON output
    json_output_file = 'data/pentest_data.json'
   
    # Panggil fungsi konversi DAN return hasilnya
    return convert_excel_to_json(excel_files_to_convert, json_output_file)

# Jalankan konversi jika script dijalankan langsung
if __name__ == "__main__":
    convert_all_excel_to_json()