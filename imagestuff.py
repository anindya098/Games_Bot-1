from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

baseImage = "tesload.png"

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

#TEXT BOXES FOR BLUE TEAM
tb0 = (260, 450, 529, 513)
tb1 = (543, 450, 810, 513)
tb2 = (823, 450, 1092, 513)
tb3 = (1105, 450, 1373, 513)
tb4 = (1387, 450, 1655, 513)

#TEXT BOXES FOR RED TEAM
tb5 = (260, 1000, 529, 1063)
tb6 = (543, 1000, 810, 1063)
tb7 = (823, 1000, 1092, 1063)
tb8 = (1105, 1000, 1373, 1063)
tb9 = (1387, 1000, 1655, 1063)

textBoxes = [tb0, tb1, tb2, tb3, tb4, tb5, tb6, tb7, tb8, tb9]

def addToImage(summoner, champion, index):
    print("champion: %s\nsummoner: %s\nindex: %d" % (champion, summoner, index))

    im = Image.open(baseImage)

    url = "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/" + champion + "_0.jpg"
    response = requests.get(url)
    champImage = Image.open(BytesIO(response.content))
    champImage = champImage.resize(size=(int(champImage.size[0] / 1.14), int(champImage.size[1] / 1.13)))

    im.paste(champImage, corners[index])

    draw = ImageDraw.Draw(im, mode="RGBA")
    font = ImageFont.truetype("arial.ttf", 24)

    message = summoner
    w, h = font.getsize(message)

    textBoxX = textBoxes[index][0]
    textBoxY = textBoxes[index][1]
    textBoxHeight = textBoxes[index][3] - textBoxes[index][1]
    textBoxWidth = textBoxes[index][2] - textBoxes[index][0]

    x = textBoxX + (textBoxWidth/2) - (w/2)
    y = textBoxY + (textBoxHeight/2) - (h/2)
    draw.rectangle(textBoxes[index], fill=(0, 0, 0, 200))
    draw.text((x, y), message, font=font, fill=(255, 215, 0))

    im.save("tesload.png")