from PIL import Image

img1 = Image.open(r"./static/pics/0.png")
newsize = (50,50)
img1 = img1.resize(newsize)
image1copy = img1.copy()
img2 = Image.new('RGBA', (380, 700), (255, 0, 0, 0))
image2copy = img2.copy()

image2copy.paste(image1copy, (115,112))
image2copy.paste(image1copy.rotate(90), (51, 603))
image2copy.paste(image1copy.rotate(180), (323,71))
image2copy.paste(image1copy.rotate(270), (326,445))

image2copy.show()


