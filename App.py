import tkinter as tk
from tkinter import messagebox
import time
import os
# Assuming MapGenerator(row, col) has .map, .mineLocation, .safetiles, .row, .column
from MapMaker import MapGenerator

class MinesweeperPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper Light")
        self.root.geometry("650x700")
        self.root.configure(bg="#F3F4F6") # Light Gray background

        # --- Game Logic ---
        self.rows, self.cols = 10, 10
        self.obj = MapGenerator(self.rows, self.cols)
        self.button_list = []
        self.grids_active = 0
        self.game_over = False
        self.start_time = time.time()
        self.highscore = self.load_highscore()

        self.setup_ui()

    def load_highscore(self):
        if not os.path.exists("highscore.txt"):
            with open("highscore.txt", "w") as f: f.write("")
        with open("highscore.txt", "r") as f:
            data = f.read().strip()
            return data if data else "N/A"

    def setup_ui(self):
        """Builds a clean, centered Light Theme UI."""
        # Top Header
        self.header = tk.Frame(self.root, bg="#FFFFFF", pady=20, bd=1, relief="solid")
        self.header.pack(fill="x", padx=20, pady=20)

        self.hiscore_label = tk.Label(self.header, text=f"Best Time: {self.highscore}s", 
                                      font=("Helvetica", 14), bg="white", fg="#374151")
        self.hiscore_label.pack()

        # Board Container (Centers the grid)
        self.board_container = tk.Frame(self.root, bg="#F3F4F6")
        self.board_container.pack(expand=True)

        for i in range(self.rows):
            row_btns = []
            for j in range(self.cols):
                btn = tk.Button(self.board_container, text="", font=("Arial", 12, "bold"), 
                                width=3, height=1, bg="#A8A8A8", relief="flat", 
                                bd=1, highlightthickness=1, highlightbackground="#D1D5DB")
                
                # Left Click to Open
                btn.config(command=lambda x=i, y=j: self.handle_click(x, y))
                
                # Right Click to Flag (Essential for Minesweeper!)
                btn.bind("<Button-3>", lambda e, x=i, y=j: self.toggle_flag(x, y))
                
                btn.grid(row=i, column=j, padx=1, pady=1)
                row_btns.append(btn)
            self.button_list.append(row_btns)

    def toggle_flag(self, x, y):
        """Right-click logic to mark potential bombs."""
        if self.game_over: return
        btn = self.button_list[x][y]
        if btn.cget("bg") == "#E5E7EB": # Only flag closed tiles
            if btn.cget("text") == "🚩":
                btn.config(text="", fg="black")
            else:
                btn.config(text="🚩", fg="#EF4444")

    def handle_click(self, x, y):
        if self.game_over or self.button_list[x][y].cget("text") == "🚩":
            return
        self.recursive_open(x, y)

    def recursive_open(self, x, y):
        btn = self.button_list[x][y]
        val = self.obj.map[x][y]

        # Base cases: already open
        if btn.cget("state") == "disabled":
            return

        # Handle Bomb
        if val == -1:
            self.trigger_game_over()
            return

        # Open Tile
        self.grids_active += 1
        btn.config(text=str(val) if val > 0 else "", state="disabled", 
                   relief="sunken", bg="#F9FAFB", fg=self.get_color(val))

        # Check Win
        if self.grids_active == self.obj.safetiles:
            self.win_game()
            return

        # Recursive Fill (Open neighbors if current is 0)
        if val == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols:
                        self.recursive_open(nx, ny)

    def get_color(self, val):
        """Standard Minesweeper number colors."""
        colors = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "maroon"}
        return colors.get(val, "black")

    def trigger_game_over(self):
        self.game_over = True
        for x, y in self.obj.mineLocation:
            self.button_list[x][y].config(text="💣", bg="#FEE2E2", state="normal")
        messagebox.showerror("BOMB!", "Boom! You hit a mine. Game Over!")

    def win_game(self):
        self.game_over = True
        total_time = int(time.time() - self.start_time)
        messagebox.showinfo("VICTORY", f"Clear! Time: {total_time}s")
        
        if self.highscore == "N/A" or total_time < int(self.highscore):
            with open("highscore.txt", "w") as f: f.write(str(total_time))
            messagebox.showinfo("New High Score!", f"{total_time}s is the new record!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperPro(root)
    root.mainloop()