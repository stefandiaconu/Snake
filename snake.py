import pygame
import random
import sys
pygame.init()

body = pygame.image.load("snake.png")
bodyrect = body.get_rect()

# Set the width and height of the screen, multiple of the body
screen_size = width, height = bodyrect.width * 30, bodyrect.height * 25
# Set the window name
pygame.display.set_caption("Snake")
# Set up the drawing window
screen = pygame.display.set_mode(screen_size)

black = 0, 0, 0
white = 255, 255, 255


def my_round(value, base=20):
    return int(value) - int(value) % int(base)


def draw_text(surf, s, size, x, y):
    # Create a font object.
    # 1st parameter is the font file which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', size)

    # Create a text surface object, on which text is drawn on it
    text = font.render('Score: ', True, white)
    score = font.render(s, True, white)

    # Create a rectangular object for the text surface object
    textRect = text.get_rect()
    scoreRect = score.get_rect()

    # Set the text to top-right of the screen
    textRect.right = width - textRect.width
    scoreRect.left = textRect.right

    surf.blit(text, textRect)
    surf.blit(score, scoreRect)


class Snake(object):
    """ This is the Snake object. """
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def set_direction(self, direction):
        self.direction = direction

    def extend_body(self, head):
        self.body.append(head)


class Apple(object):
    """ This is the Apple object"""
    def __init__(self):
        self.apple_img = pygame.image.load("apple.png")
        self.apple_rect = self.apple_img.get_rect()

    def regenerate_apple(self):
        # TODO don't create apple inside snake's body
        self.apple_rect.left = my_round(random.randint(0, width - 20))
        self.apple_rect.top = my_round(random.randint(0, height - 20))


class Game(object):
    # Set snake's direction
    DIR_UP = (0, 1)
    DIR_DOWN = (0, -1)
    DIR_LEFT = (-1, 0)
    DIR_RIGHT = (1, 0)

    # Initial speed
    speed = [20, 0]

    def __init__(self):
        # Run until the user asks to quit
        self.running = True
        # initial body of the snake
        self.init_body = []
        # Create initial body of the snake - 3 blocks
        for x in range(0, 3):
            # set the left side of each block from the snake body
            left_pos = 20 * x
            rect = pygame.Rect(left_pos, 0, 20, 20)
            self.init_body.append(rect)

        # Initialize Snake and Apple objects
        self.snake = Snake(self.init_body, self.DIR_RIGHT)
        self.apple = Apple()

    def play(self):
        self.apple.regenerate_apple()
        # Initialize the score of the game
        score = 0
        while self.running:
            # Clock
            pygame.time.delay(100)
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.snake.direction != self.DIR_LEFT:
                    self.speed = [20, 0]
                    self.snake.set_direction(self.DIR_RIGHT)
                if event.key == pygame.K_LEFT and self.snake.direction != self.DIR_RIGHT:
                    self.speed = [-20, 0]
                    self.snake.set_direction(self.DIR_LEFT)
                if event.key == pygame.K_UP and self.snake.direction != self.DIR_DOWN:
                    self.speed = [0, -20]
                    self.snake.set_direction(self.DIR_UP)
                if event.key == pygame.K_DOWN and self.snake.direction != self.DIR_UP:
                    self.speed = [0, 20]
                    self.snake.set_direction(self.DIR_DOWN)

            head = pygame.Rect(self.snake.body[-1].x, self.snake.body[-1].y, bodyrect.width, bodyrect.height)
            if head.right > width:
                head.right = 0
            elif head.bottom > height:
                head.bottom = 0
            elif head.left < 0:
                head.left = width
            elif head.top < 0:
                head.top = height
            self.move_snake(head, self.snake.direction, self.speed)

            # Flip the display
            screen.fill(black)
            for item in self.snake.body:
                screen.blit(body, item)

            screen.blit(self.apple.apple_img, self.apple.apple_rect)
            if head.colliderect(self.apple.apple_rect):
                self.snake.extend_body(head)
                self.apple.regenerate_apple()
                score += 1

            if any([head.colliderect(sp) for sp in self.snake.body[:-3]]):
                pygame.quit()
                sys.exit()

            # Copying the text surface object to the display surface object
            draw_text(screen, str(score), 20, 0, 0)

            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def move_snake(self, head, direction, snake_speed):
        if direction == self.DIR_RIGHT:
            head.x += snake_speed[0]
        elif direction == self.DIR_LEFT:
            head.x += snake_speed[0]
        elif direction == self.DIR_UP:
            head.y += snake_speed[1]
        elif direction == self.DIR_DOWN:
            head.y += snake_speed[1]
        self.snake.body.append(head)
        self.snake.body.remove(self.snake.body[0])


if __name__ == "__main__":
    game = Game()
    game.play()
