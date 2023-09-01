import os


def get_files(path, extensions):
    """ Returns a list of filenames whose file formats also appear
        in passed in list.
        
    Iterates through files in provided path, splits out the extension
    and checks if it appears in list of provided extensions.  If there
    is a match, the file name is added to the list 'file_list'.
    
    Required imports: os
    Input Arguments: path (string)
                     extensions (list)
    Returns: a list of filenames -- Note: if path is invalid or no
             extension matches, will return an empty list.
    """
    
    file_list = [] # To store files with matching extensions in
    
    try:
        for file in os.listdir(path):
            parts = os.path.splitext(file)
            # Get file extension
            ext = parts[1].lower()
            
            # Iterate through each supported extension type
            for extension in extensions:
                extension = extension.lower()
                if extension == ext:
                    file_list.append(file)                
    # Check path exists (in case function passed unchecked path)
    except FileNotFoundError:
        print("Could not find path: " + path)
        
    return file_list
