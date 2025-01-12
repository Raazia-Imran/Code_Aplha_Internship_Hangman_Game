import tkinter as tk
from tkinter import messagebox
import json
import random

# Hangman stages (text-based for simplicity)
hangman_stages = [
    """ 
     ----- 
     |   | 
         | 
         | 
         | 
         | 
    ========
    """,
    """ 
     ----- 
     |   | 
     O   | 
         | 
         | 
         | 
    ========
    """,
    """ 
     ----- 
     |   | 
     O   | 
     |   | 
         | 
         | 
    ========
    """,
    """ 
     ----- 
     |   | 
     O   | 
    /|   | 
         | 
         | 
    ========
    """,
    """ 
     ----- 
     |   | 
     O   | 
    /|\\  | 
         | 
         | 
    ========
    """,
    """ 
     ----- 
     |   | 
     O   | 
    /|\\  | 
    /    | 
         | 
    ========
    """,
    """ 
     ----- 
     |   | 
     O   | 
    /|\\  | 
    / \\  | 
         | 
    ========
    """
]

# Word categories (abbreviated for brevity)
# Expanded word categories (35 words for each difficulty level)
categories = {
    "animals": {
        "easy": ["cat", "dog", "bat", "fox", "cow", "rat", "horse", "wolf", "sheep", "goat", "lion", "elephant",
                 "mouse", "zebra", "tiger", "deer", "panda", "rabbit", "bear", "monkey", "leopard", "snake", "whale",
                 "dolphin", "eagle", "owl", "turtle", "shark", "parrot", "kangaroo", "koala", "otter", "rhino",
                 "hippo", "camel", "crocodile"],
        "medium": ["elephant", "kangaroo", "giraffe", "puma", "cheetah", "alligator", "buffalo", "zebra", "hyena",
                   "orca", "pelican", "gibbon", "pangolin", "platypus", "dromedary", "walrus", "coyote", "porcupine",
                   "armadillo", "bison", "moose", "giraffe", "capybara", "sloth", "ibex", "manatee", "pronghorn",
                   "wolverine", "flamingo", "condor", "scorpion", "mole", "swan", "crane", "caterpillar", "anaconda"],
        "hard": ["anaconda", "piranha", "chinchilla", "gecko", "geoffroys-tamarin", "meerkat", "narwhal", "red-fox",
                 "rattlesnake", "tapir", "capuchin", "serval", "frilled-lizard", "hairy-dasiy", "wild-dog", "red-panda",
                 "dhole", "serval-cat", "quokka", "platypus", "thorny-devil", "sandcat", "arctic-fox", "water-buffalo",
                 "common-pangolin", "clouded-leopard", "honey-badger", "anteater", "fossa", "firefly", "cuttlefish",
                 "tree-frog", "blind-platypus", "bat-eared-fox", "vulture"],
    },
    "sports": {
        "easy": ["soccer", "tennis", "golf", "swim", "cricket", "basketball", "football", "rugby", "hockey", "volleyball",
                 "baseball", "squash", "pingpong", "badminton", "boxing", "wrestling", "karate", "skateboarding",
                 "archery", "climbing", "yoga", "gymnastics", "cycling", "skiing", "swimming", "running", "hurdles",
                 "rowing", "triathlon", "jumping", "long-jump", "shot-put", "discus", "relay", "track"],
        "medium": ["basketball", "volleyball", "hockey", "fencing", "cricket", "ping-pong", "crossfit", "gymnastics",
                   "climbing", "kayaking", "archery", "rugby", "snowboarding", "martial-arts", "wrestling", "boxing",
                   "skateboarding", "bowling", "baseball", "swimming", "soccer", "softball", "sailing", "tennis",
                   "lacrosse", "horseback-riding", "surfing", "track-and-field", "water-polo", "water-skiing",
                   "curling", "canoeing", "skating", "rowing"],
        "hard": ["fencing", "rugby", "badminton", "baseball", "archery", "cycling", "mountain-climbing", "snowboarding",
                 "aikido", "olympic-swimming", "ice-hockey", "triathlon", "scuba-diving", "synchronized-swimming",
                 "ultimate-frisbee", "sailboarding", "bungee-jumping", "hang-gliding", "skydiving", "paragliding",
                 "skateboarding", "kitesurfing", "roller-derby", "motorsport", "windsurfing", "freestyle-skiing",
                 "darts", "horse-racing", "bobsledding", "crash-test-dummies", "snooker", "mixed-martial-arts",
                 "lumberjack-sports"],
    },
    "countries": {
        "easy": ["india", "usa", "china", "france", "japan", "germany", "brazil", "canada", "mexico", "italy", "spain",
                 "uk", "australia", "south-africa", "egypt", "brazil", "colombia", "peru", "vietnam", "indonesia",
                 "russia", "saudi-arabia", "turkey", "argentina", "chile", "belgium", "sweden", "switzerland", "new-zealand",
                 "finland", "portugal", "denmark", "south-korea", "norway", "poland"],
        "medium": ["germany", "brazil", "australia", "france", "south-africa", "colombia", "brazil", "china", "japan",
                   "austria", "switzerland", "belgium", "portugal", "hungary", "luxembourg", "malaysia", "morocco",
                   "algeria", "south-korea", "iran", "norway", "ireland", "chile", "poland", "mexico", "greece",
                   "sweden", "italy", "finland", "spain", "denmark", "argentina", "turkey", "thailand", "vietnam"],
        "hard": ["malaysia", "bangladesh", "austria", "bahrain", "zimbabwe", "palestine", "cyprus", "syria", "yemen",
                 "mozambique", "algeria", "tajikistan", "burkina-faso", "kyrgyzstan", "kurdistan", "lebanon",
                 "liberia", "belize", "nicaragua", "azerbaijan", "qatar", "fiji", "nepal", "latvia", "rwanda",
                 "mongolia", "malawi", "namibia", "georgia", "paraguay", "niger", "uganda", "bolivia", "cape-verde"],
    }
}


# File to store user data
USER_DATA_FILE = "users_data.json"


# Load user data from a JSON file
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save user data to a JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Hangman game class
class HangmanGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#FFEB5C")

        self.user_data = load_user_data()
        self.current_user = None

        self.create_login_page()
        self.root.mainloop()

    def clear_window(self):
        """Clear all widgets in the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_page(self):
        """Create the login page."""
        self.clear_window()

        # Background color for the window
        self.root.configure(bg="#FFEB5C")  # Light yellow background

        # Title label
        tk.Label(self.root, text="Hangman Game", font=("Comic Sans MS", 30, "bold"), bg="#FFEB5C", fg="#333333",
                 relief="solid", bd=2, padx=10, pady=10).pack(pady=20)

        # Username Label and Entry
        tk.Label(self.root, text="Username:", font=("Arial", 14), bg="#FFEB5C", fg="#333333").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14), bd=2, relief="groove",
                                       highlightbackground="#FFEB5C", highlightthickness=2)
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        tk.Label(self.root, text="Password:", font=("Arial", 14), bg="#FFEB5C", fg="#333333").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 14), show="*", bd=2, relief="groove",
                                       highlightbackground="#FFEB5C", highlightthickness=2)
        self.password_entry.pack(pady=5)

        # Sign In Button
        tk.Button(self.root, text="Sign In", command=self.sign_in, bg="#98FB98", fg="black", font=("Arial", 12, "bold"),
                  relief="raised", bd=3, padx=20, pady=5).pack(pady=10)

        # Sign Up Button
        tk.Button(self.root, text="Sign Up", command=self.sign_up, bg="#ADD8E6", fg="black", font=("Arial", 12, "bold"),
                  relief="raised", bd=3, padx=20, pady=5).pack(pady=10)

    def sign_in(self):
        """Sign in the user."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username in self.user_data and self.user_data[username]["password"] == password:
            self.current_user = username
            self.start_game_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def sign_up(self):
        """Sign up a new user."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists!")
        elif not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
        else:
            self.user_data[username] = {
                "password": password,
                "stats": {"easy": {"played": 0, "won": 0}, "medium": {"played": 0, "won": 0},
                          "hard": {"played": 0, "won": 0}}
            }
            save_user_data(self.user_data)
            messagebox.showinfo("Success", "Account created successfully!")


    def start_game_menu(self):
        """Show the main menu after logging in."""
        self.clear_window()

        # Welcome label
        tk.Label(self.root, text=f"Welcome, {self.current_user}!", font=("Arial", 18), bg="#FFEB5C", fg="#333333").pack(
        pady=10)

        # Start Game Button
        tk.Button(self.root, text="Start Game", command=self.setup_game, bg="#98FB98", fg="black",
              font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=5)

        # View Leaderboard Button
        tk.Button(self.root, text="View Leaderboard", command=self.view_leaderboard, bg="#ADD8E6", fg="black",
              font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=5)

        # Logout Button
        tk.Button(self.root, text="Logout", command=self.logout, bg="#FF6347", fg="white", font=("Arial", 12, "bold"),
              relief="raised", bd=3, padx=20, pady=10).pack(pady=5)


    def setup_game(self):
        """Set up the game with category and level selection."""
        self.clear_window()
        self.category_var = tk.StringVar()
        self.level_var = tk.StringVar()

        # Category selection
        tk.Label(self.root, text="Select a category:", font=("Arial", 14), bg="#FFEB5C", fg="#333333").pack(pady=5)
        tk.OptionMenu(self.root, self.category_var, *categories.keys()).pack(pady=5)

        # Level selection
        tk.Label(self.root, text="Select a level:", font=("Arial", 14), bg="#FFEB5C", fg="#333333").pack(pady=5)
        tk.OptionMenu(self.root, self.level_var, "easy", "medium", "hard").pack(pady=5)

        # Start Game Button
        tk.Button(self.root, text="Start Game", command=self.start_game, bg="#98FB98", fg="black",
              font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=10)

        # Back Button
        tk.Button(self.root, text="Back", command=self.start_game_menu, bg="#ADD8E6", fg="black",
              font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=5)


    def start_game(self):
        """Start the Hangman game with the selected settings."""
        category = self.category_var.get().lower()
        level = self.level_var.get().lower()

        if category and level:
            self.selected_word = random.choice(categories[category][level])
            self.guessed_letters = ["_"] * len(self.selected_word)
            self.incorrect_guesses = 0
            self.max_incorrect_guesses = 6
            self.hints_used = 0
            self.hint_limit = {"easy": 1, "medium": 2, "hard": 3}[level]
            self.level = level
            self.incorrect_guesses_list = []  # Initialize incorrect guesses list

            self.user_data[self.current_user]["stats"][level]["played"] += 1
            save_user_data(self.user_data)

            self.play_game()
        else:
                messagebox.showerror("Error", "Please select both category and level!")


    def play_game(self):
        """Play the game and display the current state."""
        self.clear_window()
        self.display_hangman()

        guessed_word = " ".join(self.guessed_letters)
        tk.Label(self.root, text=guessed_word, font=("Arial", 24), bg="#FFEB5C", fg="#333333").pack(pady=20)

        self.guess_entry = tk.Entry(self.root, font=("Arial", 14), bd=2, relief="groove", highlightbackground="#FFEB5C",
                                highlightthickness=2)
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())
        self.guess_entry.focus()

        # Guess button
        tk.Button(self.root, text="Guess", command=self.check_guess, bg="#98FB98", fg="black", font=("Arial", 12, "bold"),
              relief="raised", bd=3, padx=20, pady=10).pack(pady=10)

        # Hints label
        hint_message = f"Hints remaining: {self.hint_limit - self.hints_used}"
        tk.Label(self.root, text=hint_message, font=("Arial", 14), bg="#FFEB5C", fg="#333333").pack(pady=5)

        # Hint button
        if self.hints_used < self.hint_limit:
            tk.Button(self.root, text="Get Hint", command=self.get_hint, bg="#FF6347", fg="white",
                  font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=10)

        # Play another round button
        tk.Button(self.root, text="Play Another Round", command=self.play_another_round, bg="#98FB98", fg="black",
              font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=10)


    def display_hangman(self):
        """Display the Hangman drawing based on incorrect guesses."""
        hangman_visual = hangman_stages[self.incorrect_guesses]
        tk.Label(self.root, text=hangman_visual, font=("Courier", 14), bg="#FFEB5C", fg="#333333").pack(pady=20)


    def check_guess(self):
        """Check if the guessed letter is correct."""
        guess = self.guess_entry.get().strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Error", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Info", "You've already guessed this letter, try another one!")
            return

    # Check if the guess is incorrect and hasn't been guessed before
        if guess in self.incorrect_guesses_list:
            messagebox.showinfo("Info", "You've already guessed this incorrect letter!")
            return

        # Update guessed word and check for correct guess
        if guess in self.selected_word:
            # Correct guess logic
            for i, letter in enumerate(self.selected_word):
                if letter == guess:
                    self.guessed_letters[i] = guess
            if "_" not in self.guessed_letters:
                self.win_game()
        else:
            # Incorrect guess logic
            self.incorrect_guesses_list.append(guess)
            self.incorrect_guesses += 1
            if self.incorrect_guesses >= self.max_incorrect_guesses:
                self.lose_game()

        self.play_game()


    def get_hint(self):
        """Give a hint to the user."""
        if self.hints_used < self.hint_limit:
            self.hints_used += 1
            hint = random.choice([i for i, letter in enumerate(self.guessed_letters) if letter == "_"])
            self.guessed_letters[hint] = self.selected_word[hint]
            self.play_game()
        else:
            messagebox.showinfo("Info", "No hints left!")


    def win_game(self):
        """Handle winning the game."""
        messagebox.showinfo("Congratulations!", f"You guessed the word '{self.selected_word}' correctly!")
        self.user_data[self.current_user]["stats"][self.level]["won"] += 1
        save_user_data(self.user_data)
        self.start_game_menu()


    def lose_game(self):
        """Handle losing the game."""
        messagebox.showerror("Game Over", f"You've lost! The word was '{self.selected_word}'.")
        self.start_game_menu()


    def play_another_round(self):
        """Play another round of the game."""
        self.setup_game()


    def view_leaderboard(self):
        """Display the leaderboard."""
        self.clear_window()

        tk.Label(self.root, text="Leaderboard", font=("Arial", 24), bg="#FFEB5C", fg="#333333").pack(pady=20)

        for username, data in self.user_data.items():
            tk.Label(self.root, text=f"{username} - Easy: {data['stats']['easy']['won']} wins, "
                                 f"Medium: {data['stats']['medium']['won']} wins, "
                                 f"Hard: {data['stats']['hard']['won']} wins",
                 font=("Arial", 14), bg="#FFEB5C", fg="#333333").pack(pady=5)

        tk.Button(self.root, text="Back", command=self.start_game_menu, bg="#98FB98", fg="black",
              font=("Arial", 12, "bold"), relief="raised", bd=3, padx=20, pady=10).pack(pady=10)


    def logout(self):
        """Logout and return to the login page."""
        self.current_user = None
        self.create_login_page()


if __name__ == "__main__":
    HangmanGUI()
