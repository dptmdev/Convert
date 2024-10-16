import os
from PIL import Image
import pillow_heif
import pathlib
import shutil


# Load HEIC support into Pillow
pillow_heif.register_heif_opener()


def convert_heic_to_jpeg_with_exif(input_heic_path, output_jpeg_path):
    image = Image.open(input_heic_path)

    # Extract EXIF data from HEIC
    exif_data = image.info.get('exif')

    # Convert to JPEG and attach EXIF if available
    if exif_data:
        image.save(output_jpeg_path, "JPEG", exif=exif_data)
    else:
        image.save(output_jpeg_path, "JPEG")

    print(f"Converted {input_heic_path} to {output_jpeg_path} with EXIF.")

# Convert all HEIC files in a directory


def batch_convert_heic_to_jpeg(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            input_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(dirpath, folder_path)
            output_dir = os.path.join(output_folder, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            if filename.lower().endswith('.heic') or filename.lower().endswith('.heif'):
                output_path = os.path.join(
                    output_dir, f"{os.path.splitext(filename)[0]}.jpg")
                convert_heic_to_jpeg_with_exif(input_file_path, output_path)
            else:
                output_file_path = os.path.join(output_dir, filename)
                shutil.copy(input_file_path, output_file_path)

                print(f"Copied {input_file_path} to {output_file_path}")


if __name__ == '__main__':
    print("Enter the path for input folder: ")
    temp = input()
    input_dir = pathlib.Path(temp)
    print("Enter the path for output folder: ")
    temp = input()
    output_dir = pathlib.Path(temp)
    batch_convert_heic_to_jpeg(input_dir, output_dir)
