# - - - - - - - #
#    Tools.py   #
# - - - - - - - #

# 
# [!] The functions will be improved and more developed
#

# Imports
import json, pygame
from os import getcwd, path
from typing import Any
from aiofiles import open as asyncOpen

# Local imports
import bin.exceptions as e

# Check if the document path ends with an extension of .json
def isJSONFile(document_path: str) -> bool:
    return document_path.endswith('.json')

# Asynchronous function to read json file and return the content in form of dict
async def readJSON(document_path: str) -> dict:
    if not isJSONFile(document_path):
        raise e.JSONInvalidFileError('Attempted to read a non-json file!')

    async with asyncOpen(file=path.join(getcwd(), document_path), mode='r', encoding='UTF-8') as file:
        content = await file.read()

    return json.loads(content)

# Asynchronous function to write json file
async def writeJSON(document_path: str, json_pyobj: dict) -> None:
    if not isJSONFile(document_path):
        raise e.JSONInvalidFileError('Attempted to write to a non-json file!')

    with asyncOpen(file=path.join(getcwd(), document_path), mode='w', encoding='UTF-8') as file:
        stringified_json = json.dumps(json_pyobj, indent=4)

        await file.write(stringified_json)

# Asynchronous function to create an empty json file
async def createJSON(document_destination: str, json_pyobj: dict = {}) -> None:
    if not isJSONFile(document_destination):
        raise e.JSONInvalidFileError('Attempted to create a non-json file!')
    
    async with asyncOpen(file=path.join(getcwd(), document_destination), mode='x', encoding='UTF-8') as file:
        stringified_json = json.dumps(json_pyobj, indent=4)

        await file.write(stringified_json)

# Function to load an image and return it as a pygame.Surface object
def readImage(image_path: str, scale: float = 1.0, uses_alpha: int = False) -> pygame.Surface:
    full_path = getcwd() + image_path

    image = pygame.image.load(full_path)

    if uses_alpha:
        image = image.convert_alpha()

    if scale < 0.0:
        raise ValueError('Attempted to use a negative factor for scaling the image!')
    
    image = pygame.transform.scale_by(image, scale)

    return image