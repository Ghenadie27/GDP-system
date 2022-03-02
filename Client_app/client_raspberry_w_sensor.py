import GPIO as GPIO
import board
import adafruit_dht
import datetime
import time
import os
import socket
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///s1.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.create_all()


CAP = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
DECONECTARE = "!DECONECTAT"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(('', 5050))


def conexiune():
    client.connect(ADDR)


def send(msg):
    mesaj = msg.encode(FORMAT)
    lungime_mes = len(mesaj)
    lungime_trimis = str(lungime_mes).encode(FORMAT)
    lungime_trimis += b' '*(CAP - len(lungime_trimis)) # b - byte format
    client.send(lungime_trimis)
    client.send(mesaj)
    print(client.recv(2048).decode(FORMAT))


class citiri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timp = db.Column(db.String(120), nullable=False)
    temperatura = db.Column(db.String(120), nullable=False)
    umiditatea = db.Column(db.String(120), nullable=False)


DHT_SENSOR = adafruit_dht.DHT22(board.D4)
comanda = "shutdown"
comanda += " -r" + " +" + str(1)


def citire():
    while True:
        temperatura = DHT_SENSOR.temperature
        umiditatea = DHT_SENSOR.humidity
        temperatura="{0:0.1f}".format(temperatura)
        umiditatea="{0:0.1f}".format(umiditatea)
        acum = datetime.datetime.now()
        timp = (acum.strftime("%Y-%m-%d %H:%M:%S"))

        if temperatura is not None and umiditatea is not None:
            rand = citiri(timp=timp, temperatura=temperatura, umiditatea=umiditatea)
            db.session.add(rand)
            db.session.commit()
            rand = [{timp}, {temperatura}, {umiditatea}]
            with open('s1.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rand)
            print(timp, "Temperatura = ", temperatura, "Umiditatea = ", umiditatea)
            time.sleep(1.0)
            send(timp)
            time.sleep(1.0)
            send(temperatura)
            time.sleep(1.0)
            send(umiditatea)
            time.sleep(1.0)
            send(DECONECTARE)
        else:
            print("Eroare!")
            GPIO.cleanup()
            time.sleep(10.0)
            continue
        time.sleep(5.0)


try:
    conexiune()
    citire()
except KeyboardInterrupt:
    print("Programul se inchide!")
except TimeoutError:
    print("TimeOut")
    time.sleep(10.0)
    os.system(comanda)
except ConnectionResetError:
    print("ConnectionReset")
    time.sleep(10.0)
    os.system(comanda)
except OSError:
    print("OSError")
    time.sleep(10.0)
    os.system(comanda)
except RuntimeError:
    print("RunTimeError")
    time.sleep(10.0)
    os.system(comanda)


