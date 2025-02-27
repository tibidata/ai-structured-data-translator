def get_prompt(file_type: str = "json", output_language: str = "Hungarian"):
    """
    Generate a prompt for translation tasks.

    This function creates a customized prompt for an AI assistant to translate
    the values of a specified file type into a target language.

    Args:
        file_type (str): The type of file containing the text to be translated.
                         Defaults to "json".
        output_language (str): The target language for translation.
                               Defaults to "Hungarian".

    Returns:
        str: A formatted prompt string for the AI assistant.

    Example:
        >>> get_prompt("yaml", "French")
        'You are a helpful assistant who helps the user translate the values of a yaml into French"
        You must keep the structure of the json in youre response.
        You must only return the json without explanation'
    """
    # Define the base prompt template
    base_prompt = """You are a helpful assistant who helps the user translate the values of a {file_type} into {output_language}"
                You must keep the structure of the json in youre response.
                You must only return the json without explanation"""

    # Format the base prompt with the provided file type and output language
    return base_prompt.format(file_type=file_type, output_language=output_language)
