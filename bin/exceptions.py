# - - - - - - - - - - #
#    exceptions.py    #
# - - - - - - - - - - #

# Custom JSON related exceptions
class JSONReadFileError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class JSONWriteFileError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class JSONInvalidFileError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class JSONCreateFileError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


# Custom components related exceptions
class ComponentInitError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

# exceptions related to accessing things that you were not supposed to access or using wrong type
class ConstantChangeError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        
class InvalidTypeError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        
        
# resourceManager errors
class InternalResourceManagerError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        
class AccessToNotExistingResourceError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)

# Custom game files related exceptions
class UnavailableFontError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

# TODO: Add more exceptions