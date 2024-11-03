######################
# resourceManager.py #
######################

# The purpose of this module is to not reuse the same texture and waste memory and computing time

# global imports
from pygame import SRCALPHA
from pygame.surface import Surface
from pygame.image import load as loadImagePygame
from enum import Enum

# local imports
from bin.exceptions import internalResourceManagerError, accessToNotExistingResourceError
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

JSONFILES = (".json", ".jso")
SURFACEFILES = (".jpg")
SURFACEFILESTRANSPARENT = (".png")

class ResourceManager:
    """Single unit of resourceManager. the latest is saved automatically, but in theory you can have more than one.
        It's used to remove unnecessary loading of textures and other files.
        It also allows to load every file at the beginning to remove lags.
    """
    
    currentResourceManager: 'ResourceManager | None' = None
    
    
    
    def clean(self):
        """removes unused resources from cache
        """
        for resourceName, resourceObject in self.__savedFiles.items():
           if resourceObject[1] <= 0:
               del self.__savedFiles[resourceName]
               
              
              
               
    def getRawUseCount(self, path: str) -> int:
        """ allows you to get current use of this resource

        Args:
            path (str): a path to a resource

        Raises:
            accessToNotExistingResourceError: occurs if there was a try to access nonexistent resource

        Returns:
            int: current use
        """
        obj = self.__savedFiles.get(path)
        if obj != None:
            raise accessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
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
        obj = self.__savedFiles.get(path)
        if obj != None:
            raise accessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
        self.__savedFiles[path][1] += howmuch      
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
        obj = self.__savedFiles.get(path)
        if obj != None:
            raise accessToNotExistingResourceError(f"Resource {path} doesnt exist")
        
        self.__savedFiles[path][1] -= howmuch  
        return obj[1]    

    
    
    
    def getRaw(self, path: str, addToUseCount: bool = False, reloadForce: bool = False) -> any:
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
        if reloadForce or path not in self.__savedFiles:
            self.loadRaw(path)
            
        # get object    
        objectToReturnAndChange: list[any,int,str] | None = self.__savedFiles.get(path, default = None)
        
        # if it's none, there's something not good :c
        if objectToReturnAndChange == None:
            raise internalResourceManagerError(f"Objects for '{path}' are corrupted or do not exist!")
        
        # use count
        if addToUseCount:
            objectToReturnAndChange[1] += 1
        
        # just return the result :3
        return objectToReturnAndChange[0]
            
        
    def loadRaw(self, path: str, forceType: loadedFileType | None = None):
        """loads resource from path

        Args:
            path (str): path to a file
            forceType (loadedFileType | None, optional): force type, if none it will be autodetected by a file extension

        Raises:
            internalResourceManagerError: If it couldn't get its way to load a resource
        """
        try:
            obj = self.__savedFiles.get(path, default = None) # previous obj if there was
            
            # wrapper for seeing if a resource was changed
            wrapper: list[bool] | None = None # object to be changed after update is done
            if obj != None and type(obj) == dict: # get object if there was one
                wrapper = obj[4] 
                
            # surface files for images
            if path.endswith(SURFACEFILES) or forceType == loadedFileType.pygamesurface:
                toLoad = loadImagePygame(path)
                fileType = loadedFileType.pygamesurface
                
            # surface files for transparent images
            if path.endswith(SURFACEFILESTRANSPARENT) or forceType == loadedFileType.pygamesurfaceTransparent:
                toLoad = loadImagePygame(path, SRCALPHA)
                fileType = loadedFileType.pygamesurfaceTransparent

            # surface files for images
            elif path.endswith(JSONFILES) or forceType == loadedFileType.json:
                toLoad = readJSON(path)
                fileType = loadedFileType.json   
                
            
            # no other types
            else:
                with open(path, "r") as file:
                    toLoad = file.read()
                fileType = loadedFileType.rawfile
                         
            # set to savedfiles
            # the last one is a list because i can't create in any other way a pointer and i want the other objects to know
            # when to reload themselves
            # toLoad = actualResource
            # 0 = used to cleaning up resourceManager, if there 0 or less it will be removed from memory
            # fileType = type of resource
            # [False] = if resource was changed. There's no pointers in python, so i needed to make this stupid workaround. Maybe it should be rewritten in c or c++ for that reason
            self.__savedFiles[path] = [toLoad, 0, fileType, [False]]
                
            # set wrapper
            if wrapper != None:
                wrapper[3] = True
                
                
        except Exception as e:
            raise internalResourceManagerError(f"there was internal resource manager error that went undetected!\n Error: {e}")

        
        
    
    
    def __init__(self) -> None:
        self.currentResourceManager = self
        
        
        self.__savedFiles: dict[str, list[any, int, str, list[bool]]] = {}
        self.__savedFiles.setdefault(None)
        

    