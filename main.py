import json
import os
import shutil
import tkinter.filedialog
from datetime import datetime
from tkinter import Tk

import pytesseract
from PIL import Image

root = Tk()
root.withdraw()

card_destination = os.path.dirname(__file__)
card_destination = os.path.join(card_destination, "cards")


# Creates a new card, and copies the provided image path to the app's own path, and adds data for the card
def create_card():
    global cards

    # Assigns name, description, creation date, and the original image destination
    card_name = input("Card Name: ")
    card_description = input("Card Description: ")
    card_creation_date = datetime.now()
    original_image_destination = tkinter.filedialog.askopenfilename()
    print("Original Image Destination: " + original_image_destination)

    # Copies the card from the original destination to the new destination defined in card_destination
    shutil.copy2(original_image_destination, card_destination)
    card_image_path = os.path.join(card_destination, os.path.basename(original_image_destination))
    print("New Image Destination: " + card_image_path)

    # Creates nested dictionary under the cards dictionary with keys for the card's name, description, creation
    # date, and image destination, and then saves the cards.
    cards[card_name] = {"Card Name": card_name,
                        "Card Description": card_description,
                        "Card Date": card_creation_date,
                        "Card Image": card_image_path
                        }
    save_all_cards()

    # Checks to see if the new card is added into the dictionary
    if card_name not in cards:
        print("Failed to add " + card_name + ". Please try again. ")

    else:
        print("Successfully added " + card_name)
    return cards[card_name]


# Gets the text from the selected image
def get_card_text():
    global cards

    card_name = input("Which card would you like to get text from?\n")

    try:
        image_text = pytesseract.image_to_string(Image.open(cards[card_name]["Card Image"]))

        if len(image_text) == 0:
            return "I was unable to find any text in the image.\n"

        else:
            return image_text

    except KeyError:
        print("Failed to get card text. Please try again.\n")
        return


def save_all_cards():
    global cards

    with open("cards.json", "w") as jsonFile:
        json.dump(cards, jsonFile, indent=4, default=str)


def list_all_cards():
    global cards

    with (open('cards.json', 'r') as jsonFile):
        cards = json.load(jsonFile)

    print(json.dumps(cards, indent=4))


def help():
    print("create/c: creates a card\n"
          "delete/d: deletes selected card\n"
          "save/s: saves all cards\n"
          "quit/q: quits the program\n"
          "image/i: shows the image of a card\n"
          "list/l: lists all cards\n"
          "text/t: attempts to get text from the selected card using OCR\n")


def delete_card():
    global cards

    while True:
        list_all_cards()
        card_name = input("Which card would you like to delete? Type \"q\" to quit.\n")
        if card_name == "q":
            return

        elif card_name not in cards:
            print(card_name + " was not found in your cards list. Please verify the filename of the card you wish to "
                              "delete and try again")
            continue

        else:
            # Delete image in cards folder
            card_image_path = cards[card_name]['Card Image']

            print(card_image_path)

            try:
                os.remove(card_image_path)

            except KeyError:
                print(f"Failed to delete {cards[card_name][card_image_path]}. Please try again.\n")
                pass

            del cards[card_name]
            save_all_cards()

        # Checks if the card was successfully deleted and outputs the result
        if card_name not in cards:
            print("Successfully deleted " + card_name + ". ")
            return

        else:
            print("Failed to delete " + card_name + ". Please try again. ")
            continue


def show_card_image():
    global cards

    user_response = input("Which card would you like to show? Type \"q\" to quit.\n")

    if user_response == "q":
        return

    elif os.path.exists(cards[user_response]['Card Image']):
        card_image_path = cards[user_response]['Card Image']
        image = Image.open(card_image_path)
        image.show()

    else:
        print("Invalid card image. Please try again.")


# Opens the cards.json file and imports the data as a dictionary
try:
    with open("cards.json", "r") as file:
        cards = json.load(file)

except json.decoder.JSONDecodeError:
    with open("cards.json", "w") as file:
        cards = {}
        json.dump(cards, file)


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

            elif choice == "quit" or choice == "q":
                quit()

            elif choice == "image" or choice == "i":
                show_card_image()

            elif choice == "text" or choice == "t":
                print(get_card_text())

            else:
                print("Invalid")

        except ValueError:
            print("Not a valid input. Please try again. ")


if __name__ == '__main__':
    print("Type help/h for a list of commands, or quit/q to quit.")
    main()
