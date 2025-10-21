import random

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

class Snake:
    def __init__(self, snakebody, direction, score):
        self.snakebody = snakebody
        self.direction = direction
        self.prev_direction = direction
        self.score = score

    def take_step(self, vector, apple):
        self.prev_direction = self.direction
        self.new_direction = vector

        head = self.get_head().copy()
        new_head = [head[0] + self.new_direction[0], head[1] + self.new_direction[1]]

        eaten = False
        if apple.isapple and new_head == apple.apple:
            eaten = True
            apple.isapple = False
            self.score += 1

        self.snakebody.append(new_head)

        if not eaten:
            self.snakebody.pop(0)

    def set_direction(self, direction):
        self.direction = direction

    def get_head(self):
        return self.snakebody[-1]


class Apple:
    def __init__(self, apple):
        self.apple = apple
        self.isapple = False

    def set_position(self, snakebody):
        while True:
            y = random.randint(0, game.height - 1)
            x = random.randint(0, game.width - 1)
            overlap = False
            for part in snakebody:
                if [x, y] == part:
                    overlap = True
                    break

            if not overlap:
                self.apple = [x, y]
                self.isapple = True
                break

    def apple_onfield(self, isapple):
        self.isapple = isapple


class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.snake = Snake([[0, 0], [1, 0], [2, 0], [3, 0]], RIGHT, 0)
        self.apple = Apple(None)

    def board(self):
        board = []
        if not self.apple.isapple:
            self.apple.set_position(self.snake.snakebody)
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if [j, i] == self.snake.get_head():
                    row.append('X')
                elif [j, i] in self.snake.snakebody:
                    row.append('O')
                elif self.apple.isapple and [j, i] == self.apple.apple:
                    row.append('@')
                else:
                    row.append(' ')

            board.append(row)
        return board

    def render(self):
        board = self.board()
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(board[i][j])

        print('+', end='')
        for iii in range(self.width):
            print('-', end='')
        print('+', end='\n')

        for ii in range(self.height):
            print('|', end='')
            for iii in range(self.width):
                print(board[ii][iii], end='')
            print('|')

        print('+', end='')
        for iii in range(self.width):
            print('-', end='')
        print('+', end='')


def check_valid_move(body, x, y):
    for position in body:
        if position[0] == x and position[1] == y:
            return False
    return True

# DIRECTIONS ARE X,Y (row, col) (height, width)
if __name__ == "__main__":
    game = Game(10, 30)
    game.render()
    while True:
        d = input("\nSnake direction: ")
        head = game.snake.get_head()
        vector = RIGHT
        if d == 'w':
            vector = UP
            if head[1] + vector[1] >= 0:
                if not check_valid_move(game.snake.snakebody, head[0] + vector[0], head[1] + vector[1]):
                    if [head[0] + vector[0], head[1] + vector[1]] == game.snake.snakebody[-2]:
                        print("Invalid move.")
                        continue
                    else:
                        print("Game over. \n\nScore: " + str(game.snake.score))
                        break
                game.snake.set_direction(UP)
                game.snake.take_step(UP, game.apple)
                game.render()
            else:
                print("Game over. \n\nScore: " + str(game.snake.score))
                break
        elif d == 'd':
            vector = RIGHT
            if head[0] + vector[0] < game.width:
                if not check_valid_move(game.snake.snakebody, head[0] + vector[0], head[1] + vector[1]):
                    if [head[0] + vector[0], head[1] + vector[1]] == game.snake.snakebody[-2]:
                        print("Invalid move.")
                        continue
                    else:
                        print("Game over. \n\nScore: " + str(game.snake.score))
                        break
                game.snake.set_direction(RIGHT)
                game.snake.take_step(RIGHT, game.apple)
                game.render()
            else:
                print("Game over. \n\nScore: " + str(game.snake.score))
                break
        elif d == 's':
            vector = DOWN
            if head[1] + vector[1] < game.height:
                if not check_valid_move(game.snake.snakebody, head[0] + vector[0], head[1] + vector[1]):
                    if [head[0] + vector[0], head[1] + vector[1]] == game.snake.snakebody[-2]:
                        print("Invalid move.")
                        continue
                    else:
                        print("Game over. \n\nScore: " + str(game.snake.score))
                        break
                game.snake.set_direction(DOWN)
                game.snake.take_step(DOWN, game.apple)
                game.render()
            else:
                print("Game over. \n\nScore: " + str(game.snake.score))
                break
        elif d == 'a':
            vector = LEFT
            if head[0] + vector[0] >= 0:
                if not check_valid_move(game.snake.snakebody, head[0] + vector[0], head[1] + vector[1]):
                    if [head[0] + vector[0], head[1] + vector[1]] == game.snake.snakebody[-2]:
                        print("Invalid move.")
                        continue
                    else:
                        print("Game over. \n\nScore: " + str(game.snake.score))
                        break
                game.snake.set_direction(LEFT)
                game.snake.take_step(LEFT, game.apple)
                game.render()
            else:
                print("Game over. \n\nScore: " + str(game.snake.score))
                break
        else:
            print("Invalid move.")
