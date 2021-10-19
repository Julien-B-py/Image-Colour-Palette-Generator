import numpy as np
from PIL import Image

from utils import convert_to_hex


class IMG:
    def __init__(self, image):
        self.image = Image.open(image)
        self.image_max_size = (200, 200)
        self.resize()
        self.to_array()

    # # Resize to a smaller image to speed up analyze process and reduce overall amount of colors
    def resize(self):
        if self.image.height >= self.image_max_size[0] or self.image.width >= self.image_max_size[1]:
            # Keep aspect ratio
            self.image.thumbnail(self.image_max_size, Image.ANTIALIAS)

    def to_array(self):
        self.array = np.array(self.image)
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]
        self.pixels = self.height * self.width


    def analyse(self,colors=10):
        self.get_most_frequent_rgb_values(colors)
        self.get_rgb()
        self.get_hex()
        self.get_percentage()
        return self.top_colors


    def get_most_frequent_rgb_values(self, colors=10):
        # Create a dict to store every single RGB value from the image as the key and the occurrence count as value
        self.rgb_occurrences = {}
        # Create a list to store uniques rgb values as tuples
        self.all_image_colors = []

        for x in range(self.width):
            for y in range(self.height):

                rgb = tuple(self.array[y][x])

                # Count
                if f"{rgb}" in self.rgb_occurrences:
                    self.rgb_occurrences[f'{rgb}'] += 1
                else:
                    self.rgb_occurrences[f'{rgb}'] = 1
                    self.all_image_colors.append(rgb)

        # Create a new list containing rgb values (dict keys) sorted by occurrence count (dict values)
        # in descending order (reverse=True)
        # Sliced to keep only the 10 most common colors
        self.top_rgb_occurences = sorted(self.rgb_occurrences, key=self.rgb_occurrences.get, reverse=True)[:colors]

    def get_rgb(self):

        # # Create a final list of dicts that will contain the most common colors information
        self.top_colors = []
        for color in self.top_rgb_occurences:
            for col in self.all_image_colors:
                if color == str(col):
                    self.top_colors.append({'rgb': col})

    def get_hex(self):
        # Add hex values to the list of dicts
        for color in self.top_colors:
            rgb = color['rgb']
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            color['hex'] = f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}'

    def get_percentage(self):
        # Add percentage
        for color in self.top_rgb_occurences:
            for c in self.top_colors:
                if color == str(c['rgb']):
                    c['rate'] = round(self.rgb_occurrences[color] / self.pixels * 100, 2)


