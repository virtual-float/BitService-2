# - - - - - - - #
#    fonts.py   #
# - - - - - - - #

# Imports
import pygame
from typing import Final, Tuple

# Local imports
from bin.exceptions import UnavailableFontError

# Constant
RelativeFontSizes: Final[Tuple] = (
    ('LXX', 70), ('XL', 40), ('XXX', 30),
    ('XXV', 25), ('XXI', 21), ('XX', 20),
    ('XVIII', 18), ('XVI', 16), ('XIV', 14),
    ('XII', 12), ('X', 10), ('VIII', 8)
)

# Fonts dictionary
FontData: dict[str, dict[str, pygame.font.Font]] = {}

# Function for gathering the availability of a specific font
def isFontAvailable(font_name: str) -> bool:
    return pygame.font.SysFont(font_name, 18)

# Function for initializing fonts dictionary
def initFontsDictionary(font_names: list[str]) -> None:
    global FontData, RelativeFontSizes
    
    if FontData != {}:
        return

    if not pygame.font.get_init():
        pygame.font.init()

    for font in font_names:
        current_font = font.strip()

        if not isFontAvailable(current_font):
            raise UnavailableFontError('Unavailable font!')
        
        FontData[current_font] = {}

        for roman_size, decimal_size in RelativeFontSizes:
            FontData[current_font][roman_size] = pygame.font.SysFont(current_font, decimal_size)


pygame.font.init()

initFontsDictionary(['Arial'])