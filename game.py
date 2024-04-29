import tkinter as tk
import random

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Three in a row")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.score = 0
        self.score_label = tk.Label(self.master, text="Очки: 0")
        self.score_label.pack()
        self.board = Board(self.canvas, self.update_score)
        self.board.draw()

    def update_score(self, points):
        self.score += points
        self.score_label.config(text="Очки: {}".format(self.score))

class Board:

    def __init__(self, canvas, update_score):
        self.canvas = canvas
        self.update_score = update_score
        self.cells = [[random.choice(['red', 'green', 'blue']) for _ in range(8)] for _ in range(8)]

    def draw(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x0, y0 = i * 50, j * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.cells[i][j], tags="square")

    def remove_lines(self, x, y):
        MIN_REMOVE_ELEMENTS = int(3)
        color = self.cells[x][y]
        connected = self.find_connected(x, y, color, [])
        if len(connected) >= MIN_REMOVE_ELEMENTS:
            for i, j in connected:
                self.cells[i][j] = ''
            self.canvas.delete("square")
            self.draw()
            self.update_score(10 * (len(connected) - 2))

    def remove_connected(self, x, y, color):
        if x < 0 or x >= 8 or y < 0 or y >= 8 or self.cells[x][y] != color:
            return
        self.cells[x][y] = ''
        self.canvas.delete("square")
        self.draw()
        self.remove_connected(x + 1, y, color)
        self.remove_connected(x - 1, y, color)
        self.remove_connected(x, y + 1, color)
        self.remove_connected(x, y - 1, color)

    def find_connected(self, x, y, color, visited):
        if x < 0 or x >= 8 or y < 0 or y >= 8 or self.cells[x][y] != color or (x, y) in visited:
            return visited
        visited.append((x, y))
        self.find_connected(x + 1, y, color, visited)
        self.find_connected(x - 1, y, color, visited)
        self.find_connected(x, y + 1, color, visited)
        self.find_connected(x, y - 1, color, visited)
        return visited

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.game = Game(self.root)
        self.game.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

    def on_click(self, event):
        x, y = event.x // 50, event.y // 50
        if self.game.board.cells[x][y] != '':
            self.game.board.remove_lines(x, y)

if __name__ == "__main__":
    Main()
