# Imports
import asyncio, pygame
from typing import Final

# Local imports
import bin.fonts as font
import bin.tools as tools

pygame.init()
pygame.font.init()
pygame.mixer.init()


async def main():
    # TODO: Add a loading screen window
    app_resource: Final[dict] = await tools.readJSON('\\config\\default.json')

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