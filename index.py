import uuid
from cv2 import data
import imutils
import cv2
import numpy as np
import os
import json
from flask import Flask, render_template, Response, jsonify, request, url_for
import pyautogui
import webbrowser as web
from time import sleep
import emoji

app = Flask(__name__)

dataPath = 'C:/Users/usuario/Desktop/app-flask - copia/data'  # Cambia a la ruta donde hayas almacenado Data
imagePaths = os.listdir(dataPath)

# -------------METODOS
# method= 'EigenFaces'
# method= 'FisherFaces'
method = 'LBPH'

if method == 'EigenFaces': emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
if method == 'FisherFaces': emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
if method == 'LBPH': emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

# -------------leyendo modlos
emotion_recognizer.read('modelo' + method + '.xml')
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camara = cv2.VideoCapture(0)
word = ""
emotions = []


def generador_frames():
    while True:
        ok, imagen = obtener_frame_camara()
        if not ok:
            break
        else:
            # Regresar la imagen en modo de respuesta HTTP
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + imagen + b"\r\n"


def obtener_frame_camara():
    ok, frame = camara.read()
    if ok == False: return False, None
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    # nFrame = cv2.hconcat([frame,np.zeros((480,300,3),dtype=np.uint8)])
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = emotion_recognizer.predict(rostro)

        cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

        if method == 'LBPH':
            if result[1] < 60:
                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                word = imagePaths[result[0]]
                emotions.append(word)
                # print(word)
                # image = emotionImage(imagePaths[result[0]])
                # nFrame = cv2.hconcat([frame])
            else:
                cv2.putText(frame, 'No identificado', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # nFrame = cv2.hconcat([frame,np.zeros((480,300,3),dtype=np.uint8)])

    _, bufer = cv2.imencode(".jpg", frame)
    imagen = bufer.tobytes()
    return True, imagen


@app.route("/mostrarCamara")
def mostrarCamara():
    return Response(generador_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/emojis', methods=['POST'])
def emojis():
    word = emotions.pop()
    print(word)
    return json.dumps({'emotion': word});


@app.route('/wpp/<emotion>', methods=['POST'])
def wpp(emotion):
    print(emotion)
    # word=emotion.pop()
    web.open("https://web.whatsapp.com/")
    sleep(25)
    if (emotion == "Felicidad"):
        print(emotion)
        message = emoji.emojize(':smiling_cat_face_with_open_mouth:', use_aliases=True)
        pyautogui.typewrite(message)
    elif (emotion == "Tristeza"):
        message = emoji.emojize(':weary_cat_face:', use_aliases=True)
        pyautogui.typewrite(message)
    elif (emotion == "Enojo"):
        message = emoji.emojize(':pouting_cat_face:', use_aliases=True)
        pyautogui.typewrite(message)
    elif (emotion == "Sorpresa"):
        message = emoji.emojize(':surprised_face:', use_aliases=True)
        pyautogui.typewrite(message)
    pyautogui.press("enter")
    sleep(1)
    pyautogui.press("enter")


@app.route('/')
def principal():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
