# Imports
import asyncio, pygame

# Local imports
import bin.fonts as font


async def main():
    pygame.init()

    display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test")

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