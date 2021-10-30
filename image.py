import numpy as np
from PIL import Image

from utils import convert_to_hex


class IMG:
    def __init__(self, image):
        self.image = Image.open(image)

        # old method
        # self.image_max_size = (200, 200)
        # self.resize()
        # self.to_array()

    # Resize to a smaller image to speed up analyze process and reduce overall amount of colors
    def resize(self):
        # If image height or width is higher than specified value
        if self.image.height >= self.image_max_size[0] or self.image.width >= self.image_max_size[1]:
            # Resize and keep aspect ratio
            self.image.thumbnail(self.image_max_size, Image.ANTIALIAS)

    def to_array(self):
        self.array = np.array(self.image)
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]
        self.pixels = self.height * self.width

    def analyze(self, colors=10):
        self.get_most_frequent_rgb_values(colors)
        self.get_rgb()
        self.get_hex()
        self.get_percentage()
        return self.top_colors

    def analyze_new(self, nb_colors=10):

        self.array = np.asarray(self.image)

        print(self.array)
        print(self.array.shape)

        self.height = self.array.shape[0]
        self.width = self.array.shape[1]
        self.pixels = self.height * self.width

        print('****')
        # 3 to group r, g and b values, -1 to let numpy determine the number for rows
        print(self.array.reshape(-1, 3))

        colors, counts = np.unique(self.array.reshape(-1, 3),
                                   return_counts=True,
                                   axis=0)
        print('****')
        print(colors)
        print(counts)

        print(colors.shape)

        # Reshape count to have as many lines as colors
        counts = counts.reshape(colors.shape[0], -1)
        print('****')
        # Add count in the 4th column for each row
        test = np.concatenate((colors, counts), axis=1)
        print(test)

        sorted_array = test[np.argsort(test[:, 3])]
        print('****')
        print(sorted_array)

        # Sorted values in descending order of occurrences
        print('****')
        print(sorted_array[::-1])
        temp = sorted_array[::-1]

        self.top_colors = {}

        for i in range(nb_colors):
            r, g, b = tuple(temp[i, :3])
            print(r, g, b)
            count = int(temp[i, -1:])
            print(count)
            ratio = round(count / self.pixels * 100, 2)

            self.top_colors[i] = {"rgb": (r, g, b),
                                  "hex": f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}',
                                  "ratio": ratio}

        # equivaut à self.top_colors de la premiere version
        return self.top_colors

    def get_color_palette_new(self):
        # Make a copy of self.top_colors (list of dict with rgb, hex and ratio data)
        to_clean = self.top_colors.copy()

        print(to_clean)

        # Create a new empty list
        clean = []

        # Loop while the list to clean still has elements and the clean list has not reached 10 colors
        while to_clean and len(clean) != 10:
            # Get the first item

            first_key = next(iter(to_clean))

            current_color = to_clean[first_key]
            print(current_color)
            # Init too_close to false, this var will become true if any color rgb values are similar to a color already
            # existing in clean list.
            too_close = False
            # Get r,g,b values
            r = current_color['rgb'][0]
            g = current_color['rgb'][1]
            b = current_color['rgb'][2]

            # If clean contains colors
            if clean:
                # Loop through all colors
                for color_2 in clean:
                    # Get r,g,b values
                    r_2 = color_2[0]
                    g_2 = color_2[1]
                    b_2 = color_2[2]

                    # If the absolute difference between both r, both g and both b is less than 24 we consider colors
                    # are too close to eachother so we will not keep it
                    if abs(int(r) - int(r_2)) <= 24 and abs(int(g) - int(g_2)) <= 24 and abs(
                            int(b) - int(b_2)) <= 24:
                        too_close = True

                # Add the color to clean list only if this color is not too close from any other color from clean list
                if not too_close:
                    clean.append((r, g, b))

            # Add the first color to clean list no matter what since it is the most common from the image
            if not clean:
                clean.append((r, g, b))

            # Once we are done with a color we remove it from to_clean list and we start from the beginning of the loop
            del to_clean[first_key]

        print(f"Clean : {clean}")

        # Sort the final list based on the sum of the elements of the tuples from the largest to the smallest
        clean.sort(key=lambda x: int(x[0]) + int(x[1]) + int(x[2]))

        print(f" sorted clean : {clean}")

        # Create final list to store HEX values to display colors in the HTML
        self.color_palette = []
        # Loop through all colors from clean list
        for value in clean:
            r = value[0]
            g = value[1]
            b = value[2]
            # Convert all rgb values to hex and add the result to the list
            self.color_palette.append(f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}')

        print(self.color_palette)

        return self.color_palette

    def get_color_palette(self):
        # Make a copy of self.top_colors (list of dict with rgb, hex and ratio data)
        to_clean = self.top_colors.copy()
        # Create a new empty list
        clean = []

        # Loop while the list to clean still has elements and the clean list has not reached 10 colors
        while to_clean and len(clean) != 10:
            # Get the first item
            current_color = to_clean[0]
            # Init too_close to false, this var will become true if any color rgb values are similar to a color already
            # existing in clean list.
            too_close = False
            # Get r,g,b values
            r = current_color['rgb'][0]
            g = current_color['rgb'][1]
            b = current_color['rgb'][2]

            # If clean contains colors
            if clean:
                # Loop through all colors
                for color_2 in clean:
                    # Get r,g,b values
                    r_2 = color_2[0]
                    g_2 = color_2[1]
                    b_2 = color_2[2]

                    # If the absolute difference between both r, both g and both b is less than 24 we consider colors
                    # are too close to eachother so we will not keep it
                    if abs(int(r) - int(r_2)) <= 24 and abs(int(g) - int(g_2)) <= 24 and abs(
                            int(b) - int(b_2)) <= 24:
                        too_close = True

                # Add the color to clean list only if this color is not too close from any other color from clean list
                if not too_close:
                    clean.append((r, g, b))

            # Add the first color to clean list no matter what since it is the most common from the image
            if not clean:
                clean.append((r, g, b))

            # Once we are done with a color we remove it from to_clean list and we start from the beginning of the loop
            del to_clean[0]

        # Sort the final list based on the sum of the elements of the tuples from the largest to the smallest
        clean.sort(key=lambda x: int(x[0]) + int(x[1]) + int(x[2]))

        # Create final list to store HEX values to display colors in the HTML
        self.color_palette = []
        # Loop through all colors from clean list
        for value in clean:
            r = value[0]
            g = value[1]
            b = value[2]
            # Convert all rgb values to hex and add the result to the list
            self.color_palette.append(f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}')

        return self.color_palette

    def get_most_frequent_rgb_values(self, colors=10):
        # Create a dict to store every single RGB value from the image as the key and the occurrence count as value
        self.rgb_occurrences = {}
        # Create a list to store uniques rgb values as tuples
        self.all_image_colors = []

        # Loop through the image pixels
        for x in range(self.width):
            for y in range(self.height):
                # Get a tuple containing rgb values for every pixel
                rgb = tuple(self.array[y][x])

                # If this rgb combination already exist in the dict, just add 1 to his occurrence count
                if f"{rgb}" in self.rgb_occurrences:
                    self.rgb_occurrences[f'{rgb}'] += 1
                # If this rgb combination doest not exist in the dict we create it and set occurrence count to 1
                # We also add this tuple to the unique colors list
                else:
                    self.rgb_occurrences[f'{rgb}'] = 1
                    self.all_image_colors.append(rgb)

        # Create a new list containing rgb values (dict keys) sorted by occurrence count (dict values)
        # in descending order (reverse=True)
        # Sliced to keep only the specified amount of most common colors
        self.top_rgb_occurences = sorted(self.rgb_occurrences, key=self.rgb_occurrences.get, reverse=True)[:colors]

    def get_rgb(self):

        # # Create a final list of dicts that will contain the most common colors information
        self.top_colors = []
        # Loop through all the colors from the list containing the most common colors
        for color in self.top_rgb_occurences:
            # Loop through all colors from unique colors list
            for col in self.all_image_colors:
                # If any color match between theses 2 lists we add the rgb info to the new list of dict
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
        # Add percentage for each rgb value
        for color in self.top_rgb_occurences:
            for c in self.top_colors:
                if color == str(c['rgb']):
                    c['rate'] = round(self.rgb_occurrences[color] / self.pixels * 100, 2)
