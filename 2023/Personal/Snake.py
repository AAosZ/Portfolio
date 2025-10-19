UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)


class Snake:
    def __init__(self, snakebody, direction):
        self.snakebody = snakebody
        self.direction = direction

    def take_step(self, position):
        for part in self.snakebody:
            part[0] += position[0]
            part[1] += position[1]

    def set_direction(self, direction):
        self.direction = direction

    def head(self):
        return self.snakebody[-1]


class Apple:
    pass


class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.snake = Snake([[0, 0], [1, 0], [2, 0], [3, 0]], 'RIGHT')

    def board(self):
        board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if [j, i] == self.snake.head():
                    row.append('X')
                elif [j, i] in self.snake.snakebody:
                    row.append('O')
                else:
                    row.append(' ')
            board.append(row)
        return board

    def render(self):
        # Debug statements
        # print("Height: " + str(self.height))
        # print("Width: " + str(self.width))

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
# create something that detects collision with itself
if __name__ == "__main__":
    game = Game(10, 30)
    game.render()
    # print(head[0] + UP[0]) debug
    while True:
        d = input("\nSnake direction: ")
        head = game.snake.head()
        if d == 'w':
            if head[0] + UP[0] >= 0 and head[1] + UP[1] >= 0 and head[0] + UP[0] <= game.height and head[1] + UP[1] <= game.width:
                if not check_valid_move(game.snake.snakebody, head[0] + UP[0], head[1] + UP[1]):
                    print("Invalid move.")
                    continue
                game.snake.set_direction('UP')
                print(head[0] + UP[0])
                print(head[1] + UP[1])
                game.snake.take_step(UP)
                game.render()
        elif d == 'd':
            if head[0] + RIGHT[0] >= 0 and head[1] + RIGHT[1] >= 0 and head[0] + RIGHT[0] <= game.height and head[1] + RIGHT[1] <= game.width:
                if not check_valid_move(game.snake.snakebody, head[0] + RIGHT[0], head[1] + RIGHT[1]):
                    print("Invalid move.")
                    continue
                print(head[0] + RIGHT[0])
                game.snake.set_direction('RIGHT')
                game.snake.take_step(RIGHT)
                game.render()
        elif d == 's':
            if head[0] + DOWN[0] >= 0 and head[1] + DOWN[1] >= 0 and head[0] + DOWN[0] <= game.height and head[1] + DOWN[1] <= game.width:
                if not check_valid_move(game.snake.snakebody, head[0] + DOWN[0], head[1] + DOWN[1]):
                    print("Invalid move.")
                    continue
                game.snake.set_direction('DOWN')
                game.snake.take_step(DOWN)
                game.render()
        elif d == 'a':
            if head[0] + LEFT[0] >= 0 and head[1] + LEFT[1] >= 0 and head[0] + LEFT[0] <= game.height and head[1] + LEFT[1] <= game.width:
                if not check_valid_move(game.snake.snakebody, head[0] + LEFT[0], head[1] + LEFT[1]):
                    print("Invalid move.")
                    continue
                print(head[0] + LEFT[0])
                print(head[1] + LEFT[1])
                game.snake.set_direction('LEFT')
                game.snake.take_step(LEFT)
                game.render()
        else:
            print("Invalid move.")
