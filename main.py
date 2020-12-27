import random
import re
import smtplib
import config

participantes={}
correos = []
grupos={} 

def enviar_email(msg, destinatario): #ENVÍO DE MENSAJES POR SMTP
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()        
    server.login(config.remitente,config.clave)
    server.sendmail(config.remitente, destinatario,msg)
    server.quit()

def repartidor(correos, participantes,grupos): #REPARTE LOS AMIGOS CON LA LISTA DE CORREOS Y PARTICIPANTES
    correos_regalan = list(correos)#SE CREAN DOS LISTAS PARA PODER DIFERENCIAR QUIEN FALTA POR REGALAR Y QUIEN FALTA POR RECIBIR
    correos_reciben = list(correos)

    while len(correos_regalan)!=0 and len(correos_reciben)!=0:
        random.shuffle(correos_regalan)#SE MEZCLAN LAS LISTAS CADA VEZ QUE SE BORRA UN ELEMENTO DE ELLAS
        random.shuffle(correos_reciben)#SEGURO QUE SE PUEDE MODIFICAR Y OPTIMIZAR
        if grupos!=1:
            if correos_reciben[0] != correos_regalan[0] and grupos[correos_reciben[0]]!=grupos[correos_regalan[0]]:#SEGURAMENTE SE PUEDE OPTIMIZAR PARA NO REPETIR EL CODIGO
                msg = "Le tienes que regalar algo a "+str(participantes[correos_reciben[0]])
                destinatario = correos_regalan[0]
                enviar_email(msg, destinatario)
                print(msg)
                correos_reciben.remove(correos_reciben[0])
                correos_regalan.remove(correos_regalan[0])
        else:
            if correos_reciben[0] != correos_regalan[0]:#AQUÍ ES DONDE SE REPITE
                msg = "Le tienes que regalar algo a "+str(participantes[correos_reciben[0]])
                destinatario = correos_regalan[0]
                enviar_email(msg, destinatario)
                print(msg)
                correos_reciben.remove(correos_reciben[0])
                correos_regalan.remove(correos_regalan[0])

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
        restr = int(input("1.Si\n2.No\n -->"))
        if restr==1:
            break
        if restr==2:
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
    #try:
    if restr:
        repartidor(correos,participantes,grupos)
    else:
        repartidor(correos, participantes,1)#LE DAS COMO VALOR DE grupos = 1 PARA QUE NO COMPARE NINGUN VALOR DE LOS GRUPOS
    #except:
        #print("Ha surgido un error en el envío. Por favor, inténtelo de nuevo.")
    
    pass
