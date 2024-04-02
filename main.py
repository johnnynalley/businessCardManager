import pytesseract
import tkinter.filedialog
from tkinter import Tk
import json
import os
import shutil

from PIL import Image

root = Tk()
root.withdraw()

with open("cards.json", "r") as file:
    cards = json.load(file)


# Imports a card
def import_card():
    global cards

    try:
        cardPath = tkinter.filedialog.askopenfilename()
        print(cardPath)

        shutil.copy(cardPath, "./cards/")

        cards[os.path.basename(cardPath)] = "./cards/" + os.path.basename(cardPath)

        save_all_cards()
        print(f"Successfully imported {os.path.basename(cardPath)}, and is now saved to ./cards/" + os.path.basename(
            cardPath))
        return cards[os.path.basename(cardPath)]

    except (IsADirectoryError, FileNotFoundError) as error:
        return "Failed to import card, please try again. "


# Gets the path of the desired business card
# def open_business_card():
#     global cards
#
#     while True:
#         print(cards)
#
#         try:
#             fileInput = input("Which card would you like to access? ")
#             break
#
#         except KeyError:
#             print("Not a valid input. Please try again. ")
#
#     if fileInput:
#         return cards[fileInput]


# Gets the text from the selected image
def get_card_text():
    global cards

    card_name = input("Which card would you like to get text from? ")

    image_text = pytesseract.image_to_string(Image.open(cards[card_name]))

    if len(image_text) == 0:
        return "I was unable to find any text in the image."

    else:
        return image_text


def save_all_cards():
    global cards

    with (open('cards.json', 'w') as jsonFile):
        json.dump(cards, jsonFile)


def list_all_cards():
    global cards

    with (open('cards.json', 'r') as jsonFile):
        cards = json.load(jsonFile)
    formatted_cards = json.dumps(cards, indent=2)

    print(formatted_cards)


def help():
    print("import: imports your cards\n"
          # "open: opens a card\n"
          "save: saves all cards\n"
          "list: lists all cards\n"
          "text: attempts to get text from the selected card using OCR\n"
          "quit: quits the program\n")


def main():
    global cards, currentCard

    while True:
        choice = input("Enter your choice: ")

        try:
            if choice == "help" or choice == "h":
                help()

            elif choice == "import" or choice == "f":
                choice = ""
                import_card()

            # elif choice == "open" or choice == "o":
            #     open_business_card()

            elif choice == "save" or choice == "s":
                save_all_cards()

            elif choice == "list" or choice == "l":
                list_all_cards()

            elif choice == "text" or choice == "t":
                print(get_card_text())

            elif choice == "quit" or choice == "q":
                quit()

        except ValueError:
            print("Not a valid input. Please try again. ")


if __name__ == '__main__':
    print("Type help/h for a list of commands, or quit/q to quit.")

    main()
