import itertools
import fitz
import io
from PIL import Image
from pathlib import Path

"""
Use the following instructions
    function 1: list(map(extract_fimage, p))
    The first function extract images of pdf files from list_of_book folder

    function 2: make_output_foler(dirs)
    The second function arrange the results into the output folder
"""

# Using the module pathlib to select the files from folder
p = Path(parents=True)
p_books = p.joinpath("list_of_books").iterdir()

def extract_fimage(file):
    pdf_file = fitz.open(file)
    book_title = pdf_file.metadata['title']
    for page_index in range(len(pdf_file)):
        if page_index != 0:
            continue
        # get the page itself
        page = pdf_file[page_index]
        # get image list
        image_list = page.get_images()
        # printing number of images found in this page
        for image_index, img in enumerate(image_list, start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to disk
            filename = image.save(open(f"{book_title}_{page_index+1}_{image_index}.{image_ext}", "wb"))

# Assigning file extension to its identifier
dirs = {".png": "Images", ".jpeg": "Images"}

def make_output_folder(p, dirs):
    # Create a new folder to save each image file
    p_images = p / "output"

    files = [f for f in p.iterdir() if f.is_file()]
    files_bool =[bool(dirs.get(f.suffix)) for f in files]
    filter_files = [f for f in itertools.compress(files, files_bool)]

    for f_image in filter_files:
        p_images.mkdir(exist_ok=True)
        f_image.rename(p_images / f_image.name)


if __name__ == "__main__":
     print("Executing the first function method to extract the cover page of books from list_of_books...")
     list(map(extract_fimage, p_books))

     print("Create output folder...")
     make_output_folder(p, dirs)
