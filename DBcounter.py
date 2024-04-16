import tkinter as tk
from tkinter import ttk
import keyboard  # Import the keyboard library

class BombTrackerApp:
    def __init__(self, master):
        self.master = master
        self.current_player = 1
        self.selected_players = {1, 2, 3, 4, 5, 6, 7, 8}  # Default: all players selected
        self.key_bind = 'Caps Lock'  # Default key bind changed to 'Caps Lock'
        self.timer_count = 20
        self.timer_label = None
        self.timer_running = False
        self.timer_id = None  # To store the timer ID for stopping

        self.tabs = ttk.Notebook(master)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.game_tab = tk.Frame(self.tabs)
        self.settings_tab = tk.Frame(self.tabs)

        self.tabs.add(self.game_tab, text="Game")
        self.tabs.add(self.settings_tab, text="Settings")

        self.label_text = tk.Label(self.game_tab, text="Current Player:", font=("Arial", 18))
        self.label_text.pack()

        self.label_number = tk.Label(self.game_tab, text=self.current_player, font=("Arial", 48), fg="red")
        self.label_number.pack(pady=20)

        self.next_button = tk.Button(self.game_tab, text="Next Player", command=self.next_player, font=("Arial", 18))
        self.next_button.pack()

        self.reset_button = tk.Button(self.game_tab, text="Reset", command=self.reset_game, font=("Arial", 12))
        self.reset_button.pack()

        self.timer_label = tk.Label(self.game_tab, text=f"Time left: {self.timer_count} seconds", font=("Arial", 18))
        self.timer_label.pack(side=tk.RIGHT)

        self.key_label = tk.Label(self.settings_tab, text="Key Bind:")
        self.key_label.pack(anchor=tk.W)

        self.key_entry = tk.Entry(self.settings_tab)
        self.key_entry.insert(0, self.key_bind)
        self.key_entry.pack()

        self.player_checkboxes = []
        for player_num in range(1, 9):
            var = tk.IntVar(value=1 if player_num in self.selected_players else 0)  # Default selection
            checkbox = tk.Checkbutton(self.settings_tab, text=f"Player {player_num}", variable=var)
            checkbox.pack(anchor=tk.W)
            self.player_checkboxes.append(var)

        self.apply_settings_button = tk.Button(self.settings_tab, text="Apply Settings", command=self.apply_settings)
        self.apply_settings_button.pack(pady=10)

        # Use the 'keyboard' library to bind global key events
        keyboard.on_press_key(self.key_bind.lower(), self.key_pressed)

    def next_player(self):
        if not self.selected_players:
            return

        self.current_player += 1
        while self.current_player not in self.selected_players:
            self.current_player += 1
            if self.current_player > 8:
                self.current_player = 1
        
        self.label_number.config(text=self.current_player)
        self.timer_count = 20
        self.timer_label.config(text=f"Time left: {self.timer_count} seconds")
        self.game_tab.config(bg="white")  # Change background color of game tab back to default

        # Stop the old timer before starting a new one
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.start_timer()

    def apply_settings(self):
        self.selected_players = {i+1 for i, var in enumerate(self.player_checkboxes) if var.get() == 1}
        self.key_bind = self.key_entry.get()

    def key_pressed(self, event):
        self.next_player()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer_count -= 1
            self.timer_label.config(text=f"Time left: {self.timer_count} seconds")

            if self.timer_count == 0:
                self.timer_running = False
                self.game_tab.config(bg="blue")  # Change background color of game tab to blue when timer hits 0
            else:
                self.timer_id = self.master.after(1000, self.update_timer)

    def reset_game(self):
        self.current_player = 1
        self.label_number.config(text=self.current_player)
        self.timer_count = 20
        self.timer_label.config(text=f"Time left: {self.timer_count} seconds")
        self.game_tab.config(bg="white")  # Reset background color to default
        self.timer_running = False
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

root = tk.Tk()
root.title("Bomb Tracker")
app = BombTrackerApp(root)
root.mainloop()
