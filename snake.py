import pygame
import sys
import random

# 游戏窗口大小
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 初始化
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇 Snake Game')
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 25)

def draw_block(color, pos):
    rect = pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, color, rect)

def random_food():
    x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return (x, y)

def main():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = 'RIGHT'
    food = random_food()
    score = 0
    running = True

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # 移动蛇
        head_x, head_y = snake[0]
        if direction == 'UP':
            head_y -= BLOCK_SIZE
        elif direction == 'DOWN':
            head_y += BLOCK_SIZE
        elif direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head_x += BLOCK_SIZE
        new_head = (head_x, head_y)

        # 判断碰撞
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake
        ):
            running = False
            continue

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()

        # 绘制
        window.fill(BLACK)
        for block in snake:
            draw_block(GREEN, block)
        draw_block(RED, food)
        score_text = font.render(f'得分: {score}', True, WHITE)
        window.blit(score_text, (10, 10))
        pygame.display.flip()

    # 游戏结束
    game_over_text = font.render('游戏结束，按任意键退出', True, WHITE)
    window.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(1000)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
