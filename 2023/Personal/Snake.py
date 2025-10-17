DIRECTIONS = {
    'UP': (0, 1),
    'RIGHT': (1, 0),
    'DOWN': (0, -1),
    'LEFT': (-1, 0),
}

class Snake():
    def __init__(self, initialize_snake, initialize_direction):
        self.initialize_snake = initialize_snake
        self.initialize_direction = initialize_direction

    def take_step(self, position):
        self.take_step = self.initialize_snake[1:] + [position]

    def set_direction(self, direction):
        self.set_direction = direction

    def head(self):
        return self.initialize_snake[-1]


class Apple():
    pass

class Game():
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.snake = Snake([(0, 0), (1, 0), (2, 0), (3, 0)], 'UP')


    def board(self):
        board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (j, i) == self.snake.head():
                    row.append('X')
                elif (j, i) in self.snake.initialize_snake:
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


        print('+', end = '')
        for iii in range(self.width):
            print('-', end='')
        print('+', end='\n')

        for ii in range(self.height):
            print('|', end='')
            for iii in range(self.width):
                print(board[ii][iii], end='')
            print('|')

        print('+', end = '')
        for iii in range(self.width):
            print('-', end='')
        print('+', end='')

if __name__ == "__main__":
    game = Game(10, 20)
    game.render()
    while True:
        d = input("\nSnake direction: ")
        for i in range(game.height):
            for j in range(game.width):
                if i < 0 or i >= game.height or j < 0 or j >= game.width:
                    if d == 'w':
                        game.snake.set_direction('UP')
                        game.snake.take_step((0, 1))
                        game.render()
                    if d == 'd':
                        game.snake.set_direction('RIGHT')
                        game.snake.take_step((1, 0))
                        game.render()
                    if d == 's':
                        game.snake.set_direction('DOWN')
                        game.snake.take_step((0, -1))
                        game.render()
                    if d == 'a':
                        game.snake.set_direction('LEFT')
                        game.snake.take_step((-1, 0))
                        game.render()
                print("Invalid move.")
