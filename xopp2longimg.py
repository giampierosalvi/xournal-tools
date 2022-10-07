import sys # for command-line arguments
import os # for file system
import PIL # for image manipulation
from PIL import Image
from tempfile import gettempdir # for temp directory (obviously)
from random import randint # for temp file name

def element_after(element, arr: list, convert_to=None):
    """Returns the next element after the given element in the provided list.

    Args:
        arr (list): list which should be searched through
        element (any): the element before the wanted element in the list.
        convert_to (any): converts the result to some data-type.

    Returns:
        Any: Depends on the datatype of the element. 
        NoneType: If the given element isn't in the list or is the last element.
    """
    result = None
    try: result = arr[arr.index(element)+1]
    except ValueError: pass
    
    try:
        if convert_to is not None: result = convert_to(result)
    except TypeError: pass
        
    return result

def imgs2longimg(img_paths: list[str], output_path: str, max_width: int=None, 
                max_height: int=None, background: str=None):
    """Connecting multiple images to one long image. 
    This is a stripped down version of a function which is hosted at:
    https://github.com/OsiPog/bogdan-tools/blob/master/imgs2longimg.py

    Args:
        img_paths (list[str]): A list of all input-image paths.
        output_path (str): The file path of the long output-image.
        max_width (int, optional): Scale the image down if value exceeded.
        max_height (int, optional): Scale the image down if value exceeded.
    """

    pil_images: list = []
    # this will be the width of the most wide image at the end of the loop
    long_width: int = 0 
    # all heights all added up
    long_height: int = 0
    for png_path in img_paths:
        try:
            image = Image.open(png_path, "r")

            # Error would happen one line above
        
        # Skip images that do not work
        except PIL.UnidentifiedImageError: continue
        
        pil_images.append(image)
        long_width = max(image.size[0], long_width)
        long_height += image.size[1]

    # The long transparent image
    long_image = Image.new("RGB", (long_width, long_height), (255, 255, 255))
    
    MIDDLE_X: int = round(long_width/2)
    current_height: int = 0
    for image in pil_images:
        # getting the right offset so that the images are centered and above
        # each other
        paste_offset = (MIDDLE_X - round(image.size[0]/2), current_height)
        
        long_image.paste(image, paste_offset)
        
        current_height += image.size[1]

    # scaling long image according to max_height or max_width
    if not max_width: max_width = long_image.size[0]
    if not max_height: max_height = long_image.size[1]
    long_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # saving the file to the specified file
    long_image.save(output_path)
    print(f"Successfully saved image file to '{output_path}'")


def main():
    if len(sys.argv) < 3:
        print("""Usage: python xopp2longimg.py output-file input-file.xopp [options]
(The output-file can by any image-like file type.)
    Options:
        -h <int>\tScaling the image down to a certain height if it exceeds it
        -w <int>\tScaling the image down to a certain width if it exceeds it
""")
        exit()

    output_path: str = sys.argv[1]
    input_path: str = sys.argv[2]

    # Converting the xopp to seperate images 
    temp_dir: str = gettempdir()
    # for cross platform
    while "\\" in temp_dir: temp_dir = temp_dir.replace("\\", "/")
    
    # To make sure that a folder like that really doesn't exist yet
    rnd_name: str = str(randint(0,99999))
    temp_dir += f"/{rnd_name}"
    
    os.mkdir(temp_dir)

    # Assuming Xournal++ is installed and in PATH
    os.system(f"xournalpp -i {temp_dir}/{rnd_name}.png {input_path}")

    # getting all the seperate images + file paths
    png_paths: list[str] = os.listdir(temp_dir)
    for i,png in enumerate(png_paths): png_paths[i] = f"{temp_dir}/{png}"
    
    
    # Adding up all the images into one
    imgs2longimg(png_paths, output_path,
                 max_width = element_after("-w", sys.argv, int), 
                 max_height = element_after("-h", sys.argv, int))
    
    # Deleting temp files and folder
    for png in png_paths: os.remove(png)
    os.rmdir(temp_dir)


if __name__ == "__main__":
    main()