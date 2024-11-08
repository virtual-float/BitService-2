# Imports
import asyncio, pygame
from typing import Final
from os import path, getcwd

# Local imports
import bin.fonts as font
import bin.tools as tools
import bin.resourceManager as rsPackage

pygame.init()
pygame.font.init()
pygame.mixer.init()


async def main():
    rs = rsPackage.ResourceManager()
    
    # TODO: Add a loading screen window
    # app_resource: Final[dict] = await tools.readJSON('\\config\\default.json')
    app_resource: Final[dict] = await rs.getRaw(path.join("config", "default.json"), True)
    
    # tests (you can delete this later on)
    pointer: list[bool, bool] = rs.getPointerToResourceRawChangeStatus(path.join("config", "default.json"))
    app_resource2: Final[dict] = await rs.getRaw(path.join("config", "default.json"), True)
    print("czy to jest ten sam obiekt: ", app_resource2 is app_resource2)
    print(f"pointers: {pointer}")
    l = rs.getRawUseCount(path.join("config", "default.json"))
    print(f"ilość użyć: {l}")


    display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(app_resource.get('title'))

    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        
        display.fill((0, 0, 0))

        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())