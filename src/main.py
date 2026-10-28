from sys import exit
import components
import config
import population
import pygame

pygame.init()
clock = pygame.time.Clock()
population = population.Population(100)

def generate_pipes():
    config.pipes.append(components.Pipe(config.winWidth))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipesSpawnTime = 10

    while True:

        quit_game()

        config.window.fill((0, 0, 0))

        # Spawn Ground
        config.ground.draw(config.window)

        # Spawn Pipes
        if pipesSpawnTime <= 0:
            generate_pipes()
            pipesSpawnTime = 200
        pipesSpawnTime -= 2

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.offScreen:
                config.pipes.remove(p)

        if not population.extinct():
            population.update_live_players()

        else:
            config.pipes.clear()
            population.natural_selection()

        clock.tick(60)
        pygame.display.flip()

main()