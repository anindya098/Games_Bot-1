from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

#The base image that will be modified (This is a path relative to this python file)
baseImage = "tesload.png"

#Positions of the top left corner for each champion picture added to a list
c0 = (260, 20)
c1 = (543, 20)
c2 = (823, 20)
c3 = (1105, 20)
c4 = (1387, 20)
c5 = (260, 570)
c6 = (543, 570)
c7 = (823, 570)
c8 = (1105, 570)
c9 = (1387, 570)
corners = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]

#Postion for text boxes for blue team
tb0 = (260, 450, 529, 513)
tb1 = (543, 450, 810, 513)
tb2 = (823, 450, 1092, 513)
tb3 = (1105, 450, 1373, 513)
tb4 = (1387, 450, 1655, 513)

#Postion for text boxes for red team
tb5 = (260, 1000, 529, 1063)
tb6 = (543, 1000, 810, 1063)
tb7 = (823, 1000, 1092, 1063)
tb8 = (1105, 1000, 1373, 1063)
tb9 = (1387, 1000, 1655, 1063)

textBoxes = [tb0, tb1, tb2, tb3, tb4, tb5, tb6, tb7, tb8, tb9]

#Method takes a summoner name, champion name and index (picture #) and uses those to modify the image
def addToImage(summoner, champion, index):

    #Image type that represents the image being modified
    im = Image.open(baseImage)

    #Get a splash image for whichever champion the summoner is playing, and resize it to match the size of the boxes being replaced
    url = "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/" + champion + "_0.jpg"
    response = requests.get(url)
    champImage = Image.open(BytesIO(response.content))
    champImage = champImage.resize(size=(int(champImage.size[0] / 1.14), int(champImage.size[1] / 1.13)))

    #Add the resized splash image at the specified index (picture #) to the base image
    im.paste(champImage, corners[index])

    #draw must be in RGBA mode because we want the textboxes to be sort of transparent (have an alpha channel)
    draw = ImageDraw.Draw(im, mode="RGBA")
    
    #Font that we will be using. (This is a path relative to this python file)
    font = ImageFont.truetype("arial.ttf", 24)

    #Get the width and the height of the summoner name in the specified font (arial)
    message = summoner
    w, h = font.getsize(message)

    #Get the X, Y, height and width of the text box that needs to be drawn (This is so we can center the summoner name in the text box)
    textBoxX = textBoxes[index][0]
    textBoxY = textBoxes[index][1]
    textBoxHeight = textBoxes[index][3] - textBoxes[index][1]
    textBoxWidth = textBoxes[index][2] - textBoxes[index][0]

    #x and y are the x and y position of the summoner name that will be written (centered in the textbox)
    x = textBoxX + (textBoxWidth/2) - (w/2)
    y = textBoxY + (textBoxHeight/2) - (h/2)

    #Draw the textbox and summoner name onto the image
    draw.rectangle(textBoxes[index], fill=(0, 0, 0, 200))
    draw.text((x, y), message, font=font, fill=(255, 215, 0))

    #Save the image
    im.save("tesload.png")