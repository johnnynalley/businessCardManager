import pytesseract
import tkinter.filedialog
from tkinter import Tk
import json
import os
import shutil

from PIL import Image

root = Tk()
root.withdraw()

# Opens the cards.json file and imports the data as a dictionary
with open("cards.json", "r") as file:
    cards = json.load(file)


def create_card():
    global cards

    card_name = input("Card Name: ")
    card_description = input("Card Description: ")
    card_image = tkinter.filedialog.askopenfilename()

    cards[card_name] = {"Card Name": card_name, "Card Description": card_description, "Card Image": card_image}

    save_all_cards()

    card = cards[card_name]
    return card


# Gets the text from the selected image
def get_card_text():
    global cards

    card_name = input("Which card would you like to get text from? ")

    image_text = pytesseract.image_to_string(Image.open(cards[card_name]["Card Image"]))

    if len(image_text) == 0:
        return "I was unable to find any text in the image."

    else:
        return image_text


def save_all_cards():
    global cards

    with open("cards.json", "w") as jsonFile:
        json.dump(cards, jsonFile)


def list_all_cards():
    global cards

    with (open('cards.json', 'r') as jsonFile):
        cards = json.load(jsonFile)

    print(json.dumps(cards, indent=4))


def help():
    print("create: creates a card\n"
          "save: saves all cards\n"
          "list: lists all cards\n"
          "text: attempts to get text from the selected card using OCR\n"
          "quit: quits the program\n")


def main():
    global cards

    while True:
        choice = input("Enter your choice: ")

        try:
            if choice == "help" or choice == "h":
                help()

            elif choice == "create" or choice == "c":
                create_card()

            elif choice == "save" or choice == "s":
                save_all_cards()

            elif choice == "list" or choice == "l":
                list_all_cards()

            elif choice == "text" or choice == "t":
                print(get_card_text())

            elif choice == "quit" or choice == "q":
                quit()
            else:
                print("Invalid")

        except ValueError:
            print("Not a valid input. Please try again. ")


if __name__ == '__main__':
    print("Type help/h for a list of commands, or quit/q to quit.")

    main()
