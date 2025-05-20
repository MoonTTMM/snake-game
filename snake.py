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

font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 25)

def draw_block(color, pos):
    rect = pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, color, rect)

def random_food():
    x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return (x, y)

def main():
    # 玩家1（绿色蛇）
    snake1 = [(100, 100), (80, 100), (60, 100)]
    direction1 = 'RIGHT'
    score1 = 0
    # 玩家2（蓝色蛇）
    snake2 = [(300, 300), (320, 300), (340, 300)]
    direction2 = 'LEFT'
    score2 = 0
    food = random_food()
    running = True
    
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # 玩家1：方向键
                if event.key == pygame.K_UP and direction1 != 'DOWN':
                    direction1 = 'UP'
                elif event.key == pygame.K_DOWN and direction1 != 'UP':
                    direction1 = 'DOWN'
                elif event.key == pygame.K_LEFT and direction1 != 'RIGHT':
                    direction1 = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction1 != 'LEFT':
                    direction1 = 'RIGHT'
                # 玩家2：WASD
                elif event.key == pygame.K_w and direction2 != 'DOWN':
                    direction2 = 'UP'
                elif event.key == pygame.K_s and direction2 != 'UP':
                    direction2 = 'DOWN'
                elif event.key == pygame.K_a and direction2 != 'RIGHT':
                    direction2 = 'LEFT'
                elif event.key == pygame.K_d and direction2 != 'LEFT':
                    direction2 = 'RIGHT'

        # 玩家1移动
        head1_x, head1_y = snake1[0]
        if direction1 == 'UP':
            head1_y -= BLOCK_SIZE
        elif direction1 == 'DOWN':
            head1_y += BLOCK_SIZE
        elif direction1 == 'LEFT':
            head1_x -= BLOCK_SIZE
        elif direction1 == 'RIGHT':
            head1_x += BLOCK_SIZE
        new_head1 = (head1_x, head1_y)

        # 玩家2移动
        head2_x, head2_y = snake2[0]
        if direction2 == 'UP':
            head2_y -= BLOCK_SIZE
        elif direction2 == 'DOWN':
            head2_y += BLOCK_SIZE
        elif direction2 == 'LEFT':
            head2_x -= BLOCK_SIZE
        elif direction2 == 'RIGHT':
            head2_x += BLOCK_SIZE
        new_head2 = (head2_x, head2_y)

        # --- 碰撞判定 ---
        loser = None
        # 玩家1撞墙
        if head1_x < 0 or head1_x >= WIDTH or head1_y < 0 or head1_y >= HEIGHT:
            loser = 1
        # 玩家2撞墙
        if head2_x < 0 or head2_x >= WIDTH or head2_y < 0 or head2_y >= HEIGHT:
            loser = 2 if loser is None else 0
        # 玩家1撞自己
        if new_head1 in snake1[1:]:
            loser = 1 if loser is None else 0
        # 玩家2撞自己
        if new_head2 in snake2[1:]:
            loser = 2 if loser is None else 0
        # 玩家1撞玩家2
        if new_head1 in snake2:
            loser = 1 if loser is None else 0
        # 玩家2撞玩家1
        if new_head2 in snake1:
            loser = 2 if loser is None else 0
        # 玩家1和玩家2头部重叠
        if new_head1 == new_head2:
            loser = 0
        if loser is not None:
            running = False
            break

        # 先插入新头
        snake1.insert(0, new_head1)
        snake2.insert(0, new_head2)

        # 吃食物判定（后续完善得分归属）
        if new_head1 == food:
            score1 += 1
            food = random_food()
        else:
            snake1.pop()
        if new_head2 == food:
            score2 += 1
            food = random_food()
        else:
            snake2.pop()

        # 绘制
        window.fill(BLACK)
        for block in snake1:
            draw_block(GREEN, block)
        for block in snake2:
            draw_block((0, 128, 255), block)  # 蓝色蛇
        draw_block(RED, food)
        score_text1 = font.render(f'玩家1得分: {score1}', True, WHITE)
        score_text2 = font.render(f'玩家2得分: {score2}', True, WHITE)
        window.blit(score_text1, (10, 10))
        window.blit(score_text2, (WIDTH - 180, 10))
        pygame.display.flip()

    # 游戏结束提示
    if 'loser' in locals():
        if loser == 1:
            game_over_text = font.render('玩家1失败，按任意键退出', True, WHITE)
        elif loser == 2:
            game_over_text = font.render('玩家2失败，按任意键退出', True, WHITE)
        else:
            game_over_text = font.render('平局，按任意键退出', True, WHITE)
    else:
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
