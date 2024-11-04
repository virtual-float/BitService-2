# - - - - - - - - #
#   component.py  #
# - - - - - - - - #

# Imports
import pygame
from abc import ABC, abstractmethod
from typing import Iterable, Final

# Local imports
from bin.exceptions import ComponentInitError
#import bin.tools as tools

DEFAULT_LAYOUT_INDEX: Final[int] = 0

# Abstract Component class
class Component(ABC, pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], texture: pygame.Surface, use_alpha: bool = False) -> None:
        super().__init__()

        if size[0] < 0 or size[1] < 0:
            raise ComponentInitError('Attempted to set a negative width or height!')

        if use_alpha:
            self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        else:
            self.image = pygame.Surface(size)
        
        self.image.blit(texture, (0, 0))

        self.size = size
        self.rect = self.image.get_rect()

        self.__alpha = use_alpha
    
    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError('Attempted to invoke an unimplemented method!')

    def has_alpha(self) -> bool:
        return self.__alpha


# Components group
class ComponentsGroup(pygame.sprite.Group):
    def __init__(self, components: Iterable[Component] = []) -> None:
        super().__init__(components)


# Layout group for components (For rendering order purposes)
class Layout(pygame.sprite.Group):
    def __init__(self, components: ComponentsGroup, layout_index: int = DEFAULT_LAYOUT_INDEX) -> None:
        super().__init__(components.sprites())

        self.index = layout_index
    
    def __init__(self, components: Iterable[Component], layout_index: int = DEFAULT_LAYOUT_INDEX) -> None:
        super().__init__(components)

        self.index = layout_index