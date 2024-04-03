import pytesseract
import tkinter.filedialog
from tkinter import Tk
import json
import os
import shutil

from PIL import Image

root = Tk()
root.withdraw()

card_destination = "./cards/"

# Opens the cards.json file and imports the data as a dictionary
with open("cards.json", "r") as file:
    cards = json.load(file)


def create_card():
    global cards

    card_name = input("Card Name: ")
    card_description = input("Card Description: ")
    original_image_destination = tkinter.filedialog.askopenfilename()
    print("Original Image Destination: " + original_image_destination)

    # Copies the card from the original destination to the new destination defined in card_destination
    shutil.copy2(original_image_destination, card_destination)
    card_image = card_destination + os.path.basename(original_image_destination)
    print("New Image Destination: " + card_image)

    # Creates nested dictionary under the cards dictionary with keys for the card's name, description, and image
    # destination, and then saves the cards.
    cards[card_name] = {"Card Name": card_name, "Card Description": card_description, "Card Image": card_image}
    save_all_cards()

    return cards[card_name]


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
    print("create/c: creates a card\n"
          "save/s: saves all cards\n"
          "delete/d: deletes selected card\n"
          "list/l: lists all cards\n"
          "text/t: attempts to get text from the selected card using OCR\n"
          "quit/q: quits the program\n")


def delete_card():
    global cards

    while True:
        list_all_cards()
        card_name = input("Which card would you like to delete? Type \"q\" to quit.")
        if card_name == "q":
            return

        elif card_name not in cards:
            print(card_name + "was not found in your cards list. Please verify the filename of the card you wish to "
                              "delete and try again")
            continue

        else:
            del cards[card_name]
            save_all_cards()

        if card_name not in cards:
            print("Successfully deleted " + card_name + ". ")

        else:
            print("Failed to delete " + card_name + ". Please try again. ")


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

            elif choice == "delete" or choice == "d":
                delete_card()

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
