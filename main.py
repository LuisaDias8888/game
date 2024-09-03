import pygame
import random
import time

# Inicializar o Pygame
pygame.init()

# Definir cores
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)

# Configurar a tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Elite Colégio")

# Carregar fontes
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 30)

# Configurar o jogo
clock = pygame.time.Clock()
monitor_speed = 5
game_duration = 15  # segundos

# Função para criar crianças com roupas de cores aleatórias
def create_child(incorrect_uniform):
    color = random.choice([GREEN, RED, PURPLE]) if incorrect_uniform else ORANGE
    return pygame.Surface((30, 30)), color

# Função para desenhar texto na tela
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Função para desenhar o fundo da escola (simplificado)
def draw_background():
    pygame.draw.rect(screen, BLACK, [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.draw.rect(screen, WHITE, [50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100])
    pygame.draw.rect(screen, BLACK, [50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100])  # Área de refeitório

# Função para verificar colisão com crianças
def check_collision(monitor_rect, children):
    for child in children:
        if monitor_rect.colliderect(child['rect']):
            return child
    return None

def game_loop():
    monitor_x, monitor_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    monitor_image = pygame.Surface((50, 50))
    monitor_image.fill(ORANGE)  # Monitora com blusa laranja

    children = []
    for _ in range(55):
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = random.randint(0, SCREEN_HEIGHT - 30)
        surface, color = create_child(True)
        surface.fill(color)
        children.append({'rect': pygame.Rect(x, y, 30, 30), 'surface': surface})

    for _ in range(15):
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = random.randint(0, SCREEN_HEIGHT - 30)
        surface, color = create_child(False)
        surface.fill(color)
        children.append({'rect': pygame.Rect(x, y, 30, 30), 'surface': surface})

    start_time = time.time()
    running = True
    captured_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            monitor_x -= monitor_speed
        if keys[pygame.K_RIGHT]:
            monitor_x += monitor_speed
        if keys[pygame.K_UP]:
            monitor_y -= monitor_speed
        if keys[pygame.K_DOWN]:
            monitor_y += monitor_speed

        # Atualizar a tela
        screen.fill(WHITE)
        draw_background()
        
        # Desenhar a monitora
        monitor_rect = pygame.Rect(monitor_x, monitor_y, 50, 50)
        screen.blit(monitor_image, monitor_rect.topleft)

        # Desenhar crianças
        for child in children:
            screen.blit(child['surface'], child['rect'].topleft)

        # Verificar colisões
        collided_child = check_collision(monitor_rect, children)
        if collided_child:
            if collided_child['surface'].get_at((0, 0)) != ORANGE:  # Se não é laranja
                collided_child['surface'].fill(ORANGE)  # Trocar para laranja
                captured_count += 1
                draw_text('A', small_font, BLACK, collided_child['rect'].x, collided_child['rect'].y)

        # Checar tempo restante
        elapsed_time = time.time() - start_time
        remaining_time = max(0, game_duration - elapsed_time)
        draw_text(f'Tempo restante: {int(remaining_time)}s', small_font, BLACK, 10, 10)

        if remaining_time <= 0:
            if captured_count == 55:
                screen.fill(WHITE)
                draw_text("BOM TRABALHO, VOCÊ É UM INSPETOR ELITE", font, BLACK, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50)
                pygame.display.flip()
                pygame.time.wait(3000)
            return

        pygame.display.flip()
        clock.tick(30)

# Rodar o jogo
while True:
    game_loop()
