from tkinter import filedialog, Tk
from PIL import Image
import pytesseract

root = Tk()
root.withdraw()


# Gets the path of the desired business card
while True:
    try:
        path = filedialog.askopenfilename()
        break

    except IsADirectoryError:
        input("Press Enter to try again. ")


# Gets the text from the selected image
def get_card_text():
    imageText = pytesseract.image_to_string(Image.open(path))

    if len(imageText) == 0:
        return "I was unable to find any text in the image."

    else:
        return imageText


if __name__ == '__main__':
    print(get_card_text())  # TODO find a way to handle blank outputs
