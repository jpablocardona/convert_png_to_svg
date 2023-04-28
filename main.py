import os
import base64
import random
import string


path = 'input'
dest = 'output'
max_height = 100


def main(rezise=False):

    print(os.listdir(path))
    already = list(filter(lambda x: x.endswith(".png"), os.listdir(dest)))

    for i in list(filter(lambda x: x.endswith(".png"), os.listdir(path))):
        if i not in already:
            if rezise:
                rezise_image(path + '/' + i, max_height)
                print(i)
                with open(path + '/' + i.split(".png")[0] + '_resized.png', "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
            else:
                if i.endswith("resized.png"):
                    continue
                print(i)
                with open(path + '/' + i, "rb") as image_file:
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


def rezise_image(image_path, max_height=400):
    from PIL import Image
    # Open the original image
    image = Image.open(image_path, formats=['PNG'])

    # Get the dimensions of the original image
    width, height = image.size

    # Calculate the scaling factor
    scale_factor = max_height / height

    # Calculate the new width
    new_width = int(width * scale_factor)

    # Resize the image
    resized_image = image.resize((new_width, max_height))

    # Save the resized image
    resized_image.save(str(image_path).replace('.png', '_resized.png'))

if __name__ == '__main__':
    main()