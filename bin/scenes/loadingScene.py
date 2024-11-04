##########################
# scenes/loadingScene.py #
##########################

# global imports
from typing import Iterable
from pygame.sprite import AbstractGroup


# local imports
from bin.scene import Scene

# it implements the loading scene on the start

class loadingScene(Scene):
    def __init__(self, isActive: bool = True, name: str | None = None, *sprites: AbstractGroup | Iterable) -> None:
        super().__init__(isActive, name, *sprites)