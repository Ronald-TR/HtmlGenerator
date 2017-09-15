import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>%s</title>
</head>
<body>
%s
</body>
</html>
"""

bodyteste = []

marginx = 0
marginy = 0


def addBody(imgdiv, contour, tab=1):
    nx, ny, nw, nh = cv2.boundingRect(contour)
    marginx = nx
    marginy = ny
    tabs = ''.join('\t' for i in range(tab))
    if tab == 1:
        obody = tabs + '<div style="width: %ipx; height: %ipx; margin: %ipx %ipx">\n' % (nw, nh, 0, 0)
        bodyteste.append(obody)
    else:
        obody = tabs + '<div style="width: %ipx; height: %ipx; margin: %ipx %ipx">\n' % (nw, nh, 0, 0)
        bodyteste.append(obody)


    nx = nx + 10
    ny = ny + 10
    nw = nw - 20
    nh = nh - 20

    cutimg = imgdiv[ny:ny+nh, nx:nx+nw]

    img2, cont2, hier2 = cv2.findContours(cutimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not len(cont2) == 0:
        addBody(cutimg, cont2[0], tab + 1)
        bodyteste.append(tabs + '</div>\n')
        return None
    else:
        bodyteste.append(tabs + '</div>\n')
        return None

img = ImageOps.invert(Image.open('teste4.png'))
img = ImageOps.flip(img)

imagem_bin = np.asarray(img).astype(np.uint8)

imagem_bin_cinza = cv2.cvtColor(imagem_bin, cv2.COLOR_RGB2GRAY)

img, cont, hier = cv2.findContours(imagem_bin_cinza, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for indice, c in enumerate(cont):
    x, y, w, h = cv2.boundingRect(c)
    addBody(imagem_bin_cinza, c)

with open('index.html', 'w') as filehtml:
    filehtml.write(HTML % ('Testando Gerador HTML', ''.join(bodyteste)))

print(HTML % ('Testando Gerador HTML', ''.join(bodyteste)))
