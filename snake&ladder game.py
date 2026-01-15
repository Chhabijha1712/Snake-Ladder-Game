import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake & Ladder - Pro Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
PURPLE = (180, 0, 180)
YELLOW = (255, 255, 0)

player_colors = [RED, BLUE, GREEN, PURPLE]

# Fonts
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)

# Board settings
CELL = 60
BOARD_OFFSET = 100

# Snakes & Ladders
snakes = {16: 6, 48: 26, 62: 18, 88: 24, 95: 56, 97: 78}
ladders = {2: 38, 7: 14, 8: 31, 15: 26, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 78: 98}

# Convert board position to coordinates
def get_position(pos):
    if pos == 0:
        return -50, -50
    row = (pos-1)//10
    col = (pos-1)%10
    if row % 2 == 1:
        col = 9 - col
    x = col * CELL + CELL//2
    y = HEIGHT - (row+1)*CELL - BOARD_OFFSET
    return x, y

# Choose number of players
def choose_players():
    while True:
        screen.fill(WHITE)
        text = big_font.render("Press 2 / 3 / 4 to Select Players", True, BLACK)
        screen.blit(text, (150, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.unicode in ['2','3','4']:
                return int(event.unicode)

# Dice animation
def roll_dice_animation():
    final_value = random.randint(1,6)
    for _ in range(15):  # cycling animation
        temp = random.randint(1,6)
        draw_screen()
        pygame.draw.rect(screen, YELLOW, (WIDTH-120, 20, 80, 80))
        number = big_font.render(str(temp), True, BLACK)
        screen.blit(number, (WIDTH-90, 45))
        pygame.display.update()
        pygame.time.delay(50)
    # show final value
    draw_screen()
    pygame.draw.rect(screen, YELLOW, (WIDTH-120, 20, 80, 80))
    number = big_font.render(str(final_value), True, BLACK)
    screen.blit(number, (WIDTH-90, 45))
    pygame.display.update()
    return final_value

# Animate player movement
def move_player(player_index, start, end):
    step = 1 if start < end else -1
    for pos in range(start + step, end + step, step):
        players[player_index] = pos
        draw_screen()
        pygame.display.update()
        pygame.time.delay(150)

# Draw board with numbers, snakes and ladders
def draw_board():
    for row in range(10):
        for col in range(10):
            x = col*CELL
            y = HEIGHT - (row+1)*CELL - BOARD_OFFSET
            color = GRAY if (row+col)%2==0 else WHITE
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))
            num = row*10 + col + 1
            if row%2==1:
                num = row*10 + (9-col)+1
            text = font.render(str(num), True, BLACK)
            screen.blit(text, (x+5, y+5))
    # Draw snakes
    for start, end in snakes.items():
        x1, y1 = get_position(start)
        x2, y2 = get_position(end)
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 4)
        pygame.draw.circle(screen, RED, (x1, y1), 8)
    # Draw ladders
    for start, end in ladders.items():
        x1, y1 = get_position(start)
        x2, y2 = get_position(end)
        pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 4)
        pygame.draw.rect(screen, GREEN, (x1-5, y1-5, 10, 10))

# Draw all players
def draw_players():
    for i, pos in enumerate(players):
        x, y = get_position(pos)
        radius = 14 if i == turn else 12  # highlight current player
        pygame.draw.circle(screen, player_colors[i], (x, y), radius)

# Draw score panel
def draw_score(turn, last_roll):
    panel_x, panel_y = 10, 10
    for i, pos in enumerate(players):
        text = font.render(f"P{i+1}: {pos}", True, player_colors[i])
        screen.blit(text, (panel_x, panel_y + i*25))
    info = font.render(f"Turn: Player {turn+1} | Last Roll: {last_roll}", True, BLACK)
    screen.blit(info, (panel_x, panel_y + len(players)*25 + 5))

# Draw everything
def draw_screen():
    screen.fill(WHITE)
    draw_board()
    draw_players()
    draw_score(turn, last_roll)
    # dice placeholder
    pygame.draw.rect(screen, YELLOW, (WIDTH-120, 20, 80, 80))
    number_text = str(last_roll) if last_roll != "-" else "-"
    number = big_font.render(number_text, True, BLACK)
    screen.blit(number, (WIDTH-90, 45))

# Main game loop
def main_game(num_players):
    global players, turn, last_roll
    players = [0]*num_players
    turn = 0
    last_roll = "-"

    while True:
        draw_screen()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice = roll_dice_animation()
                    last_roll = dice
                    start = players[turn]
                    end = start + dice

                    if end <= 100:
                        move_player(turn, start, end)
                        players[turn] = end

                        # Safe ladder move
                        if players[turn] in ladders:
                            dest = ladders[players[turn]]
                            move_player(turn, players[turn], dest)
                            players[turn] = dest

                        # Safe snake move
                        elif players[turn] in snakes:
                            dest = snakes[players[turn]]
                            move_player(turn, players[turn], dest)
                            players[turn] = dest

                    # Check win
                    if players[turn] == 100:
                        draw_screen()
                        win_text = big_font.render(f"🎉 Player {turn+1} Wins!", True, BLACK)
                        screen.blit(win_text, (200, 350))
                        pygame.display.update()
                        pygame.time.delay(4000)
                        return

                    # Next player
                    turn = (turn + 1) % num_players

# Run the game
num_players = choose_players()
players = [0]*num_players
turn = 0
last_roll = "-"
main_game(num_players)







