# - - - - - - - #
#    Tools.py   #
# - - - - - - - #

# Imports
import pygame

# Local imports
from bin.tools import readImage


class AnimationFrame(pygame.Surface):
    def __init__(self, texture: pygame.Surface) -> None:
        super().__init__(texture.get_size(), pygame.SRCALPHA, 32)

        self.blit(texture, (0, 0))

        self.rect = self.get_rect()
        self.rect.topleft = (0, 0)


class Animation:
    def __init__(self, texture_package: str, element_width: int, element_height: int) -> None:
        self.texture_path = texture_package
        self.texture = readImage(self.texture_path, uses_alpha=True)

        self.__element_width = element_width
        self.__element_height = element_height

        self.__total_elements_x = self.texture.get_width() // self.__element_width
        self.__total_elements_y = self.texture.get_height() // self.__element_height

        self.__frames: list[AnimationFrame] = []

        for y in range(0, self.__total_elements_y, 1):
            for x in range(0, self.__total_elements_x, 1):
                surface = pygame.Surface((self.__element_width, self.__element_height), pygame.SRCALPHA, 32)
                surface.blit(
                    self.texture,
                    (0, 0),
                    (self.__element_width * x, self.__element_height * y, self.__element_width * (x + 1), self.__element_height * (y + 1))
                )

                frame = AnimationFrame(surface)

                self.__frames.append(frame)

        self.__iterator = 0

    def play(self, victim) -> None:
        raise NotImplementedError('Attempted to invoke a not-implemented method!')