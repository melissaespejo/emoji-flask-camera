import cv2
import os
import numpy as np
import time

def obtenerModelo(method, facesData, labels):
    if method == 'EigenFaces': emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
    else:
        if method == 'FisherFaces': emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
        else:
            if method == 'LBPH': emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
    #entrenar el reconocerdor
    print('Entrenando('+method+')...')
    inicio = time.time()
    emotion_recognizer.train(facesData, np.array(labels))
    tiempoEntrenamiento = time.time()-inicio
    print('Tiempo de entrenamiento ('+method+'):',tiempoEntrenamiento)

    #Almacenamos modelo obtenido
    emotion_recognizer.write('modelo'+method+'.xml')


dataPath = 'C:/Users/usuario/Desktop/emoji-whatsapp/reconocimiento emociones/data' #Cambia a la ruta donde hayas almacenado Data
emotionList = os.listdir(dataPath)
print('Lista de emociones: ', emotionList)

labels=[]
facesData =[]
label = 0

for nameDir in emotionList:
    emotionPath = dataPath + '/' + nameDir
    #print('Leyendo las imagenes')

    for fileName in os.listdir(emotionPath):
        labels.append(label)
        facesData.append(cv2.imread(emotionPath+'/'+fileName,0))
    label = label + 1

obtenerModelo('EigenFaces',facesData,labels)
obtenerModelo('FisherFaces',facesData,labels)
obtenerModelo('LBPH',facesData,labels)