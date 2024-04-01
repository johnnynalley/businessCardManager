import tkinter.filedialog
from tkinter import filedialog, Tk
from PIL import Image
import pytesseract, shutil

root = Tk()
root.withdraw()

cards = [""]
currentCard = cards[0]


# Saves the currently open business card
def save_business_card():
    global cards, currentCard

    while True:
        try:
            input("Press Enter to save the businessCard ")
            businessCard = tkinter.filedialog.asksaveasfilename()
            cards.append(businessCard)
            currentCard = cards[-1]
            return businessCard

        except IsADirectoryError:
            input("Press Enter to try again. ")


# Gets the path of the desired business card
def open_business_card():
    global cards

    while True:
        for x in range(len(cards)):
            print(cards)


# Gets the text from the selected image
def get_card_text():
    imageText = pytesseract.image_to_string(Image.open(currentCard))

    if len(imageText) == 0:
        return "I was unable to find any text in the image."

    else:
        return imageText


if __name__ == '__main__':
    print(get_card_text())
