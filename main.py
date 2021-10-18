import time

import numpy as np
from PIL import Image

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

# Specify the path where the app will store the uploaded files
UPLOAD_FOLDER = r'static\uploads'

app = Flask(__name__)

# Specify the path where the app will store the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)


@app.route("/")
def hello_world():
    top_colors = get_colors_stats("static/uploads/small.png")

    return render_template('index.html', top_colors=top_colors)


def convert_to_hex(value):
    hex_value = hex(value).replace('0x', '')
    # Added to uniformize output with 2 digits.
    if len(hex_value) < 2:
        hex_value = f'0{hex_value}'
    return hex_value


def get_colors_stats(image):
    im = Image.open(image)

    # Convert image into NumPy array
    image_array = np.array(im)
    # Shape = height x width x channels
    height = image_array.shape[0]
    width = image_array.shape[1]
    pixels = height * width

    # Create a dict to store every single RGB value from the image as the key and the occurrence count as value
    rgb_occurrences = {}
    # Create a list to store uniques rgb values as tuples
    all_image_colors = []

    delta = 100

    """
    r = image_array[:, :, 0]
    g = image_array[:, :, 1]
    b = image_array[:, :, 2]
    """

    for x in range(width):
        for y in range(height):

            too_close = False

            rgb = tuple(image_array[y][x])

            r = int(rgb[0])
            g = int(rgb[1])
            b = int(rgb[2])

            if f"{rgb}" in rgb_occurrences:
                rgb_occurrences[f'{rgb}'] += 1
            else:

                rgb_occurrences[f'{rgb}'] = 1
                all_image_colors.append(rgb)

    # Create a new list containing rgb values (dict keys) sorted by occurrence count (dict values)
    # in descending order (reverse=True)
    # Sliced to keep only the 10 most common colors
    top_rgb_occurences = sorted(rgb_occurrences, key=rgb_occurrences.get, reverse=True)[:10]

    # # Create a final list of dicts that will contain the most common colors information
    top_colors = []
    for color in top_rgb_occurences:
        for col in all_image_colors:
            if color == str(col):
                top_colors.append({'rgb': col})

    # Add hex values to the list of dicts
    for color in top_colors:
        rgb = color['rgb']
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]

        color['hex'] = f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}'

    # Add percentage
    for color in top_rgb_occurences:
        for c in top_colors:
            if color == str(c['rgb']):
                c['rate'] = round(rgb_occurrences[color] / pixels * 100, 2)



    #### TEST delta colors
    cleaned_list = []
    # Stocke premiere valeur
    color_0 = all_image_colors[0]

    cleaned_list.append(color_0)
    del all_image_colors[0]

    while all_image_colors:
        color_0 = all_image_colors[0]
        # print(color_0)
        too_close = False

        for color in cleaned_list:
            if (abs(int(color_0[0]) - int(color[0]))) <= delta and (abs(int(color_0[1]) - int(color[1]))) <= delta and (
            abs(int(color_0[2]) - int(color[2]))) <= delta:
                too_close = True
                break

        if not too_close:
            cleaned_list.append(color_0)

        del all_image_colors[0]

    print(cleaned_list)


    print(top_colors)
    return top_colors


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
