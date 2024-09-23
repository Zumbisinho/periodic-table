## Feito por Zumbisinho

import json
import os
import math
from PIL import Image, ImageDraw, ImageFont

image_path = 'template.png' ##Mude para o nome e extensão do arquivo colocano na mesma pasta que o main.py

output = 'output' ##A pasta onde será colocado as imagens geradas + folhas otimizadas
    
ate_elemento = 118 ##Qualquer Número atômico de 1-118
cor = (1, 0, 0)  ## Cor do texto/Numeros

##Definições da folha
dpi = 300
largura_a4 = int(21 * dpi / 2.54)
altura_a4 = int(29.7 * dpi / 2.54)
a4_tamanho = (largura_a4, altura_a4)
y_offset = int(20) ##Definição de pixeis de separamento entre imagens


if not os.path.exists(output):
    os.makedirs(output)


font = ImageFont.truetype("arial.ttf", 100)  
font3 = ImageFont.truetype("arial.ttf", 60)  
font4 = ImageFont.truetype("arial.ttf", 50)
font2 = ImageFont.truetype("arial.ttf", 30)  


with open('lista.json', 'r',encoding='utf-8') as file:
    data = json.load(file)


for index in range(ate_elemento): #118
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)    
    numero_procurado = index + 1
    elemento_encontrado = next((elemento for elemento in data['elements'] if elemento['number'] == numero_procurado), None)

    shel = (elemento_encontrado['shells'])

    for i in range(len(shel)):
        numero = str(shel[i])
        posicao_desejada = (140 + (288 * i), 155)


        ##nao mexer pq nem deus sabe oq faz
        bbox = draw.textbbox((0, 0), numero, font=font)
        largura_texto = bbox[2] - bbox[0]
        altura_texto = bbox[3] - bbox[1]
        posicao_x = posicao_desejada[0] - (largura_texto / 2)
        posicao_y = posicao_desejada[1] - (altura_texto / 2)
        draw.text((posicao_x, posicao_y), numero, fill=cor, font=font)
    draw.text((0,300),str(numero_procurado),fill=(202,202,202),font=font2)

    folder = os.path.join(output,f'{numero_procurado}.png')
    image.save(folder)

    print(f'imagem pronta! ({118 - numero_procurado})')

input = input('Otimizar a quantidade por folhas? (Y/N)')

if input == 'Y':
    image = Image.open(image_path)
    imagems_por_folha = math.floor((a4_tamanho[1] - y_offset) / (image.height + y_offset))
    folhas_totais = math.ceil(ate_elemento / imagems_por_folha)
    imagem_anterior = 0
    indice_imagem = 0
    for folha in range(folhas_totais):
        a4_imagem = Image.new('RGBA', a4_tamanho, (255, 255, 255, 0)) ## Reload o a4
        offset_do_y=y_offset

        if folha +1 != folhas_totais:
            imagens = []
            for img in range(imagems_por_folha):
                indice_imagem = indice_imagem + 1
                if indice_imagem > ate_elemento:  # Não tentar adicionar mais imagens que o total
                    break
                caminho_imagem = os.path.join(output, f'{indice_imagem}.png')
                print(indice_imagem)
                if os.path.exists(caminho_imagem):
                    imagens.append(Image.open(caminho_imagem))

            for index,imagem in enumerate(imagens):
                a4_imagem.paste(
                    imagens[index],
                    ((a4_imagem.width // 2) - (imagem.width // 2), offset_do_y),
                )
                offset_do_y += imagem.height + y_offset  # Incrementar o offset vertical
                imagem_anterior += 1
            desenho = ImageDraw.Draw(a4_imagem)
            desenho.text((0,0),text=f'{folha + 1} - {folhas_totais - 1}',fill=(10,0,0),font=font3)
            desenho.text((0,(a4_imagem.height - 80)),text=f'https://github.com/Zumbisinho/periodic-table',fill=(188, 255, 160),font=font3)
            a4_imagem.save(os.path.join(output,f'otimizado_{folha}.png'))
