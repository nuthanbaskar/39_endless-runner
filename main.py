
import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner - Pygame Version")

SKY = (200, 220, 240)
clock = pygame.time.Clock()
FPS = 60


def choose_difficulty():
    font = pygame.font.SysFont("Arial", 30)
    options = [
        ("Easy", 4, 90),
        ("Medium", 6, 70),
        ("Hard", 9, 50),
    ]

    while True:
        SCREEN.fill(SKY)
        title = font.render("Choose Difficulty", True, (0, 0, 0))
        SCREEN.blit(title, title.get_rect(center=(WIDTH // 2, 90)))

        for i, (name, _, _) in enumerate(options):
            text = font.render(
                f"{i + 1}. {name}", True, (0, 0, 0)
            )
            SCREEN.blit(
                text,
                text.get_rect(center=(WIDTH // 2, 160 + i * 45))
            )

        exit_text = font.render("E. Exit", True, (0, 0, 0))
        SCREEN.blit(
            exit_text,
            exit_text.get_rect(center=(WIDTH // 2, 320))
        )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    return options[0]
                if event.key in (pygame.K_2, pygame.K_KP2):
                    return options[1]
                if event.key in (pygame.K_3, pygame.K_KP3):
                    return options[2]
                if event.key == pygame.K_e:
                    return None

        clock.tick(FPS)


def main():
    running = True

    while running:
        difficulty = choose_difficulty()
        if difficulty is None:
            break

        name, start_speed, spawn_interval = difficulty
        engine = GameEngine(WIDTH, HEIGHT)
        engine.speed = start_speed
        engine.spawn_interval = spawn_interval

        while running:
            SCREEN.fill(SKY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    engine.handle_event(event)

            if not running:
                break

            engine.handle_input()
            engine.update()
            engine.render(SCREEN)
            pygame.display.flip()
            clock.tick(FPS)

            if engine.game_over:
                pygame.time.wait(1200)
                break

    pygame.quit()


if __name__ == "__main__":
    main()
