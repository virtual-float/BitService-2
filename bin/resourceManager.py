######################
# resourceManager.py #
######################

# The purpose of this module is to not reuse the same texture and waste memory and computing time

# global imports
from pygame import SRCALPHA
from pygame.surface import Surface
from pygame.image import load as loadImagePygame
from enum import Enum
from typing import Iterable, TypedDict, Optional
from datetime import datetime
import traceback
from aiofiles import open as asyncOpen
from os import path as pathTools

# local imports
from bin.exceptions import InternalResourceManagerError, AccessToNotExistingResourceError
from bin.tools import readJSON

class loadedFileType(Enum):
    pygamesurface = "pygamesurface"
    pygamesurfaceTransparent = "pygamesurfacetransparent"
    surface = "pygamesurface"
    surfaceTransparent = "pygamesurfacetransparent"
    json = "json"
    pythonmodule = "pythonmodule"
    python = "pythonmodule"
    rawfile = "rawfile"
    file = "rawfile"
    raw = "rawfile"
    

class preloadResourceInformation(TypedDict):
    """represents a single unit of a resource to be preloaded\n\n
    -------------------------\n
    path (str): path to the file\n
    saveAs (Optional[str]): path to be saved as (can be used to just simple time "bob" or "char/bob" instead of "characters/bob.png"). if None then it will be determined during execution by looking at a path\n
    ofType (Optional[loadedFileType]): type of the file. Used to preoptimize things. If it's not specified, then it will be determined by simply looking at file extension. If something doesn't work then you should change it\n
    category (str): category that is shown on loading screen\n
    skip (bool): if this resource should be ignored in preloading. Defaults to false.\n
    lazyloading (bool): if this resource should be lazy loaded. Defaults to false.\n
    forceReload (bool): if this resource should be preloaded, even if was already loaded. Defaults to False.\n
    
    """
    path: str
    saveAs: Optional[str] = None
    ofType: Optional[loadedFileType] = None
    category: str
    skip: bool = False
    lazyloading: bool = False
    forceReload: bool = False
    
    
class preloadStatusInterface(TypedDict):
    """a dict that have information about current state of preloading\n
    ------------------------\n
    category (str): name of the category that is currently loading\n
    precentCategory (float): percent of how many resources in category is loaded\n
    numberOfResourcesInCategoryLoaded (int): how many of resources in current category has been loaded\n
    numberOfResourcesInCategory (int): the total amount of all resources in current category\n
    percentWhole (float): percent of how many resources is loaded in total\n
    numberOfResourcesLoaded (int): the total number of loaded resources\n
    numberOfResources (int): the total number of resources\n
    currentResourceAs (str): the name to which the current loading resource is saving\n
    currentResourcePath (str): the path to current loading resource\n
    isLoading (bool): if it's still loading\n
    isLazyLoading (bool): if it's still lazyloading (not implemented)\n
    startTime (datetime): the start time of the loading\n
    endTime (datetime): the end time of the loading. it Doesn't include lazy loading. It's none if not completed.\n
    endTimeLazy (datetime): the end time of the lazy loading. It's none if not completed (not implemented).\n
    stopped: (bool): if the loading is stopped. It's for possibility of stopping loading (for example to stop lazy loading, if user has window minimized) (not implemented yet)
    """
    category: str
    precentCategory: float
    numberOfResourcesInCategoryLoaded: int
    numberOfResourcesInCategory: int
    precentWhole: float
    numberOfResourcesLoaded: int
    numberOfResources: int
    currentResourceAs: str
    currentResourcePath: str
    isLoading: bool
    isLazyLoading: bool
    startTime: datetime
    endTime: Optional[datetime] = None
    stopped: bool


JSONFILES = (".json")
SURFACEFILES = (".jpg")
SURFACEFILESTRANSPARENT = (".png")

class ResourceManager:
    """Single unit of resourceManager. the latest is saved automatically, but in theory you can have more than one.
        It's used to remove unnecessary loading of textures and other files.
        It also allows to load every file at the beginning to remove lags.
    """
    
    currentResourceManager: 'ResourceManager | None' = None
    
    async def preload(self, listOfItems: list[preloadResourceInformation]) -> preloadStatusInterface:
        pass
        # for item in listOfItems:
        #     self.loadRaw()
        
    
    def clean(self):
        """removes unused resources from cache
        """
        for resourceName in list(self.__rawCache.keys()):
            if resourceName != None and self.__rawCache[resourceName][1] <= 0:
                # set information about being changed
                self.__rawCache[resourceName][3][0] = True
                self.__rawCache[resourceName][3][1] = True
                
                # delete resource
                del self.__rawCache[resourceName]
        
        
    def doesResourceRawExist(self, path: str) -> bool:
        return path in self.__rawCache
         
           
    def getPointerToResourceRawChangeStatus(self, path: str) -> list[bool]:
        """ allows you to get a pointer to a specialized information about specified path
        it doesn't use dicts because it's a lot slower

        Args:
            path (str): a path to a resource

        Raises:
            accessToNotExistingResourceError: occurs if there was a try to access nonexistent resource

        Returns:
            list[IfResourceWasChanged: bool, ifResourceWasDeleted: bool]
        """
        obj = self.__rawCache.get(path)
        if obj == None:
            raise AccessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
        return obj[3]     
       
               
    def getRawUseCount(self, path: str) -> int:
        """ allows you to get current use of this resource

        Args:
            path (str): a path to a resource

        Raises:
            accessToNotExistingResourceError: occurs if there was a try to access nonexistent resource

        Returns:
            int: current use
        """
        obj = self.__rawCache.get(path)
        if obj == None:
            raise AccessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
        return obj[1]
        
    def addRawUseCount(self, path: str, howmuch: int = 1) -> int:
        """_summary_

        Args:
            path (str): a path to a resource
            howmuch (int, optional): How much to add. Defaults to 1.

        Raises:
            accessToNotExistingResourceError: occurs if there was a try to access nonexistent resource

        Returns:
            int: current use after addition
        """
        obj = self.__rawCache.get(path)
        if obj == None:
            raise AccessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
        self.__rawCache[path][1] += howmuch      
        return obj[1]
               

    def subRawUseCount(self, path: str, howmuch: int = 1) -> int:
        """_summary_

        Args:
            path (str): a path to a resource
            howmuch (int, optional): How much to subtract. Defaults to 1.

        Raises:
            accessToNotExistingResourceError: occurs if there was a try to access nonexistent resource

        Returns:
            int: current use after subtraction
        """
        obj = self.__rawCache.get(path)
        if obj == None:
            raise AccessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
        self.__rawCache[path][1] -= howmuch  
        return obj[1]    

    
    
    
    async def getRaw(self, path: str, addToUseCount: bool = False, reloadForce: bool = False) -> any:
        """allows you to get easily specified path. If it was cached, the cache is used!

        Args:
            path (str): path to the file
            addToUseCount (bool, optional): if it should add to use count (used to clean up unused space). Defaults to False.
            reloadForce (bool, optional): force reloading source, no matter if it's cached (may cause problems if that resource was used somewhere else). Defaults to False.

        Raises:
            internalResourceManagerError: _description_

        Returns:
            any: _description_
        """
        
        
        # if there no data about it in cache, load it
        if reloadForce or path not in self.__rawCache:
            await self.loadRaw(path)
            
        # get object    
        objectToReturnAndChange: list[any,int,str] | None = self.__rawCache.get(path)
        
        # if it's none, there's something not good :c
        if objectToReturnAndChange == None:
            raise InternalResourceManagerError(f"Objects for '{path}' are corrupted or do not exist!")
        
        # use count
        if addToUseCount:
            objectToReturnAndChange[1] += 1
        
        # just return the result :3
        return objectToReturnAndChange[0]
            
        
    async def loadRaw(self, path: str, forceType: loadedFileType | None = None):
        """loads resource from path

        Args:
            path (str): path to a file
            forceType (loadedFileType | None, optional): force type, if none it will be autodetected by a file extension

        Raises:
            internalResourceManagerError: If it couldn't get its way to load a resource
        """
        try:
            obj = self.__rawCache.get(path) # previous obj if there was
            
            # wrapper for seeing if a resource was changed
            wrapper: list[bool] | None = None # object to be changed after update is done
            if obj != None and type(obj) == list: # get object if there was one
                wrapper = obj[3] 
                
            # surface files for images
            if path.endswith(SURFACEFILES) or forceType == loadedFileType.pygamesurface:
                toLoad = loadImagePygame(path).convert()
                fileType = loadedFileType.pygamesurface
                
            # surface files for transparent images
            if path.endswith(SURFACEFILESTRANSPARENT) or forceType == loadedFileType.pygamesurfaceTransparent:
                toLoad = loadImagePygame(path, SRCALPHA).convert_alpha()
                fileType = loadedFileType.pygamesurfaceTransparent

            # surface files for images
            elif path.endswith(JSONFILES) or forceType == loadedFileType.json:
                toLoad = await readJSON(path)
                fileType = loadedFileType.json   
                
            
            # no other types
            else:
                async with asyncOpen(path, "r") as file:
                    toLoad = await file.read()
                fileType = loadedFileType.rawfile
                         
            # set to savedfiles
            # the last one is a list because i can't create in any other way a pointer and i want the other objects to know
            # when to reload themselves
            # toLoad = actualResource
            # 0 = used to cleaning up resourceManager, if there 0 or less it will be removed from memory
            # fileType = type of resource
            # [False] = if resource was changed. There's no pointers in python, so i needed to make this stupid workaround. Maybe it should be rewritten in c or c++ for that reason
            self.__rawCache[path] = [toLoad, 0, fileType, [False, False]]
                
            # set wrapper
            if wrapper != None:
                wrapper[0] = True
                
                
        except Exception as e:
            raise InternalResourceManagerError(f"there was internal resource manager error that went undetected!\n Error: {e}")

        
        
    
    
    def __init__(self) -> None:
        self.currentResourceManager = self
        
        
        self.__rawCache: dict[str, list[any, int, str, list[bool]]] = {}
        self.__rawCache.setdefault(None)
        

    