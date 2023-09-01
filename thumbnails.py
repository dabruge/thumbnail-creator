"""
thumbnails.py creates thumbnail images of a size specified by the user, to
be saved in a new directory in the same location as the original images.
"""

import os
import sys

from PIL import Image
from get_files import get_files

# File types that can be included in conversion to thumbnails
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".bmp",
                     ".tif", ".tiff", ".gif", ".eps",]


def get_nonempty_path(prompt):
    """ Returns the path of a directory entered by the user.
    
    Takes string as argument to be used to prompt for user input.
    Utilises isdir() from os module to test path exists and work
    around any difference between "/" and "\" in path.  Flags if
    entered directory contains no files.  Repeats request until
    valid path is entered.
    
    Required imports: os
    Input Agruments: prompt (string)
    Returns: a directory path as a string
    """
    
    while True:
        path = input(prompt).strip()
        
        if os.path.isdir(path):  # Check path is valid
            try:
                for file in os.listdir(path):  # Check not empty directory
                    return path
                print("Directory is empty.")    
            except FileNotFoundError:
                print("Path not found.")
        else:
            print("Path not found.")


def files_exist(file_list):
    """ Returns True is passed in list is not empty.

    Checks if paassed in list is not empty and returns True if so.
    Will exit program if no files found.
    
    Required imports: sys
    Input Arguments: file_list (list)
    Returns: boolean, True -- Note: will exit program
             without returning if file_list passed in is empty
    """
    
    if file_list:
        return True
    else:
        print("\nNo supported files found.")
        print("Exiting program...")
        sys.exit(0)
            
            
def get_thumbnail_size():
    """ Returns thumbnail size entered by user.

    Prompts user to input desired thumbnail size.  Tests whether
    input is an integer and catch ValueError if not.  If an integer
    is entered, then checks if it is positive.  Repeats request
    until a positive integer is entered.
    
    Required imports: none
    Input Arguments: none
    Returns: thumbnail size as an integer
    """
    
    # Declare variable to be tested if negative in while loop.
    # Will always pass first iteration.
    size = -1
    print("\nPlease enter thumbnail size of longest edge (in pixels):")
    
    while size < 0:
        try:
            size = int(input())  # Check input is type integer
            if size < 0:
                print("Must be a positive integer. Please re-enter.")
        except ValueError:
            print("Must be an integer. Please re-enter.")
            
    return size


def new_directory(path, size):
    """ Creates new directory in given path.

    Creates new directory in path passed in, named in format:
        thumbnails_{size}px e.g. thumbnails_150px
    If directory already exists, asks user to confirm whether to
    overwrite, otherwise will exit program.
    
    Required imports: os, sys
    Input Arguments: path (string)
                     size (integer)
    Returns: path of newly created directory -- Note: will exit program
             without returning if directory exists and user chooses not
             to overwrite
    """
    
    # Concatenate name of new directory to end of path
    directory = "thumbnails_" + str(size) + "px"      
    path = os.path.join(path, directory)
    
    try:
        os.mkdir(path)
        return path
    except FileExistsError:
        print("Directory already exists, contents may be overwritten.")
        
        while True:
            overwrite = input("Continue? (y/n) ").lower()
            if overwrite == "y":
                return path
            elif overwrite == "n":
                print("Exiting program...")
                sys.exit(0)


def create_thumbnails(path_images, path_save, file_list, size):
    """ Creates thumbnail images of a specfied size.

    Iterates through each passed in file, using the Image.thumbnail
    method from PIL to convert to thumbnail with max edge length of
    the passed in size.  Saves images to passed in directory in JPG
    format with size of image added to filename.  Prints confirmation
    and saved location when all thumbnails have been created.
    
    Required imports: os, PIL.Image
    Input Arguments: path_images (string) - path of images for conversion
                     path_save (string) - path to save thumbnails in
                     file_list (list) - list of files to create thumbnails of
                     size (integer) - size of longest edge of thumbnails
    Returns: nothing -- Prints confirmation files created and path to them
    """
    
    # Maximum dimensions for thumbnail
    SIZE = (size, size)
    
    for file in file_list:
        # Get the filename without extension for each image
        name_ext = os.path.splitext(file)
        filename = name_ext[0]
        with Image.open(path_images + "/" + file) as im:
            # Creates thumbnail of image with default BICUBIC filter
            im.thumbnail(SIZE)
            # Saves in new directory and modifies filename
            im.save(path_save + "/" + filename + "_" + str(size) \
                    + "px.jpg", quality=95)
            
    print("\nSuccessfully created thumbnails.")
    print("Files can be found in:\n" + os.path.normpath(path_save))
        

if __name__ == "__main__":
    path_images = get_nonempty_path("Please enter path to image directory:\n")
    files = get_files(path_images, SUPPORTED_FORMATS)
    files_exist(files)
    size = get_thumbnail_size()
    path_save = new_directory(path_images, size)
    create_thumbnails(path_images, path_save, files, size)
