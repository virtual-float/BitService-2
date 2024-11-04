#####################
#    scene.py       #
#####################

# global imports
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Union
from pygame.sprite import AbstractGroup, Group as spriteGroup, LayeredDirty
from pygame.surface import Surface
from asyncio import sleep

# local imports
from bin.exceptions import ConstantChangeError, InvalidTypeError

# The purpose of this module is to allow abstraction of what is seen on screen
# Every scene contains of dirty sprites, its own attributes, and loop method
# without that it would be a very great hustle for example to change a scene from a office to his home

class Scene(ABC, LayeredDirty):
    """The scene represents a single page of the application"""
    tickrate = 1/20
    __defaultName = ""
    
    @abstractmethod
    async def loop(self) -> None:
        """a loop is executed every tick"""
        pass
    
    
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
        raise ConstantChangeError("You can't change that constant! The name of the scene is constant during whole execution of the code!")
        
    @property
    def active(self) -> bool:
        return self.__isActive
    
    @active.setter
    def active(self, val: Optional[bool]):
        if val != None:
            if val != True and val != False:
                raise InvalidTypeError("The scene can be only active or not active, nothing in between!") 
        
        self.__isActive = val       
    
    def __init__(self, isActive: bool = True, name: Optional[str] = None, *sprites: Union[AbstractGroup, Iterable]) -> None:
        """creates an instance of the scene

        Args:
            isActive (bool, optional): if The scene is active. Non-active scenes can still be drawn. Defaults to True.
            name (Optional[str], optional): The name of the scene. Names have to be unique. If it's none, it will be copied from class default name. Defaults to None.
        """
        # intialize pygame stuff
        super().__init__(*sprites)
        
        # save attributes
        if name: self.__name = name
        else: self.__name = self.__defaultName
        
        self.__isActive: bool = isActive