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

# Custom game files related exceptions
# TODO: Add more exceptions