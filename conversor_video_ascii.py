import cv2
import subprocess
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from sys import argv
import os




def image_to_ascii(image_path , resolucion):

    img = Image.open(image_path)
    #escalo la imagen 
    width, height = img.size
    aspect_ratio = height/width
    new_width = resolucion
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    # nuevo tamaño
    # print(img.size)

    # convierto la imagen a escala de grises
    img = img.convert('L')

    pixels = img.getdata()

    #Reemplazo los pixeles por los pixeles del array
    chars = ["B","S","#","&","@","$","%","*","!",":","."]
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    #pongo los caracteres como strings de longitud igual 
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    return(ascii_image)


#agarra todos los cuadros del video
def video_to_frames(video_name):
    vidcap = cv2.VideoCapture(video_name)
    success,image = vidcap.read()
    count = 0
    print('Converting video to frames')
    while success:
        cv2.imwrite("frames/{:015d}.jpg".format(count), image)     # save frame as JPEG file      
        print('creado frame {}'.format(count))
        success,image = vidcap.read()
        count += 1
    print('Done from video to frames')

#convierte todos los cuadros del video en ascii
def convert_frames():
    path = str(os.popen('pwd').read()).replace('\n' , '') + '/'
    path += 'frames'
    lista_frames = []
    for i in os.listdir(path):
        name = '{}/{}'.format(path,i)
        lista_frames.append(name)
    print('Lista Frames : Done')
    lista_frames.sort()
    return(lista_frames)


#retorna una lista con cada cuadro del video escrita en ascii art
def lista_cuadros_ascii_text(resolucion):
    lista_cuadros = []
    lista =  convert_frames()
    cont = 0
    print('Creando Lista Cuadros')
    for i in lista:
        ascii_image = image_to_ascii(i , resolucion)
        lista_cuadros.append(ascii_image)
#        print(cont)
#        print(ascii_image)
        cont += 1
    print('Lista Cuadros Texto creada')
    return(lista_cuadros)

#permite intertar texto centrado en una imagen
def create_image_text(anchura , largura , texto , nombre):
    image_width = anchura
    image_height = largura
    img = Image.new('RGB', (image_width, image_height), color='black')

    canvas = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text_width, text_height = canvas.textsize(texto , font=font)

    x_pos = int((image_width - text_width) / 2)
    y_pos = int((image_height - text_height) / 2)

    canvas.text((x_pos, y_pos), texto , font=font, fill='#FFFFFF')

    img.save(nombre + '.png')


#pasa por la lista que contiene el ascii art de cada cuadro y por cada cuadro crea una imagen que contiene el ascii art
def crear_imagenes_png_ascii(resolucion):
    lista_cuadros_en_ascii = lista_cuadros_ascii_text(resolucion)
    cont = 0
    print('Creando Imagenes Ascii ... ')
    for i in lista_cuadros_en_ascii:
        name = 'cuadros_ascii/{:015d}'.format(cont)
        cont += 1
        print('{}/{} imagenes procesadas'.format(cont,len(lista_cuadros_en_ascii)))
        create_image_text(resolucion*6 , resolucion*6 , i , name)
    print('Done Creando Imagenes')

#agarra todas las imagenes que contienen ascii art y crea un video de 24 cuadros por segundo
def crear_video(audio):
    #cambie el regex de %d a %04d
    os.system('ffmpeg -r 24 -f image2 -s 1920x1080 -i cuadros_ascii/%015d.png -i {} -vcodec libx264 -crf 25  -pix_fmt yuv420p ascii_video.mp4'.format(audio))

#borra todas las cosas que se crearon
def clean():
    os.system('rm frames/*')
    os.system('rm cuadros_ascii/*')
    print('Todo limpio y video creado')

#main
def run():
    os.system('mkdir cuadros_ascii')
    os.system('mkdir frames')
    nombre_video = argv[1]
    nombre_audio = argv[2]
    resolucion =  int(argv[3])
    video_to_frames(nombre_video)
    crear_imagenes_png_ascii(resolucion)#dejemolo abierto para que se pueda modificar la resolucion
    crear_video(nombre_audio)
    clean()
    os.system('rm -rf cuadros_ascii')
    os.system('rm -rf frames')

if(len(argv) == 4):
    run()
else:
    print('Uso:')
    print('python3 {} <video.mp4> <audio.mp3> <resolucion(numero)>'.format(argv[0]))
