import random

COLORS = ['red', 'green', 'blue', 'yellow']


class GameLogic:
    def __init__(self):
        self.board = [[random.choice(COLORS) for _ in range(8)] for _ in range(8)]
        self.score = 0

    def remove_lines(self, x, y):
        color = self.board[x][y]
        connected = self.find_connected(x, y, color)
        if len(connected) >= 3:
            for i, j in connected:
                self.board[i][j] = ''
            self.shift_down()
            self.score += 10 * (len(connected) - 2)
            if len(connected) > 4:
                self.generate_bomb()
            return True
        return False

    def find_connected(self, x, y, color):
        visited = set()
        stack = [(x, y)]
        connected = []

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            if cx < 0 or cx >= 8 or cy < 0 or cy >= 8 or self.board[cx][cy] != color:
                continue
            connected.append((cx, cy))
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

        return connected

    def shift_down(self):
        for j in range(8):
            k = 0
            for i in range(7, -1, -1):
                if self.board[i][j] == '':
                    k += 1
                elif k > 0:
                    self.board[i + k][j] = self.board[i][j]
                    self.board[i][j] = ''

    def generate_element(self):
        empty_cells = [j for j in range(8) if self.board[0][j] == '']
        if empty_cells:
            col = random.choice(empty_cells)
            self.board[0][col] = random.choice(COLORS)
            for i in range(1, 8):
                if self.board[i][col] != '':
                    break
                self.board[i][col], self.board[i - 1][col] = self.board[i - 1][col], self.board[i][col]

    def generate_bomb(self):
        empty_cells = [j for j in range(8) if self.board[0][j] == '']
        if empty_cells:
            col = random.choice(empty_cells)
            self.board[0][col] = 'black'

    def check_win(self):
        for row in self.board:
            if any(cell != '' for cell in row):
                return False
        return True
