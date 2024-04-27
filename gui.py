import tkinter as tk
import random

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Игра на сбор линеек")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.create_board()
        self.score = 0
        self.score_label = tk.Label(self.master, text="Очки: 0")
        self.score_label.pack()

    def create_board(self):
        self.board = [[random.choice(['red', 'green', 'blue']) for _ in range(8)] for _ in range(8)]
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x0, y0 = i * 50, j * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.board[i][j], tags="square")

    def remove_lines(self, x, y):
        color = self.board[x][y]
        self.board[x][y] = ''
        self.canvas.delete("square")
        self.draw_board()
        self.master.update()
        self.board[x][y] = color
        self.remove_connected(x, y, color)
        if self.check_lines():
            self.score += 10
            self.score_label.config(text="Очки: {}".format(self.score))

    def remove_connected(self, x, y, color):
        if x < 0 or x >= 8 or y < 0 or y >= 8 or self.board[x][y] != color:
            return
        self.board[x][y] = ''
        self.canvas.delete("square")
        self.draw_board()
        self.master.update()
        self.remove_connected(x + 1, y, color)
        self.remove_connected(x - 1, y, color)
        self.remove_connected(x, y + 1, color)
        self.remove_connected(x, y - 1, color)

    def check_lines(self):
        for i in range(8):
            for j in range(6):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] != '':
                    return True
        for j in range(8):
            for i in range(6):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] != '':
                    return True
        return False

    def on_click(self, event):
        x, y = event.x // 50, event.y // 50
        if self.board[x][y] != '':
            self.remove_lines(x, y)

def main():
    root = tk.Tk()
    game = Game(root)
    game.canvas.bind("<Button-1>", game.on_click)
    root.mainloop()

if __name__ == "__main__":
    main()
