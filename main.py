import pytesseract
import tkinter.filedialog
from tkinter import Tk
import json

from PIL import Image

root = Tk()
root.withdraw()

cards = {
}

# Saves the currently open business card
def save_current_card():
    global cards, currentCard

    while True:
        try:
            input("Press Enter to save the businessCard ")
            businessCard = tkinter.filedialog.asksaveasfilename()
            cards[businessCard] = businessCard
            currentCard = cards[-1]
            return businessCard

        except IsADirectoryError:
            input("Press Enter to try again. ")


# Gets the path of the desired business card
def open_business_card():
    global cards

    while True:
        print(cards)

        fileInput = input("Which card would you like to access? ")
        break

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

    with (open('cards.json', 'w') as file):
        json.dump(cards, file)




currentCard = ""

if __name__ == '__main__':
    currentCard = "./cards/test_card_1"

    save_current_card()

    print(get_card_text())
