import cv2
import numpy as np
from UtilsHtmlGenerator import *

from PIL import Image, ImageFilter, ImageOps

HTML = """
<!DOCTYPE html>
<html lang="por">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset="UTF-8">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <title>%s</title>
</head>
<body>
%s

<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
</html>
"""

bodyteste = []

marginx = 0
marginy = 0



def addBody(imgdiv, imgcolorida, contour, tab=1):
    nx, ny, nw, nh = cv2.boundingRect(contour)
    marginx = nx
    marginy = ny

    nx = nx + 10
    ny = ny + 10
    nw = nw - 20
    nh = nh - 20


    cutimg = imgdiv[ny:ny+nh, nx:nx+nw]

    cutcolorida = imgcolorida[ny:ny+nh, nx:nx+nw]

    img2, cont2, hier2 = cv2.findContours(cutimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    tagAnalyzed = ''

    if len(cont2) == 0: # verifico se a box possui box filhas, se possuir eu não analizo textos (redução alta de custos de processamento)
        tagAnalyzed = analyzeTag(np.asarray(ImageOps.flip(Image.fromarray(cutcolorida))).astype(np.uint8))

    tabs = ''.join('\t' for i in range(tab))
    obody = tabs + tagAnalyzed + '\n'
    if tagAnalyzed.startswith('flgstyle'):
        bodyteste[-1:] = tabs + '<div {tagOptions}>\n'.format(**{'tagOptions': tagAnalyzed.replace('flgstyle', '')})
        obody = ''
        
    if tagAnalyzed == '':
        #obody = tabs + '<div class="container" style="width: %ipx; height: %ipx; margin: %ipx %ipx">\n' % (nw, nh, 0, 0)
        obody = tabs + '<div class="container">\n'
        bodyteste.append(obody)
    else:
        #obody = tabs + '<div style="width: %ipx; height: %ipx; margin: %ipx %ipx">\n' % (nw, nh, 0, 0)
        bodyteste.append(obody)

    if not len(cont2) == 0:
        for i in cont2:
            addBody(cutimg, cutcolorida, i, tab + 1)
        bodyteste.append(tabs + '</div>\n')
        return None
    elif tagAnalyzed == '':
        bodyteste.append(tabs + '</div>\n')
        return None


imgColorida = Image.open('login.jpg').convert('RGB')

imgColoridaParaCv2 = np.asarray(imgColorida).astype(np.uint8) # rever

imgtemp = Image.fromarray(replacecolor(imgColoridaParaCv2)) # rever esta redundancia

imgColoridaParaCv2 = np.asarray(ImageOps.flip(imgColorida)).astype(np.uint8) # rever

imgLimpaParaCv2 = np.asarray(ImageOps.invert(ImageOps.flip(imgtemp)).convert('L')).astype(np.uint8)
img, cont, hier = cv2.findContours(imgLimpaParaCv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for indice, c in enumerate(cont):
    x, y, w, h = cv2.boundingRect(c)
    addBody(imgLimpaParaCv2, imgColoridaParaCv2, c)

with open('index.html', 'w') as filehtml:
    filehtml.write(HTML % ('Testando Gerador HTML', ''.join(bodyteste)))

print(HTML % ('Testando Gerador HTML', ''.join(bodyteste)))
