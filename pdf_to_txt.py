# %%

from typing import List
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import glob

def convert_pdf_to_image(
    fname: str, 
    resolution: int = 800,
    path: str = './'
) -> List[Image.Image]:
    """
    Converts a PDF to a Pillow Image object.

    Args:
        fname: Filename without extension.
        resolution: Resolution of resulting image in dpi. Default 800.
        path: Path to the pdf file.

    Returns:
        images: List of resulting Pillow images.
    """
    images = convert_from_path(path + fname + ".pdf", dpi=resolution, 
                               output_folder=path)
    return images

def convert_image_to_string(
    images: List[Image.Image],
    lang: str = 'spa'
) -> List[str]:
    """
    Converts a list of Pillow images to strings using tesseract.
    Intended to read text from a scanned pdf.

    Args:
        images: List of images containing the pages of the original pdf.
        lang: Language of text, defaults to 'spa' for Spanish.
    
    Returns:
        pages: List of strings containing the text from each page.
    """
    pages = []
    #pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    #custom_oem_psm_config = r'--psm 12'
    custom_oem_psm_config = ''
    for image in images:
        pages.append(pytesseract.image_to_string(
            image, lang=lang, 
            config=custom_oem_psm_config))
    return pages

def delete_temp_files(path: str = './') -> None:
    """
    Deletes all .ppm files in path.

    Args:
        path: a string with the path.
    """
    temp_file_list = glob.glob(path + "*.ppm")
    for temp_file in temp_file_list:
        os.remove(temp_file)

def save_pdf_as_text(fname: str, resolution=800, path: str = './') -> None:
    """
    Converts a scanned pdf to a txt file.

    Args:
        fname: Name of the pdf.
        resolution: Resolution of the images in ppi.
        path: Path to the pdf file.
    """
    shorter_fname = fname[:-4]
    print(f"Converting {shorter_fname}.pdf to image.")
    images = convert_pdf_to_image(shorter_fname, resolution, path)
    print(f"Converting image to string.")
    pages = convert_image_to_string(images)
    print(f"Saving string as {shorter_fname}.txt")
    with open(path + shorter_fname + ".txt", "w") as fout:
        fout.write('\n'.join(pages))
    print(f"Cleaning up.")
    delete_temp_files(path)

# %%
