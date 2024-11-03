import asyncio, pygame

pygame.init()


async def main():
    
    print(pygame.get_init())

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())