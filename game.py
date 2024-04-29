import tkinter as tk
import random
import threading
import time

class GameLogic:
    def __init__(self):
        self.board = [[random.choice(['red', 'green', 'blue', '']) for _ in range(20)] for _ in range(20)]
        self.score = 0

    def remove_lines(self, x, y):
        color = self.board[x][y]
        connected = self.find_connected(x, y, color, [])
        if len(connected) >= 3:
            for i, j in connected:
                self.board[i][j] = ''
            self.score += 10 * (len(connected) - 2)
            return True
        return False

    def find_connected(self, x, y, color, visited):
        if x < 0 or x >= 20 or y < 0 or y >= 20 or self.board[x][y] != color or (x, y) in visited:
            return visited
        visited.append((x, y))
        self.find_connected(x + 1, y, color, visited)
        self.find_connected(x - 1, y, color, visited)
        self.find_connected(x, y + 1, color, visited)
        self.find_connected(x, y - 1, color, visited)
        return visited

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Three in a row")
        self.canvas = tk.Canvas(self.master, width=1000, height=1000)
        self.canvas.pack()
        self.logic = GameLogic()
        self.create_board()

        self.score_label = tk.Label(self.master, text="Очки: 0")
        self.score_label.pack()

        self.generate_thread = threading.Thread(target=self.generate_elements)
        self.generate_thread.daemon = True
        self.generate_thread.start()

    def create_board(self):
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(20):
            for j in range(20):
                x0, y0 = i * 50, j * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.logic.board[i][j], tags="square")

    def generate_elements(self):
        while True:
            time.sleep(20)
            empty_cells = [(i, j) for i in range(20) for j in range(20) if self.logic.board[i][j] == '']
            num_to_fill = len(empty_cells) // 2
            cells_to_fill = random.sample(empty_cells, num_to_fill)
            for i, j in cells_to_fill:
                self.logic.board[i][j] = random.choice(['red', 'green', 'blue'])
            self.canvas.delete("square")
            self.draw_board()
            self.master.update()

    def on_click(self, event):
        x, y = event.x // 50, event.y // 50
        if self.logic.board[x][y] != '':
            if self.logic.remove_lines(x, y):
                self.canvas.delete("square")
                self.draw_board()
                self.master.update()
                self.score_label.config(text="Очки: {}".format(self.logic.score))

def main():
    root = tk.Tk()
    game = GameGUI(root)
    game.canvas.bind("<Button-1>", game.on_click)
    root.mainloop()

if __name__ == "__main__":
    main()
