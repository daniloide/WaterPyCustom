from PIL import Image
import constantes
import time
import utiles
import os
def obtener_x(anchura_marca_de_agua, anchura_imagen, posicion, separacion_horizontal):
    x = 0
    if posicion == constantes.OPCION_HORIZONTAL_IZQUIERDA:
        x = separacion_horizontal
    elif posicion == constantes.OPCION_HORIZONTAL_CENTRO:
        centro_imagen = anchura_imagen / 2
        centro_marca_de_agua = anchura_marca_de_agua / 2
        centro = centro_imagen - centro_marca_de_agua
        x = centro + separacion_horizontal
    elif posicion == constantes.OPCION_HORIZONTAL_DERECHA:
        x = anchura_imagen - separacion_horizontal - anchura_marca_de_agua
    return int(x)

def obtener_y(altura_marca_de_agua, altura_imagen, posicion, separacion_vertical):
    y = 0
    if posicion == constantes.OPCION_VERTICAL_ARRIBA:
        y = separacion_vertical
    elif posicion == constantes.OPCION_VERTICAL_CENTRO:
        centro_imagen = altura_imagen / 2
        centro_marca_de_agua = altura_marca_de_agua / 2
        centro = centro_imagen - centro_marca_de_agua
        y = centro + separacion_vertical
    elif posicion == constantes.OPCION_VERTICAL_ABAJO:
        y = altura_imagen - separacion_vertical - altura_marca_de_agua
    return int(y)
        

def crear_thumbnails(imagenes, ruta_salida):

    ruta_thumbnails = utiles.crear_directorio_de_thumbnails(ruta_salida)

    for ruta_imagen in imagenes:
        imagen = Image.open(ruta_imagen)
        anchura_imagen, altura_imagen = imagen.size

        # crear thumbnails
        if (altura_imagen > anchura_imagen):  # imagen vertical
            anchura_thumbnail = 120                    
            altura_thumbnail = int(120 * altura_imagen / anchura_imagen)
        else: # imagen horizontal o cuadrada
            altura_thumbnail = 120
            anchura_thumbnail = int(120 * anchura_imagen / altura_imagen)

        # redimensionar
        thumbnail_tamanio = (anchura_thumbnail, altura_thumbnail)
        thumbnail = imagen.resize(thumbnail_tamanio) 
        
        # crop
        thumbnail = thumbnail.crop((0, 0, 120, 120))

        thumbnail.save(os.path.join(ruta_thumbnails, os.path.basename(ruta_imagen)))

def poner_marca_de_agua(imagenes, marca_de_agua, **opciones):   


    
    # Leer los ajustes que el usuario puso
    porcentaje_opacidad = opciones.get("porcentaje_opacidad")
    separacion_vertical = opciones.get("separacion_vertical")
    separacion_horizontal = opciones.get("separacion_horizontal")
    opcion_alineamiento_horizontal = opciones.get("opcion_alineamiento_horizontal")
    opcion_alineamiento_vertical = opciones.get("opcion_alineamiento_vertical")
    
    # A trabajar. Le quitamos la opacidad a la imagen
    marca_de_agua = Image.open(marca_de_agua).convert("RGBA")
    anchura_marca_de_agua, altura_marca_de_agua = marca_de_agua.size

    for x in range(anchura_marca_de_agua):
        for y in range(altura_marca_de_agua):
            rgba = marca_de_agua.getpixel((x,y))
            nuevo_rgba = (rgba[0],rgba[1],rgba[2],int((porcentaje_opacidad * rgba[3]) / 100))
            marca_de_agua.putpixel((x,y), nuevo_rgba)
    # Crear directorio
    ruta_verdadera = utiles.crear_directorio_de_salida(os.path.dirname(imagenes[0]))
    # Y las procesamos
    for ruta_imagen in imagenes:
        imagen = Image.open(ruta_imagen)
        anchura_imagen, altura_imagen = imagen.size            
        
        # redimensionar imagen si la resolucion es muy alta (>1440)
        if (max(altura_imagen, anchura_imagen) > 1440):
            # calcular nueva resolucion            
            if (altura_imagen > anchura_imagen):  # imagen vertical
                anchura_imagen = int(1440 * anchura_imagen / altura_imagen)                    
                altura_imagen = 1440
            else: # imagen horizontal o cuadrada
                altura_imagen = int(1440 * altura_imagen / anchura_imagen)
                anchura_imagen = 1440
            # redimensionar
            nuevo_tamanio = (anchura_imagen, altura_imagen)
            imagen = imagen.resize(nuevo_tamanio)

        # redimensionar  marca de agua
        if (altura_imagen > anchura_imagen):  # imagen vertical
            anchura_marca_de_agua_custom = int(anchura_imagen/2) 
        else: # imagen horizontal o cuadrada
            if anchura_imagen/altura_imagen > 1.5: # horizontal estandar
                anchura_marca_de_agua_custom = int(anchura_imagen/4)
            else: # cuadrada o semi cuadrada (entre 1x1 y 1x1.5)
                anchura_marca_de_agua_custom = int(anchura_imagen/3)
        
        altura_marca_de_agua_custom = int(anchura_marca_de_agua_custom * altura_marca_de_agua / anchura_marca_de_agua)

        tamanio_custom = (anchura_marca_de_agua_custom, altura_marca_de_agua_custom)
        marca_de_agua_custom = marca_de_agua.resize(tamanio_custom)

        x = obtener_x(anchura_marca_de_agua_custom, anchura_imagen, opcion_alineamiento_horizontal, separacion_horizontal)
        y = obtener_y(altura_marca_de_agua_custom, altura_imagen, opcion_alineamiento_vertical, separacion_vertical)
        imagen.paste(marca_de_agua_custom, (x, y), marca_de_agua_custom)
        #nombre_imagen_guardada = "Salida_{}.png".format(time.time())
        imagen.save(os.path.join(ruta_verdadera, os.path.basename(ruta_imagen)))
        #print("Guardada como " + nombre_imagen_guardada)

    # crear thumbnails
    crear_thumbnails(imagenes, ruta_verdadera)
