
import math
from array import array

import pygame
from .player import Player
from .obstacle import Obstacle

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 40

        self.player = Player(80, self.ground_y)

        self.speed = 6
        self.speed_increase_per_frame = 0.001
        self.max_speed = 12

        self.spawn_interval = 70
        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False

        # Task 4: Initialize sound effects.
        self.jump_sound = None
        self.score_sound = None
        self.game_over_sound = None
        self._init_sounds()

    def _make_tone(self, frequency, duration, volume=0.3):
        """Generate a short sound without needing external audio files."""
        sample_rate = 22050
        total_samples = int(sample_rate * duration)
        samples = array("h")

        for i in range(total_samples):
            t = i / sample_rate
            attack = min(1.0, i / max(1, int(sample_rate * 0.01)))
            release = min(
                1.0,
                (total_samples - i) / max(1, int(sample_rate * 0.03))
            )
            envelope = min(attack, release)
            sample = int(
                32767 * volume * envelope
                * math.sin(2 * math.pi * frequency * t)
            )
            samples.append(sample)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _init_sounds(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1,
                    buffer=512
                )

            self.jump_sound = self._make_tone(660, 0.10)
            self.score_sound = self._make_tone(880, 0.14)
            self.game_over_sound = self._make_tone(180, 0.35, 0.4)

        except pygame.error as error:
            # The game can still run if audio is unavailable.
            print("Sound unavailable:", error)

    def handle_event(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w)
        ):
            if self.player.on_ground:
                self.player.jump()
                if self.jump_sound:
                    self.jump_sound.play()

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.speed = min(
            self.speed + self.speed_increase_per_frame,
            self.max_speed
        )

        self.player.update()

        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.obstacles.append(
                Obstacle(self.width, self.ground_y, self.speed)
            )

        for obstacle in self.obstacles:
            obstacle.move()
            obstacle.speed = self.speed

        for obstacle in self.obstacles:
            if obstacle.rect().colliderect(self.player.rect()):
                self.game_over = True
                if self.game_over_sound:
                    self.game_over_sound.play()
                return

        for obstacle in self.obstacles:
            if (
                not obstacle.scored
                and obstacle.x + obstacle.width < self.player.x
            ):
                obstacle.scored = True
                self.score += 1
                if self.score_sound:
                    self.score_sound.play()

        self.obstacles = [
            obstacle for obstacle in self.obstacles
            if not obstacle.off_screen()
        ]

        self.distance += self.speed

    def render(self, screen):
        pygame.draw.line(
            screen, BROWN,
            (0, self.ground_y), (self.width, self.ground_y), 4
        )

        pygame.draw.rect(screen, WHITE, self.player.rect())

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, DARK_GREEN, obstacle.rect())

        score_text = self.font.render(
            f"Score: {self.score}", True, (0, 0, 0)
        )
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            title_font = pygame.font.SysFont("Arial", 48, bold=True)
            message_font = pygame.font.SysFont("Arial", 28)

            title = title_font.render(
                "GAME OVER", True, (255, 80, 80)
            )
            score = message_font.render(
                f"Final Score: {self.score}",
                True, (255, 255, 255)
            )
            restart = message_font.render(
                "Returning to menu...",
                True, (255, 255, 255)
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(self.width // 2, self.height // 2 - 60)
                )
            )
            screen.blit(
                score,
                score.get_rect(
                    center=(self.width // 2, self.height // 2)
                )
            )
            screen.blit(
                restart,
                restart.get_rect(
                    center=(self.width // 2, self.height // 2 + 50)
                )
            )
