# -*- coding: utf-8 -*-
# Created on Friday, July 19 15:30:00 2024
# @author: mefamex

# project_name = "image-meta-dataset"
# project_version = "1.0.0"
# project_author = "Mefamex"
# project_date = "29.01.2025"
# project_description = "This is a project description"
# project_license = "MIT"
# project_repository = "https://github.com/Mefamex/image-meta-dataset"
# project_url = "https://mefamex.com/projects/image-meta-dataset"

# pip install piexif pillow 
from PIL import Image
import os, piexif, piexif.helper

print("----------------------------------------\n"+os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))
print(__file__)
print("Pillow Version:", Image.__version__, "\n----------------------------------------\n")

from PIL import Image
import piexif
import piexif.helper
import os

def display_metadata(image_path):
    if not os.path.exists(image_path):
        print(f"Hata: {image_path} bulunamadı.")
        return
    
    image = Image.open(image_path)
    exif_bytes = image.info.get("exif")
    exif_data = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    
    print("Mevcut Metadata:")
    for ifd in exif_data:
        if exif_data[ifd] is None or isinstance(exif_data[ifd], bytes):
            continue
        for tag, value in exif_data[ifd].items():
            try:
                if isinstance(value, bytes):
                    value = value.decode(errors='ignore')
                print(f"{piexif.TAGS[ifd][tag]['name']}: {value}")
            except KeyError:
                print(f"{tag}: {value}")
    print("............................................")

def modify_image_metadata(image_path, output_path):
    if not os.path.exists(image_path):
        print(f"Hata: {image_path} bulunamadı.")
        return
    
    image = Image.open(image_path)
    exif_bytes = image.info.get("exif")
    exif_data = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    
    print("Mevcut Metadata'yı Değiştirin:")
    for ifd in exif_data:
        if exif_data[ifd] is None or isinstance(exif_data[ifd], bytes):
            continue
        for tag in list(exif_data[ifd].keys()):
            try:
                tag_name = piexif.TAGS[ifd][tag]['name']
                current_value = exif_data[ifd][tag]
                if isinstance(current_value, bytes):
                    current_value = current_value.decode(errors='ignore')
                new_value = input(f"{tag_name} için yeni değer ({current_value}): ")
                if new_value:
                    exif_data[ifd][tag] = new_value.encode() if isinstance(exif_data[ifd][tag], bytes) else new_value
            except KeyError:
                continue
    
    print("Yeni Metadata Ekleyin:")
    metadata_keys = {k: v['name'] for d in piexif.TAGS.values() for k, v in d.items()}
    while True:
        print("Eklenebilecek metadata türleri:")
        for key, name in metadata_keys.items():
            print(f"{key}: {name}")
        
        key_input = input("Eklemek istediğiniz metadata anahtarını girin (veya çıkmak için 'q' yazın): ")
        if key_input.lower() == 'q':
            break
        
        if key_input.isdigit() and int(key_input) in metadata_keys:
            value_input = input(f"{metadata_keys[int(key_input)]} için değer girin: ")
            exif_data["0th"][int(key_input)] = value_input.encode() if isinstance(value_input, str) else value_input
    
    exif_bytes = piexif.dump(exif_data)
    image.save(output_path, exif=exif_bytes)
    print(f"Yeni metadata ile {output_path} olarak kaydedildi.")

# Örnek Kullanım
image_path = "a.webp"
output_path = "aa.webp"
display_metadata(image_path)
#modify_image_metadata(image_path, output_path)