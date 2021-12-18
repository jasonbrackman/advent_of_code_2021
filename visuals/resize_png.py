from PIL import Image, ImageFilter

basewidth = 320
with Image.open('day_17.png') as img:
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))
    img.show()
    img.save('day_17b.png')