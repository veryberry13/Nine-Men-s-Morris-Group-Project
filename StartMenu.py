import subprocess
import tkinter as tk


class GameInstructions:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Instructions")
        self.window.geometry("800x600")
        self.window.configure(background="#FFFFCC")

        instructions_text = """Nine Men's Morris Game Instructions:
        
        The game proceeds in three phases:
        
        1. Placing men on vacant points.
        2. Moving men to adjacent points.
        3. (Flying phase) Moving men to any vacant point when the player has been reduced to three men.
        
        Game Objective:
        
        - Try to form a mill, so that you can remove the opponent's men.
        - To win, reduce the opponent's men to two.
        - To win, make the opponent make a move.
        
        Have fun playing Nine Men's Morris!
        """

        instructions_label = tk.Label(self.window, text=instructions_text, font=("Arial", 16), justify="left")
        instructions_label.pack(pady=20, padx=20, anchor="w")

        back_button = tk.Button(self.window, text="Back", font=("Arial", 24), bg="#FFCCCC", command=self.go_back, width=10)
        back_button.pack(pady=10)

    def go_back(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

class GameModes:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Modes")
        self.window.geometry("800x600")
        self.window.configure(background="yellow")

        font_large = ("Arial", 24)

        button_width = 15  # Set a common width for all buttons

        button1 = tk.Button(self.window, text="Human vs Human", font=font_large, bg="pink", command=self.human_vs_human, width=button_width)
        button2 = tk.Button(self.window, text="Human vs Computer", font=font_large, bg="#CCCCFF", command=self.human_vs_computer, width=button_width)
        button3 = tk.Button(self.window, text="Nine Men's Morris", font=font_large, bg="#CCFFCC", command=self.nine_mens_morris, width=button_width)
        exit_button = tk.Button(self.window, text="Exit", font=font_large, bg="red", command=self.window.destroy, width=button_width)
        rules_button = tk.Button(self.window, text="Rules", font=font_large, bg="orange", command=self.show_game_instructions, width=button_width)

        button1.pack(pady=10)
        button2.pack(pady=10)
        button3.pack(pady=10)
        rules_button.pack(pady=10)
        exit_button.pack(pady=10)

    def human_vs_human(self):
        subprocess.Popen(['python', 'NineMensMorris_front_end.py'])
        print("Starting Human vs Human Game")

    def human_vs_computer(self):
        print("Starting Human vs Computer Game")

    def nine_mens_morris(self):
        print("Starting Nine Men's Morris Game")

    def show_game_instructions(self):
        game_instructions = GameInstructions()
        game_instructions.run()

class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Start Menu")
        self.geometry("800x600")
        self.configure(background="#87CEEB")

        title_font = ("Arial", 48, "bold")
        button_font = ("Arial", 18)

        self.title_label = tk.Label(self, text="Nine Men's Morris", font=title_font)
        self.title_label.pack(pady=20)

        self.new_game_button = tk.Button(self, text="New Game", font=button_font, command=self.show_new_game_options, width=15)
        self.new_game_button.pack(pady=10)

        self.rules_button = tk.Button(self, text="Rules", font=button_font, command=self.show_game_instructions, width=15)
        self.rules_button.pack(pady=10)

        self.load_game_button = tk.Button(self, text="Load Game", font=button_font, width=15)
        self.load_game_button.pack(pady=10)

        self.exit_button = tk.Button(self, text="Exit Game", font=button_font, command=self.quit, width=15)
        self.exit_button.pack(pady=10)

    def show_game_instructions(self):
        game_instructions = GameInstructions()
        game_instructions.run()

    def show_new_game_options(self):
        new_game_window = GameModes()

if __name__ == "__main__":
    app = StartMenu()
    app.mainloop()
