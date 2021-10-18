import numpy as np
from PIL import Image

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def hello_world():
    top_colors = get_colors_stats("test.png")

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

    rgb_occurences = {}
    all_image_colors = []

    for x in range(width):
        for y in range(height):
            rgb = tuple(image_array[y][x])
            if f"{rgb}" in rgb_occurences:
                rgb_occurences[f'{rgb}'] += 1
            else:
                rgb_occurences[f'{rgb}'] = 1
                all_image_colors.append(rgb)

    top_10_rgb_occurences = sorted(rgb_occurences, key=rgb_occurences.get, reverse=True)[:10]

    top_colors = []

    # # Create a list of dicts containing rgb values
    for color in top_10_rgb_occurences:
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
    for color in top_10_rgb_occurences:
        for c in top_colors:
            if color == str(c['rgb']):
                c['rate'] = round(rgb_occurences[color] / pixels * 100, 2)

    return top_colors


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
