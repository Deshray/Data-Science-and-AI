import pygame
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Momentum Animation')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

mass = float(input("Enter the mass (kg): "))
initial_velocity = float(input("Enter the initial velocity (m/s): "))
angle = float(input("Enter the angle above the horizontal (degrees, 0-90): "))

angle_rad = math.radians(angle)

vx = initial_velocity * math.cos(angle_rad)
vy = -initial_velocity * math.sin(angle_rad)

x, y = WIDTH // 2, HEIGHT // 2

dt = 0.02

restitution = 0.9

momentum_threshold = 0.1

time.sleep(5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += vx * dt * 50
    y += vy * dt * 50

    if x <= 20 or x >= WIDTH - 20:
        vx = -vx * restitution
        x = max(20, min(WIDTH - 20, x))

    if y <= 20 or y >= HEIGHT - 20:
        vy = -vy * restitution
        y = max(20, min(HEIGHT - 20, y))

    vx *= 0.99
    vy *= 0.99

    momentum = mass * math.sqrt(vx**2 + vy**2)

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 5)

    pygame.draw.circle(screen, RED, (int(x), int(y)), 20)

    pygame.display.flip()

    if momentum < momentum_threshold:
        running = False

    pygame.time.delay(10)

pygame.quit()
