import os
import random
import time
import keyboard
from colorama import Fore, Style, init

init(autoreset=True)

class KeyboardGame:
    def __init__(self):
        self.keys_to_train = ['q', 'w', 'e', 'r', '1', '2', '3', '4', 'a', 's', 'd', 'f', 'z', 'x', 'c', 'v', 'b', 'n', 'tab', 'caps lock', 'shift']
        self.key_data = {key: {'total_time': 0, 'correct_presses': 0, 'total_attempts': 0} for key in self.keys_to_train}
        self.incorrect_presses = 0
        self.total_time = 0
        self.total_attempts = 0
        self.correct_presses = 0
        self.total_characters = 0
        self.total_words = 0
        self.score = 0

    def display_stats(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "-"*30)
        print("Game Over - Your Score:")
        print(f"Correct key presses: {self.correct_presses}")
        print(f"Incorrect key presses: {self.incorrect_presses}")
        print(f"Total characters typed: {self.total_characters}")
        print(f"Total words typed: {self.total_words}")
        print(f"Total time: {self.total_time:.2f} seconds")
        print(f"Keystrokes per minute (KPM): {self.calculate_kpm():.2f}")
        print(f"Words per minute (WPM): {self.calculate_wpm():.2f}")
        print(f"Accuracy: {self.calculate_accuracy():.2f}%")
        print("Key Statistics:")
        for key, data in self.key_data.items():
            if data['total_attempts'] > 0:
                average_time = data['total_time'] / max(1, data['total_attempts'])
                accuracy = (data['correct_presses'] / max(1, data['total_attempts'])) * 100
                print(f"Key: {key}, Times Pressed: {data['total_attempts']}, Average Time: {average_time:.2f} seconds, Accuracy: {accuracy:.2f}%")
        print("-"*30 + "\n")

    def calculate_score(self):
        # The scoring algorithm (adjust as needed)
        self.score = int((self.correct_presses) * 10 / max(1, self.total_time))

    def calculate_kpm(self):
        return (self.total_characters / 1000) / max(1, self.total_time / 60)

    def calculate_wpm(self):
        return (self.total_words / 5) / max(1, self.total_time / 60)

    def calculate_accuracy(self):
        return (self.correct_presses / max(1, self.total_attempts)) * 100

    def countdown_animation(self, seconds):
        for i in range(seconds, 0, -1):
            print(Fore.YELLOW + f"Get ready... {i}", end="\r")
            time.sleep(1)
        print(Style.RESET_ALL)
        time.sleep(1)

    def display_prompt(self, key):
        print(Fore.WHITE + f"Type: {key}\n", end="\r")

    def display_result(self, key, correct=False):
        if correct:
            print(Fore.GREEN + f"Correct!\n", end="\r")
        else:
            print(Fore.RED + f"Incorrect!\n", end="\r")

    def get_user_input(self):
        try:
            event = keyboard.read_event(suppress=True)
            pressed_key = event.name

            while event.event_type == keyboard.KEY_DOWN:
                event = keyboard.read_event(suppress=True)

            if pressed_key == 'enter':
                return 'enter'

            return pressed_key

        except KeyboardInterrupt:
            return 'exit'

    def display_user_input(self, user_input):
        print(Fore.CYAN + f"Your input: {user_input}\n", end="\r")

    def record_key_press(self, key, time_taken, correct):
        self.key_data[key]['total_time'] += time_taken
        self.key_data[key]['total_attempts'] += 1
        if correct:
            self.key_data[key]['correct_presses'] += 1

    def keyboard_game(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the Animated Keyboard Game!")
        print("Type the characters displayed as quickly as possible. Press 'Enter' to view the report.\n")

        try:
            self.countdown_animation(3)

            while True:
                random_key = random.choice(self.keys_to_train)
                self.total_attempts += 1

                # Record the start time for the key press
                start_time = time.time()

                # Display the random key to type with animation
                self.display_prompt(random_key)

                # Get user input
                user_input = self.get_user_input()
                time.sleep(0.01)
                

                if user_input == 'exit':
                    # Handle game termination with Ctrl+C
                    break
                elif user_input == 'enter':
                    # Display the report on 'Enter' press
                    self.calculate_score()
                    self.display_stats()
                    input("Press 'Enter' to continue...")
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif user_input != random_key:
                    # Handle incorrect key press
                    self.incorrect_presses += 1
                    self.display_user_input(user_input)
                else:
                    # Handle correct key press
                    self.correct_presses += 1

                # Record the end time for the key press
                end_time = time.time()
                time_taken = end_time - start_time

                # Update total characters and words
                if user_input != 'enter':
                    self.total_characters += 1
                    if user_input.isspace():
                        self.total_words += 1

                # Record the key press data
                self.record_key_press(random_key, time_taken, correct=(user_input == random_key))

                # Display the result
                self.display_result(random_key, correct=(user_input == random_key))

                # Record the end time
                self.total_time += time_taken

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

if __name__ == "__main__":
    game = KeyboardGame()
    game.keyboard_game()
