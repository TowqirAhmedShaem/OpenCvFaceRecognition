 # -*- coding : utf-8 -*-

 #img = cv2.imread('/home/shaem/Shaem/OpencvDocuments/pyfaces/Image/prove/u9.jpg')
 #ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

# resize an image using the PIL image library
# free from:  http://www.pythonware.com/products/pil/index.htm
# tested with Python24        vegaseat     11oct2005
import Image
# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
imageFile = "ss2.png"
im1 = Image.open(imageFile)
# adjust width and height to your needs
width = 600
height = 850
# use one of these filter options to resize the image
im2 = im1.resize((width, height), Image.NEAREST)      # use nearest neighbour
im3 = im1.resize((width, height), Image.BILINEAR)     # linear interpolation in a 2x2 environment
im4 = im1.resize((width, height), Image.BICUBIC)      # cubic spline interpolation in a 4x4 environment
im5 = im1.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter
im1 = im1.resize((width, height), Image.ANTIALIAS) 
ext = ".gif"
im2.save("NEAREST" + ext)
im3.save("BILINEAR" + ext)
im4.save("BICUBIC" + ext)
im5.save("ANTIALIAS" + ext)
im1.save(imageFile)
