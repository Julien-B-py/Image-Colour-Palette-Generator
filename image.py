import numpy as np
from PIL import Image

from utils import convert_to_hex


class IMG:
    def __init__(self, image_path: str) -> None:
        """
        Constructs a new IMG object.
        @param image_path: Specify the image path the user wants to extract color from.
        @type image_path: str
        """
        self.image = Image.open(image_path)
        # Create array from image
        self.array = np.asarray(self.image)
        # Get image dimensions
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]
        # Get image total pixels amount
        self.pixels = self.height * self.width
        # Create an empty list to store image most common colors information
        self.top_colors = []
        # Create final list to store HEX values to display colors in the HTML
        self.color_palette = []

    def analyze(self, nb_colors: int = 6000) -> list:
        """
        Analyze the image to extract and determine the most common colors.
            @param nb_colors: Specify the number of unique r,g,b combinations to extract from the image.
            @type nb_colors: int
            :returns: A list of dictionaries containing r,g,b values, hex value and the ratio for each unique color.
        """
        # Reshape the array to group RGB values for each pixel
        # Values: -1 to let numpy determine the number for rows and 3 to group r, g and b values
        simplified_array = self.array.reshape(-1, 3)

        # Create 2 arrays to store unique RGB values and the associated counts (number of occurrence for the specific
        # RGB combination
        colors, counts = np.unique(simplified_array,
                                   return_counts=True,
                                   axis=0)

        # Reshape count to have as many lines as colors array
        counts = counts.reshape(colors.shape[0], -1)
        # Crate a new array containing RGB combinations and add count in the 4th column for each row
        final_array = np.concatenate((colors, counts), axis=1)
        # Create a new array sorted on count value for each RGB combination
        sorted_array = final_array[np.argsort(final_array[:, 3])]
        # Finally sort values in descending order of occurrences
        sorted_array = sorted_array[::-1]

        # Extract the specified amount of colors from the image
        for i in range(nb_colors):
            # For each row extract r, g, b values, the associated occurrences number and the associated ratio
            try:
                r, g, b = tuple(sorted_array[i, :3])
                count = int(sorted_array[i, -1:])
                ratio = round(count / self.pixels * 100, 2)
            # If we looped more than the actual max number of colors
            except IndexError:
                break
            else:
                # Store theses data as a dict in the list top_colors
                self.top_colors.append({"rgb": (r, g, b),
                                        "hex": f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}',
                                        "ratio": ratio})

        return self.top_colors

    def get_color_palette(self, delta: int = 24, nb_colors: int = 10) -> list:
        """
        Analyze the extracted colors from the image to create a color palette by ignoring similar colors based on delta
        value. The smaller the delta the more similar colors you will have in the color palette.
            @param delta: Specify the quantization delta to determine how close are 2 colors. For example with 24 as
            delta (0,0,0) and (0,0,25) are considered different since at least one element has a difference above 24.
            @type delta: int
            @param nb_colors: Specify the number of colors the color palette must contain
            @type nb_colors: int
            :returns: A list of hexadecimal colors.
        """
        # Make a copy of self.top_colors (list of dict with rgb, hex and ratio data)
        to_clean = self.top_colors.copy()
        # Create a new empty list to store only colors that are not similar (based on delta between r, g, b values)
        clean = []
        # Loop while the list to clean still has elements and the clean list has not reached the specified number of
        # colors
        while to_clean and len(clean) != nb_colors:
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

                    # If the absolute difference between both r, both g and both b is less than specified delta we
                    # consider colors are too close to eachother so we will not keep it
                    if abs(int(r) - int(r_2)) <= delta and abs(int(g) - int(g_2)) <= delta and abs(
                            int(b) - int(b_2)) <= delta:
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

        # Loop through all colors from clean list
        for value in clean:
            r = int(value[0])
            g = int(value[1])
            b = int(value[2])
            # Convert all rgb values to hex and add the result to the list
            self.color_palette.append(f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}')

        return self.color_palette
