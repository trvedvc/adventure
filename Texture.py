
import arcade
from math import *

def load_weapon_texture_pair(filename, hit_box_algorithm: str = "Simple"):  # Default: "Simple"
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename,
                            hit_box_algorithm=hit_box_algorithm),
        arcade.load_texture(filename,
                            flipped_vertically=True,
                            hit_box_algorithm=hit_box_algorithm)
    ]


def load_texture_pair(filename, hit_box_algorithm: str = "Simple"):
    """
    Load a texture pair, with the second being a mirror image of the first.
    Useful when doing animations and the character can face left/right.
    """
    return [
        arcade.load_texture(filename,
                            hit_box_algorithm=hit_box_algorithm),
        arcade.load_texture(filename,
                            flipped_horizontally=True,
                            hit_box_algorithm=hit_box_algorithm)
    ]