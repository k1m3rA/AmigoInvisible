import random
import re
import smtplib
import config
from email.mime.text import MIMEText

participantes={}
correos = []
grupos={}
server = smtplib.SMTP(config.host,config.port)

def enviar_email(msg): #ENVÍO DE MENSAJES POR SMTP
            
    server.sendmail(msg['From'], msg['To'],msg.as_string().encode('utf8'))#EL ENCODE PERMITE EL ENVÍO DE CARACTERES ESPECIALES
    

def contenido_email(participantes,correos_reciben,correos_regalan):
    texto = "Le tienes que regalar algo a "+str(participantes[correos_reciben[0]])
    msg = MIMEText(texto.encode('utf-8'), _charset='utf-8')
    msg['Subject'] = 'Amigo Invisible'
    msg['From'] = config.remitente
    msg['To'] = correos_regalan[0]
    try:
        enviar_email(msg)
        print("{}({}) ya tiene amigo invisible.".format(participantes[msg['To']],msg['To']))
    except:
        print("Ha surgido un error, {} no tiene amigo invisible y {} no recibirá ningún regalo.".format(msg['To'],correos_reciben[0]))
    correos_reciben.remove(correos_reciben[0])
    correos_regalan.remove(correos_regalan[0])

def repartidor(correos, participantes,grupos): #REPARTE LOS AMIGOS CON LA LISTA DE CORREOS Y PARTICIPANTES
    correos_regalan = list(correos)#SE CREAN DOS LISTAS PARA PODER DIFERENCIAR QUIEN FALTA POR REGALAR Y QUIEN FALTA POR RECIBIR
    correos_reciben = list(correos)
    server.starttls()
    server.login(config.remitente,config.clave)
    while len(correos_regalan)!=0 and len(correos_reciben)!=0:
        random.shuffle(correos_regalan)#SE MEZCLAN LAS LISTAS CADA VEZ QUE SE BORRA UN ELEMENTO DE ELLAS
        random.shuffle(correos_reciben)#SEGURO QUE SE PUEDE MODIFICAR Y OPTIMIZAR
        if grupos!=1:
            if correos_reciben[0] != correos_regalan[0] and grupos[correos_reciben[0]]!=grupos[correos_regalan[0]]:#SEGURAMENTE SE PUEDE OPTIMIZAR PARA NO REPETIR EL CODIGO
                contenido_email(participantes,correos_reciben,correos_regalan)
        else:
            if correos_reciben[0] != correos_regalan[0]:
                contenido_email(participantes,correos_reciben,correos_regalan)
    server.quit()

def es_correo_valido(correo): #COMPROBAR CORREO VALIDO
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"#PARA MAS INFO -->https://parzibyte.me/blog/2018/12/04/comprobar-correo-electronico-python/
    return re.match(expresion_regular, correo) is not None

def introducir_datos(num_participantes,num_grupos):#INTRODUCCIÓN DE DATOS
    for i in range(num_participantes): 
        while True:
            nombre = str(input("Introduzca el nombre del "+str(i+1)+"º participante: "))#NOMBRES
            correo = str(input("Introduzca el correo del "+str(i+1)+"º participante: "))#CORREOS
            if num_grupos>1:
                grupo = str(input("Introduzca el grupo al que pertenece el "+str(i+1)+"º participante: "))#GRUPOS
                grupos[correo]=grupo#SE AÑADEN ELEMENTOS AL DICCIONARIO DE GRUPOS

            if es_correo_valido(correo):
                correos.append(correo)#SE AÑADEN ELEMENTOS A LA LISTA DE CORREOS
                participantes[correo]=nombre#SE AÑADEN ELEMENTOS AL DICCIONARIO DE NOMBRES
                break
            else:
                print("Introduzca un correo válido.")
    if num_grupos>1:
        return list(correos), dict(participantes), dict(grupos)
    else:
        return list(correos), dict(participantes)

def cantidades(msg):#NUMERO DE PARTICIPANTES
    while True: 

        try:
            cantidad = int(input(msg))
            if cantidad<=1:
                print("Debe ser un valor mayor a 1.")
            else:   
                break
        except:
            print("Introduzca un número válido.\n")
    return cantidad

def opciones():#ACTIVAR OPCIONES ADICIONALES (RESTRICCION DE GRUPOS, DONDE LOS MIEMBROS DE UN MISMO GRUPO NO PUEDEN SER AMIGOS)
    while True:
        print("¿Quiere restringir por grupos?")
        restr = input("1.Si\n2.No\n --> ")
        if restr=='1' or restr=='Si' or restr=='si' or restr=='s' or restr=='S' or restr=='SI':
            break
        if restr=='2' or restr=='No' or restr=='ni' or restr=='n' or restr=='N' or restr=='NO':
            restr=False
            break
        else:
            print("Introduzca una de las opciones existentes.\n")
    return restr

if __name__ == "__main__":#INICIO DEL PROGRAMA E HILO PRINCIPAL
    restr = opciones()
    msg="Introduzca número de participantes: "
    num_participantes = cantidades(msg)
    if restr:#SI HAY RESTRICCIÓN DE GRUPO EL FLUJO SIGUE POR AQUÍ
        msg="Introduzca número de grupos: "
        num_grupos=cantidades(msg)
        correos, participantes, grupos = introducir_datos(num_participantes, num_grupos)
    else:
        correos, participantes = introducir_datos(num_participantes,1)#LE DAS COMO VALOR DE num_grupos 1 PARA QUE NO PIDA ESE DATO
    try:
        if restr:
            repartidor(correos,participantes,grupos)
        else:
            repartidor(correos, participantes,1)#LE DAS COMO VALOR DE grupos = 1 PARA QUE NO COMPARE NINGUN VALOR DE LOS GRUPOS
    except:
        print("Ha surgido un error en el envío. Por favor, inténtelo de nuevo.")
    
    pass
