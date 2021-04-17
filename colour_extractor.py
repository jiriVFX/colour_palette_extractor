import numpy
import cv2
from sklearn.cluster import KMeans
from collections import Counter


class ColourExtractor:
    def __init__(self):
        self.image = None
        self.resized_image = None

    def load_image(self, path):
        """Reads an image file into self.image.
        :type path: str
        """
        self.image = cv2.imread(path)

    def show_image(self, image, seconds=2000):
        """Opens image in a window.
        :type image: numpy.ndarray
        :type seconds: int
        """
        cv2.imshow("Image", image)
        cv2.waitKey(seconds)
        cv2.destroyAllWindows()
        print(image.shape)

    def resize_image(self, percentage=50):
        """Resizes image into percentage of its original size. Result is in self.resized_image.
        :type percentage: int"""
        original_height = self.image.shape[0]
        original_width = self.image.shape[1]
        print(f"Original width: {original_width}px")
        print(f"Original height: {original_height}px")
        resized_width = round(original_width * percentage / 100)
        resized_height = round(original_height * percentage / 100)
        print(f"Resized width: {resized_width}px")
        print(f"Resized height: {resized_height}px")

        # https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#cv2.resize
        self.resized_image = cv2.resize(self.image, dsize=(resized_width, resized_height), interpolation=cv2.INTER_CUBIC)

    def rgb_to_hex(self, r, g, b):
        """Converts RGB values into single HEX colour string.
        :type r: int
        :type g: int
        :type b: int
        :rtype: str"""
        hex_colour = "{:02x}{:02x}{:02x}".format(r, g, b)
        return hex_colour

    def extract_colours(self, colours_num):
        """Extracts most dominant colours from the image
        :type colours_num: int
        :rtype: list[str]"""
        # Reshape 3D array into a 2D list (cv2 builds on numpy, so images are a numpy arrays)
        print(self.resized_image.shape)
        # reshape width and height into (423 * 196, 3)
        # This way we have one pixel RGB(a) (actually BGR because of cv2) values on each row
        list_of_pixels = self.resized_image.reshape(
            self.resized_image.shape[0] * self.resized_image.shape[1], self.resized_image.shape[2]
        )
        print(type(list_of_pixels))
        # Find the most frequent(dominant) colours
        # return self.find_dominant_colours1(list_of_pixels, colours_num)
        return self.find_dominant_colours2(list_of_pixels, colours_num)

    def find_dominant_colours1(self, list_of_pixels, colours_num, min_difference=1000000):
        """Finds and returns colours_num most dominant (frequent) colours in the list of pixels,
        results not great use find_dominant_colours2 instead.
        :type list_of_pixels: numpy.ndarray
        :type colours_num: int
        :type min_difference: int
        :rtype: list[(str, int)]"""
        # Convert BGR values to HEX values, so we can count them
        hex_list = [self.rgb_to_hex(colour[2], colour[1], colour[0]) for colour in list_of_pixels]
        # Count colours
        counter_dict = Counter(hex_list)

        # Exclude colours with less than min_difference between (to ensure colour variety)
        sorted_colours = counter_dict.most_common()
        # Take first and the last 1000 items - works
        selected_colours = sorted_colours[:1000] + sorted_colours[-1000:]
        # add the first colour
        diff_colours = [selected_colours[0]]

        # Every newly added colour has to be different by last_difference from previous colour
        # This way we ensure better colour variety
        for i in range(1, len(selected_colours)):
            can_add = True
            current_colour = selected_colours[i]
            # Compare hex values (convert HEX string to int for the comparison)
            # against all already added colours
            for added_colour in diff_colours:
                if abs(int(current_colour[0], 16) - int(added_colour[0], 16)) < min_difference:
                    # if the difference between current_colour and any of already added colours
                    # is not higher than min_difference, colour won't be added
                    can_add = False
                    break
            # Add colour is can_add is True
            if can_add:
                diff_colours.append(current_colour)

        # Get colours_num amount of most common colours
        # counter_dict has tuples with colour and amount of appearances - e.g.: ('#2e3136', 1414)
        # most_dominant has tuples of HEX colour codes
        # and percentage of appearance in the image (rounded to two decimal places)
        most_dominant = [("#" + colour[0], "{:.2f}".format(round(colour[1] / len(counter_dict) * 100), 2))
                         for colour in diff_colours[:colours_num]]
        # return most common colours
        return most_dominant

    def find_dominant_colours2(self, list_of_pixels, colours_num):
        """Finds and returns colours_num most dominant (frequent) colours in the list of pixels.
        Takes longer than find_dominant_colours1, but gives better results.
        :type list_of_pixels: numpy.ndarray
        :type colours_num: int
        :rtype: list[(str, int)]"""
        # Utilizing Adam Spannbauer's approach using scikit-learn KMeans
        clusters = KMeans(n_clusters=colours_num)
        colours = clusters.fit_predict(list_of_pixels)

        # Count labels to find most popular
        colour_counter = Counter(colours)
        most_common = colour_counter.most_common()
        # Subset out most popular centroid
        # dominant_color = clusters.cluster_centers_[label_counts.most_common(colours_num)[0][0]]
        dominant_colors = []

        # In case there is less colours than requested
        if len(most_common) < colours_num:
            colours_num = len(most_common)

        for i in range(colours_num):
            # Get cluster center, convert ndarray to a list
            dominant_color = (clusters.cluster_centers_[most_common[i][0]].tolist(), most_common[i][1])
            # Convert BGR values into single HEX colour value, calculate colour dominance percentage
            dominant_color_hex = (
                "#" + self.rgb_to_hex(int(dominant_color[0][2]), int(dominant_color[0][1]), int(dominant_color[0][0])),
                "{:.2f}".format(round(dominant_color[1] / len(list_of_pixels) * 100))
            )
            # append colour to the list of dominant colours
            dominant_colors.append(dominant_color_hex)

        return dominant_colors


# extractor = ColourExtractor()
# extractor.load_image("static/img/cyberpunk_finished.png")
# # extractor.show_image(image=extractor.image)
# extractor.resize_image()
# # extractor.show_image(image=extractor.resized_image)
# print(extractor.extract_colours(10))
