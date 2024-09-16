import os
import zipfile
from PIL import Image

def unzip_folder(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")

def is_image_valid(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Check if the image is corrupted
            img = Image.open(file_path)  # Reopen to perform further checks
            img_format = img.format
            if img_format not in ['JPEG', 'PNG', 'GIF']:  # You can add more formats here
                return False
            img_size = os.path.getsize(file_path)
            if img_size == 0:
                return False
            return True
    except Exception:
        return False

def is_image_blank(file_path):
    try:
        with Image.open(file_path) as img:
            # Convert image to grayscale and check if all pixels are white
            img = img.convert('L')
            pixels = img.getdata()
            return all(p == 255 for p in pixels)
    except Exception:
        return False

def process_images(directory):
    valid_images = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                if is_image_valid(file_path):
                    if not is_image_blank(file_path):
                        valid_images.append(file_path)
                    else:
                        os.remove(file_path)  # Remove blank images
                else:
                    os.remove(file_path)  # Remove invalid images
            except PermissionError as e:
                print(f"PermissionError: {e} - Skipping file: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return valid_images

def zip_images(image_paths, output_zip):
    try:
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for img_path in image_paths:
                zipf.write(img_path, os.path.basename(img_path))
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"Error creating zip file {output_zip}: {e}")

def main(zip_paths, extract_to, output_zips):
    for zip_path, output_zip in zip(zip_paths, output_zips):
        unzip_folder(zip_path, extract_to)
        valid_images = process_images(extract_to)
        zip_images(valid_images, output_zip)

if __name__ == "__main__":
    # Example usage
    zip_paths = ['D:/Pictures.zip', 'D:/Pictures 1.zip']  # Paths to the zip files
    extract_to = 'D:/Extracted Images'  # Folder where files will be extracted
    output_zips = 'D:/Validni sliki/processed_images.zip'  # Paths to save the new zip files

    main(zip_paths, extract_to, output_zips)
