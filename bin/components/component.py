# - - - - - - - - #
#   component.py  #
# - - - - - - - - #

# Imports
import pygame
from abc import ABC, abstractmethod
from typing import Iterable

# Local imports
#import bin.exceptions as e
#import bin.tools as tools

# Abstract class
class DrawableComponent(ABC, pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], texture: pygame.Surface, use_alpha: bool = False) -> None:
        super().__init__()

        if use_alpha:
            self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        else:
            self.image = pygame.Surface(size)
        
        self.image.blit(texture, (0, 0))

        self.rect = self.image.get_rect()

        self.__alpha = use_alpha
    
    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError('Attempted to invoke an unimplemented method!')

    def has_alpha(self) -> bool:
        return self.__alpha


# Drawable Components group
class DrawableComponents(pygame.sprite.Group):
    def __init__(self, components: Iterable[DrawableComponent] = []) -> None:
        super().__init__(components)