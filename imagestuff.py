from PIL import Image, ImageDraw, ImageFont, ImageOps
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

def createStatsImage(summoner_name, tier, rank, lp, champ1, champ2, champ3, champ1_pts, champ2_pts, champ3_pts):
    im = Image.open("baseStatsImg.png")
    draw = ImageDraw.Draw(im, mode="RGBA")
    big_font = ImageFont.truetype("arial.ttf", 48)
    small_font = ImageFont.truetype("arial.ttf", 14)
    
    #coordinates are: top left, x top left y, bottom right x, bottom right y
    name_textbox = (282, 17, 1024, 158)
    
    #summonerx and y are the x and y position of the summoner name that will be written (10px offset from top left corner of box)
    summoner_x = (name_textbox[0] + 10)
    summoner_y = (name_textbox[1] + 10)

    #rankx and y are the x and y position of the rank that will be written (10px offset from bottom left corner of box)
    rank_x = (name_textbox[0] + 10)
    rank_y = (name_textbox[3] - 60)
    rank_text = "{} {}, {}LP".format(tier, rank, lp)

    #middle of name box is about 653x, 88zy
    #is is 742 wide, 141 tall
    #top left is 282x 17y
    draw.rectangle(name_textbox, fill=(0, 0, 0, 235))
    draw.text((summoner_x, summoner_y), summoner_name, font=big_font, fill=(255, 215, 0))
    draw.text((rank_x, rank_y), rank_text, font=big_font, fill=(255, 215, 0))


    #middle of rank icon is about 961x 86.50y
    #is 102wide 117 tall
    #top left is 910x, 28y
    rank_image_name = "images/{}.png".format(tier.lower())
    rank_image = Image.open(rank_image_name)
    rank_image = rank_image.resize(size=(int(rank_image.size[0] / 5), int(rank_image.size[1] / 5)))
    im.paste(rank_image, (910, 28), rank_image)


    #Test to make champ image circle
    
    #generic mask stuff
    mask = Image.open('mask.png').convert('L')
    mask = mask.resize((125, 125))

    #champ1 image
    url = "http://ddragon.leagueoflegends.com/cdn/9.14.1/img/champion/{}.png".format(champ1)
    response = requests.get(url)
    champ_image = Image.open(BytesIO(response.content))
    champ_image = champ_image.resize((125, 125))

    output = ImageOps.fit(champ_image, mask.size, centering = (0.5, 0.5))
    output.putalpha(mask)

    im.paste(output, (579, 311), output)

    message = "{} pts".format(champ1_pts)
    w, h = small_font.getsize(message)

    mastery_1_box = (581, 282, 701, 302)
    draw.rectangle(mastery_1_box, fill=(0, 0, 0, 235))
    text_box_x = mastery_1_box[0]
    text_box_y = mastery_1_box[1]
    text_box_height = mastery_1_box[3] - mastery_1_box[1]
    text_box_width = mastery_1_box[2] - mastery_1_box[0]

    x = text_box_x + (text_box_width/2) - (w/2)
    y = text_box_y + (text_box_height/2) - (h/2)
    draw.text((x, y), message, font=small_font, fill=(255, 215, 0))

    #champ 2 image
    url = "http://ddragon.leagueoflegends.com/cdn/9.14.1/img/champion/{}.png".format(champ2)
    response = requests.get(url)
    champ_image = Image.open(BytesIO(response.content))
    champ_image = champ_image.resize((125, 125))

    output = ImageOps.fit(champ_image, mask.size, centering = (0.5, 0.5))
    output.putalpha(mask)

    im.paste(output, (459, 500), output)

    message = "{} pts".format(champ2_pts)
    w, h = small_font.getsize(message)

    mastery_2_box = (462, 634, 582, 654)
    draw.rectangle(mastery_2_box, fill=(0, 0, 0, 235))
    text_box_x = mastery_2_box[0]
    text_box_y = mastery_2_box[1]
    text_box_height = mastery_2_box[3] - mastery_2_box[1]
    text_box_width = mastery_2_box[2] - mastery_2_box[0]

    x = text_box_x + (text_box_width/2) - (w/2)
    y = text_box_y + (text_box_height/2) - (h/2)
    draw.text((x, y), message, font=small_font, fill=(255, 215, 0))

    #champ 3 image
    url = "http://ddragon.leagueoflegends.com/cdn/9.14.1/img/champion/{}.png".format(champ3)
    response = requests.get(url)
    champ_image = Image.open(BytesIO(response.content))
    champ_image = champ_image.resize((125, 125))

    output = ImageOps.fit(champ_image, mask.size, centering = (0.5, 0.5))
    output.putalpha(mask)

    im.paste(output, (705, 500), output)

    message = "{} pts".format(champ3_pts)
    w, h = small_font.getsize(message)

    mastery_3_box = (707, 634, 827, 654)
    draw.rectangle(mastery_3_box, fill=(0, 0, 0, 235))
    text_box_x = mastery_3_box[0]
    text_box_y = mastery_3_box[1]
    text_box_height = mastery_3_box[3] - mastery_3_box[1]
    text_box_width = mastery_3_box[2] - mastery_3_box[0]

    x = text_box_x + (text_box_width/2) - (w/2)
    y = text_box_y + (text_box_height/2) - (h/2)
    draw.text((x, y), message, font=small_font, fill=(255, 215, 0))

    im.save("statstest.png")

    