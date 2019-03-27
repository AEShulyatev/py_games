from PIL import Image, ImageTk
from scipy.misc import imresize
from skimage import io
import numpy as np

img = io.imread(r'/home/artemsh23/PycharmProjects/titled/cacodemon/cacodem3.png')
img2 = io.imread(r'/home/artemsh23/PycharmProjects/titled/cacodemon/cacodem2.png')
for i in range(2, 940):
    res = imresize(img if i < 700 else img2, (i, i))
    #im = Image.fromarray(res)
    #io.imsave('/home/artemsh23/PycharmProjects/titled/cacodemon/res.png', res)
    #cac = Image.open('/home/artemsh23/PycharmProjects/titled/cacodemon/res.png')
    #cac.load()
    #print(cac)
    #arr.append(cac)
    io.imsave('/home/artemsh23/PycharmProjects/titled/cacodemon/images/img' + str(i) + '.png', res)
    print(i)
