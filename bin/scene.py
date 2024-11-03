#####################
#    scene.py       #
#####################

# global import
from abc import ABC, abstractmethod
from typing import Iterable
from pygame.sprite import AbstractGroup, Group as spriteGroup, LayeredDirty
from pygame.surface import Surface
from asyncio import sleep

# local imports
from bin.exceptions import ChangeOfConstant, InvalidType

# The purpose of this module is to allow abstraction of what is seen on screen
# Every scene contains of dirty sprites, its own attributes, and loop method
# without that it would be a very great hustle for example to change a scene from a office to his home (just example)

class Scene(ABC, LayeredDirty):
    tickrate = 1/20
    
    @abstractmethod
    async def loop(self) -> None: pass
    
    
    async def __internalLoop(self):
        if self.active:
            self.loop()
            self.update()
            
        # tickrate is 20 per seconds
        sleep(self.tickrate)
        
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