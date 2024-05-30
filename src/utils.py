import os

def load_context_data(context_dir):
    """
    Load context data from a specified directory. The context data can be text files
    that contain relevant information for answering user queries.

    Parameters:
    context_dir (str): The directory containing the context files.

    Returns:
    str: A concatenated string of all the context data.
    """
    context_data = ""
    for filename in os.listdir(context_dir):
        file_path = os.path.join(context_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                context_data += file.read() + "\n\n"
    return context_data
