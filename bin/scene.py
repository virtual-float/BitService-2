#####################
#    scene.py       #
#####################

# global import
from abc import ABC, abstractmethod
from typing import Iterable
from pygame.sprite import AbstractGroup, Group as spriteGroup
from pygame.surface import Surface

# local imports
from bin.exceptions import ChangeOfConstant, InvalidType

# The purpose of this module is to allow abstraction of what is seen on screen
# Every scene contains of sprites, its own attributes, loop and draw method
# without that it would be a very great hustle for example to change a scene from a office to his home (just example)

@ABC
class Scene(spriteGroup):
    @abstractmethod
    async def draw(self, screen: Surface) -> None: pass
    
    @abstractmethod
    async def loop(self) -> None: pass
    
    
    async def __internalLoop(self):
        if self.active:
            self.loop()
        
        
    # -------------------------    
    # property accessing points
    # -------------------------        

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, val: str) -> None: 
        raise ChangeOfConstant("You can't change that constant! The name of the scene is constant during whole execution of the code!")
        
    @property
    def active(self) -> bool:
        return self.__isActive
    
    @active.setter
    def active(self, val: bool | None):
        if val != None:
            if val != True and val != False:
                raise InvalidType("The scene can be only active or not active, nothing in between!")        
    
    def __init__(self, name: str, isActive: bool = True, *sprites: AbstractGroup | Iterable) -> None:
        # intialize pygame stuff
        super().__init__(*sprites)
        
        # save attributes
        self.__name: str = name
        self.__isActive: bool = isActive