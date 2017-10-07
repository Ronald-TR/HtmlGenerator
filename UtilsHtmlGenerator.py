import pytesseract as ocr
import cv2

from PIL import Image

reservedtags = {
    'HISTORIA : ': '<div class="container {appendClass} " align="center"><h4>{dadosTag}</h4></div>',
    'botao : ': '<button class="btn btn-primary {appendClass}" type="" name="" value="">{dadosTag}</button>',
    'entrada de texto : ': '<input class="form-control {appendClass}" type="text" placeholder="{dadosTag}"/>',
    'imagem : ': '<div align="center"><img src="{dadosTag}" /></div>',
    'fundo : ': 'flgstyle class=" {appendClass} " style = "background: url(\'{dadosTag}\');-webkit-background-size: cover; -moz-background-size: cover;-o-background-size: cover; background-size: cover;"',
}


def replacecolor(imgtemp):
    (rows, cols, depth) = imgtemp.shape

    for row in range(rows):
        for col in range(cols):
            pixel = imgtemp[row][col]
            (r, g, b) = pixel.tolist()
            if r > 17:
                imgtemp[row][col] = (255, 255, 255)
    return imgtemp


def analyzeTag(cv2img, tagsAvailable=reservedtags):
    dictparams = {
        'appendClass': '',
        'dadosTag': ''
    }

    cv2img = cv2.cvtColor(cv2img, cv2.COLOR_RGB2GRAY)

    ret, thresh = cv2.threshold(cv2img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    instrucao = ocr.image_to_string(Image.fromarray(thresh), lang='por')
    if instrucao != '':
        for tag, value in tagsAvailable.items():
            if instrucao.startswith('jumbo + '):
                instrucao = instrucao.replace('jumbo + ', '')
                dictparams['appendClass'] = 'jumbotron'
            if instrucao.startswith(tag):
                dictparams['dadosTag'] = instrucao.replace(tag, '').replace('\n', '<br>')
                return value.format(**dictparams)
    return ''
