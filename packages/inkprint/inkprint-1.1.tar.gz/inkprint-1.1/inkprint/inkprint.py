import warnings
import random
from collections import OrderedDict


class InkPrinter:
    def __init__(self, paper_color='b', ink_color='g'):

        # Available colors. 
        # When initiating an instance, both full color name and the one-letter name will work.
        self.colors_to_use = OrderedDict({
            'k': 'black',
            'r': 'red',
            'g': 'green',
            'y': 'yellow',
            'b': 'blue',
            'c': 'cyan',
            'm': 'magenta',
        })

        
        self.paper_color = self.colors_to_use.get(paper_color, paper_color)
        self.ink_color = self.colors_to_use.get(ink_color, ink_color)

        self.validate_colors()

        self.colorizer = self.get_colorizer()



    def validate_colors(self):
        """Make sure the color are chosen from valid color list and readable"""
        if self.paper_color not in self.colors_to_use and self.paper_color not in self.colors_to_use.values():
            raise ValueError(f"Wrong paper_color used: {self.paper_color}. \nPlease pick one from {self.colors_to_use}")

        elif self.paper_color == self.ink_color:
            rest_colors = [c for c in self.colors_to_use.values() if c!=self.paper_color]
            print(f"DEBUG rest_colors = {rest_colors}")
            self.ink_color = random.choice(rest_colors)
            warnings.warn("Paper and ink have the same color. Ink is changed to a random color.")

        else:
            pass


    def get_colorizer(self):
        """Return the prefix string based on the paper and ink color.
        https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
        """
        color_list = [c for c in self.colors_to_use.values()]
        digit1 = color_list.index(self.paper_color)
        digit2 = color_list.index(self.ink_color)
        colorizer = ''.join(['\x1b[0;3', str(digit2), ';4', str(digit1), 'm'])
        return colorizer


    def print(self, input_str):
        print(self.colorizer + input_str + '\x1b[0m')