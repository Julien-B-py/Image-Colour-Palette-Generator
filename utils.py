def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file extension is part of the list of allowed file extensions.
        @param filename: Specify the name of the file the user is attemption to upload.
        @type filename: str
        :returns: True if the file extension is allowed.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def convert_to_hex(value: int) -> str:
    """
    Convert an integer value (0 to 255) in hexadecimal to determine equivalent hex code for a RGB color.
        @param value: Specify the quantization delta to determine how close are 2 colors. For example with 24 as
        delta (0,0,0) and (0,0,25) are considered different since at least one element has a difference above 24.
        @type value: int
        :returns: A formatted string containing the hexadecimal equivalent of the input integer.
    """
    # Remove the not needed '0x' from the returned string
    hex_value = hex(value).replace('0x', '')
    # Added to uniformize output with 2 digits.
    if len(hex_value) < 2:
        hex_value = f'0{hex_value}'
    return hex_value
