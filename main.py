import pytesseract
import tkinter.filedialog
from tkinter import Tk
import json
import os

from PIL import Image

root = Tk()
root.withdraw()

with open("cards.json", "r") as file:
    cards = json.load(file)


# Imports a card
def import_card():
    global cards

    while True:
        try:
            input("Press Enter to save the card ")
            cardPath = tkinter.filedialog.asksaveasfilename()
            cards[os.path.basename(cardPath)] = cardPath

            save_all_cards()
            print(f"Successfully imported {os.path.basename(cardPath)}, and is now saved to {cardPath}")
            return cards[os.path.basename(cardPath)]

        except IsADirectoryError:
            input("Press Enter to try again. ")


# Gets the path of the desired business card
def open_business_card():
    global cards

    while True:
        print(cards)

        try:
            fileInput = input("Which card would you like to access? ")
            break

        except KeyError:
            print("Not a valid input. Please try again. ")

    if fileInput:
        global currentCard

        currentCard = cards[fileInput]
        return currentCard


# Gets the text from the selected image
def get_card_text():
    imageText = pytesseract.image_to_string(Image.open(currentCard))

    if len(imageText) == 0:
        return "I was unable to find any text in the image."

    else:
        return imageText


def save_all_cards():
    global cards

    with (open('cards.json', 'w') as f):
        json.dump(cards, f)


def help():
    print("import: imports your cards\n"
          "open: opens a card\n"
          "save: saves all cards\n"
          "quit: quits the program")


def main():
    global cards, currentCard

    while True:
        choice = input().lower
        try:
            if choice == "help" or "h":
                help()

            elif choice == "import":
                import_card()

            elif choice == "open":
                open_business_card()

            elif choice == "save all":
                save_all_cards()

            elif choice == "quit/q":
                quit()

        except ValueError:

            print("Not a valid input. Please try again. ")


if __name__ == '__main__':
    print("Type help/h for a list of commands, or quit/q to quit.")

    main()
