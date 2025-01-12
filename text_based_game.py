import random

# Word categories with difficulty levels
animals_easy = ["lion", "bear", "zebra", "panda", "tiger"]
animals_medium = ["elephant", "giraffe", "kangaroo", "koala", "leopard"]
animals_hard = ["hippopotamus", "rhinoceros", "orangutan", "crocodile", "alligator"]

countries_easy = ["canada", "india", "japan", "france", "mexico"]
countries_medium = ["brazil", "spain", "germany", "italy", "south africa"]
countries_hard = ["malawi", "comoros", "belize", "lesotho", "kiribati"]

sports_easy = ["soccer", "basketball", "tennis", "rugby", "baseball"]
sports_medium = ["hockey", "golf", "volleyball", "swimming", "boxing"]
sports_hard = ["fencing", "water polo", "synchronized swimming", "handball", "lacrosse"]

# Combined categories
all_categories = {
    "animals": {"easy": animals_easy, "medium": animals_medium, "hard": animals_hard},
    "countries": {"easy": countries_easy, "medium": countries_medium, "hard": countries_hard},
    "sports": {"easy": sports_easy, "medium": sports_medium, "hard": sports_hard},
}

# Leaderboard tracking wins and losses
leaderboard = {}


# Display hangman visual
def display_hangman(incorrect_guesses):
    hangman_stages = [
        '''
           ------
           |    |
                |
                |
                |
                |
        ________|_____
        ''',
        '''
           ------
           |    |
           O    |
                |
                |
                |
        ________|_____
        ''',
        '''
           ------
           |    |
           O    |
           |    |
                |
                |
        ________|_____
        ''',
        '''
           ------
           |    |
           O    |
          /|    |
                |
                |
        ________|_____
        ''',
        '''
           ------
           |    |
           O    |
          /|\\   |
                |
                |
        ________|_____
        ''',
        '''
           ------
           |    |
           O    |
          /|\\   |
          /     |
                |
        ________|_____
        ''',
        '''
           ------
           |    |
           O    |
          /|\\   |
          / \\   |
                |
        ________|_____
        '''
    ]
    print(hangman_stages[incorrect_guesses])


# Game logic
def play_hangman():
    global leaderboard

    # Get player's name for leaderboard
    player_name = input("Enter your name: ").capitalize()

    score = {"won": 0, "lost": 0}

    while True:
        print("\nWelcome to Hangman!")

        # Step 1: Ask the user to choose a category
        category = input("Choose a category (animals, countries, sports): ").lower()

        if category not in all_categories:
            print("Invalid category. Please choose 'animals', 'countries', or 'sports'.")
            continue

        # Step 2: Ask the user to choose a difficulty level
        difficulty = input("Choose a difficulty level (easy, medium, hard): ").lower()

        if difficulty not in ["easy", "medium", "hard"]:
            print("Invalid difficulty level. Please choose 'easy', 'medium', or 'hard'.")
            continue

        # Choose word from the selected category and difficulty
        word = random.choice(all_categories[category][difficulty])
        guessed_letters = ["_"] * len(word)
        incorrect_guesses = 0
        used_letters = []

        # Set the number of hints based on difficulty
        if difficulty == "easy":
            max_hints = 1
        elif difficulty == "medium":
            max_hints = 3
        else:
            max_hints = 4

        hints_used = 0
        hint_used = False

        print(f"\nYou have {6 - incorrect_guesses} chances to guess the word.")
        print(f"You can use {max_hints} hints for this difficulty.")
        print(" ".join(guessed_letters))

        while incorrect_guesses < 6:
            print("\n")
            guess = input("Guess a letter (or type 'hint' for a hint): ").lower()

            if guess == "hint" and hints_used < max_hints:
                hint_used = True
                hints_used += 1
                hint = random.choice([letter for letter in word if letter not in guessed_letters])
                print(f"Hint: One of the letters is '{hint}'")
                continue
            elif guess == "hint":
                print("You've already used your available hints!")
                continue

            if guess in used_letters:
                print(f"You've already guessed the letter '{guess}'. Try another one.")
                continue

            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a valid letter.")
                continue

            used_letters.append(guess)

            if guess in word.lower():
                for i in range(len(word)):
                    if word[i].lower() == guess:
                        guessed_letters[i] = word[i]
                print(" ".join(guessed_letters))
            else:
                incorrect_guesses += 1
                display_hangman(incorrect_guesses)
                print(f"Incorrect! You have {6 - incorrect_guesses} chances left.")

            if "_" not in guessed_letters:
                print(f"\nCongratulations! You won! The word was '{word}'.")
                score["won"] += 1
                break

        if incorrect_guesses == 6:
            print(f"\nSorry, you lost. The word was '{word}'.")
            score["lost"] += 1

        # Update leaderboard
        leaderboard[player_name] = leaderboard.get(player_name, {"won": 0, "lost": 0})
        leaderboard[player_name]["won"] += score["won"]
        leaderboard[player_name]["lost"] += score["lost"]

        print(f"\nYour current score: Won: {score['won']} | Lost: {score['lost']}")

        # Show leaderboard
        print("\nLeaderboard:")
        for player, scores in leaderboard.items():
            print(f"{player}: Wins: {scores['won']} | Losses: {scores['lost']}")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break


# Start the game
play_hangman()
