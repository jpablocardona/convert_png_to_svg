import os
import base64
import random
import string

path = 'input'
dest = 'output'
print(os.listdir(path))
already = list(filter(lambda x: x.endswith(".png"), os.listdir(dest)))

for i in os.listdir(path):
    if i not in already:
        print(i)        
        with open(path+'/'+i, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        base64_txt = encoded_string.decode('utf-8')

        # Definir el contenido del SVG como una cadena de texto
        contenido_svg = '''
        <svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <rect width="110" height="110" fill="url(#pattern0)"/>
            <defs>
                <pattern id="pattern0" patternContentUnits="objectBoundingBox" width="1" height="1">
                    <use xlink:href="#$id" transform="scale(0.0025)"/>
                </pattern>
                <image id="$id" width="400" height="400" xlink:href="data:image/png;base64,$base64"/>
            </defs>
        </svg>
        '''

        # Definir valores para nuestras variables
        id = random.randint(1, 1000)
        variables = {
            'id': id,
            'base64': base64_txt,
        }

        # Crear una plantilla con la cadena de texto y los marcadores de posición
        plantilla = string.Template(contenido_svg)

        # Renderizar la plantilla con los valores de nuestras variables
        svg_final = plantilla.substitute(variables)

        # Escribir el archivo SVG
        with open('output/{}.svg'.format(i.replace('.png', '')), 'w') as f:
            f.write(svg_final)
