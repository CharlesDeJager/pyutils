def handle_escape_characters(input_string, escape_char='\\'):
    """
    Handle escape characters in a given input string.
    
    Args:
        input_string (str): The string to process.
        escape_char (str): The character used for escaping.
        
    Returns:
        str: The processed string with escape characters handled.
    """
    # Replace escaped escape characters with a placeholder
    processed_string = input_string.replace(escape_char + escape_char, '\0')
    
    # Replace escaped characters with their actual representation
    processed_string = processed_string.replace(escape_char + 'n', '\n')
    processed_string = processed_string.replace(escape_char + 't', '\t')
    processed_string = processed_string.replace(escape_char + ',', ',')
    processed_string = processed_string.replace(escape_char + '|', '|')
    processed_string = processed_string.replace(escape_char + ';', ';')
    
    # Restore the placeholder for escaped escape characters
    processed_string = processed_string.replace('\0', escape_char)
    
    return processed_string


def escape_characters(input_string, escape_char='\\'):
    """
    Escape special characters in a given input string.
    
    Args:
        input_string (str): The string to process.
        escape_char (str): The character used for escaping.
        
    Returns:
        str: The processed string with special characters escaped.
    """
    # Escape special characters
    escaped_string = input_string.replace(escape_char, escape_char + escape_char)
    escaped_string = escaped_string.replace('\n', escape_char + 'n')
    escaped_string = escaped_string.replace('\t', escape_char + 't')
    escaped_string = escaped_string.replace(',', escape_char + ',')
    escaped_string = escaped_string.replace('|', escape_char + '|')
    escaped_string = escaped_string.replace(';', escape_char + ';')
    
    return escaped_string