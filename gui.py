import tkinter as tk
import random
import threading
import time
from game_logic import GameLogic

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Three in a Row")
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.logic = GameLogic()
        self.create_board()

        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 14), bg="#f0f0f0", fg="#000000")
        self.score_label.pack()

        self.time_label = tk.Label(self.master, text="Time: 0", font=("Helvetica", 14), bg="#f0f0f0", fg="#000000")
        self.time_label.pack()

        self.add_button = tk.Button(self.master, text="Добавить кубики", font=("Helvetica", 12), command=self.add_cubes, bg="#4caf50", fg="#000000", activebackground="#388e3c", activeforeground="#ffffff")
        self.add_button.pack(pady=5)

        self.start_time = time.time()
        self.update_time()

        self.generate_thread = threading.Thread(target=self.generate_elements)
        self.generate_thread.daemon = True
        self.generate_thread.start()

    def create_board(self):
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("square")
        for i in range(8):
            for j in range(8):
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.logic.board[i][j], tags="square", outline="#cccccc")

    def generate_elements(self):
        while True:
            time.sleep(random.randint(5, 10))
            for _ in range(random.randint(1, 5)):
                self.logic.generate_element()
            self.canvas.delete("square")
            self.draw_board()
            self.master.update()
            if self.logic.check_win():
                self.score_label.config(text="Поздравляем! Вы победили!", fg="#4caf50")
                break

    def on_click(self, event):
        x, y = event.y // 50, event.x // 50
        if self.logic.board[x][y] == 'black':
            self.explode(x, y)
        elif self.logic.board[x][y] != '':
            connected = self.logic.find_connected(x, y, self.logic.board[x][y])
            if self.logic.remove_lines(x, y):
                self.animate_removal(connected)
                self.master.update()
                self.score_label.config(text="Очки: {}".format(self.logic.score))

    def add_cubes(self):
        for _ in range(random.randint(3, 5)):
            self.logic.generate_element()
        self.canvas.delete("square")
        self.draw_board()
        self.master.update()

    def explode(self, x, y):
        cells = [(i, j) for i in range(max(0, x - 1), min(8, x + 2)) for j in range(max(0, y - 1), min(8, y + 2))]
        self.animate_removal(cells)
        self.logic.score += 50

    def animate_removal(self, cells):
        steps = 5
        delay = 50  # milliseconds

        def fade_step(step):
            color_intensity = int(240 * (steps - step) / steps) + 15
            color = f'#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}'
            for (i, j) in cells:
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="square", outline="#cccccc")
            if step < steps:
                self.master.after(delay, fade_step, step + 1)
            else:
                for (i, j) in cells:
                    self.logic.board[i][j] = ''
                self.logic.shift_down()
                self.canvas.delete("square")
                self.draw_board()

        fade_step(0)

    def update_time(self):
        elapsed_time = int(time.time() - self.start_time)
        self.time_label.config(text=f"Time: {elapsed_time}")
        self.master.after(1000, self.update_time)

def main():
    root = tk.Tk()
    root.configure(bg="#f0f0f0")
    game = GameGUI(root)
    game.canvas.bind("<Button-1>", game.on_click)
    root.mainloop()

if __name__ == "__main__":
    main()
