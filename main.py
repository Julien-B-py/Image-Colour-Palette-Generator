import numpy as np
from PIL import Image

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    im = Image.open("test.png")

    # Convert image into NumPy array
    image_array = np.array(im)
    # height x width x channel
    # print(image_array.shape)
    # print(image_array.ndim)

    height = image_array.shape[0]
    width = image_array.shape[1]

    color = {}

    for x in range(width):
        for y in range(height):
            rgb = tuple(image_array[y][x])
            if f"{rgb}" in color:
                color[f'{rgb}'] += 1
            else:
                color[f'{rgb}'] = 1

    top_10 = sorted(color, key=color.get, reverse=True)[:10]

    top_10_colors = [key for key in top_10]
    print(top_10_colors)
