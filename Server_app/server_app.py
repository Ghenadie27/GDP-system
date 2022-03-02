import socket
import threading
import datetime
from database import db, sensors

db.create_all()

CAP = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DECONECTARE = "!DISCONNECT"
racire = bool
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def gestiune_client(con, adr):
    print(f"[CONEXIUNE NOUĂ] {adr[0]} conectat.\n")
    numarator_1 = 1
    numarator_2 = 1
    numarator_3 = 1
    conectat = True

    while conectat:
        msg = con.recv(CAP).decode(FORMAT)
        if adr[0] == ('client_1_IP_address'):
            if numarator_1 == 1:
                acum = datetime.datetime.now()
                timp = (acum.strftime("%Y-%m-%d %H:%M:%S"))
                temperatura = msg
                numarator_1 += 1
                if float(temperatura) >= 22:
                    global racire
                    racire = True
                else:
                    racire = False
            elif numarator_1 == 2:
                umiditatea = msg
                numarator_1 += 1
            elif numarator_1 == 3:
                rand = sensors(denumire="Depozitare", timp=timp, temperatura=temperatura, umiditatea=umiditatea)
                db.session.add(rand)
                db.session.commit()
                numarator_1 = 1

        if adr[0] == ('client_2_IP_address'):
            if numarator_2 == 1:
                acum = datetime.datetime.now()
                timp = (acum.strftime("%Y-%m-%d %H:%M:%S"))
                temperatura = msg
                numarator_2 += 1
                if float(temperatura) >= 22:
                    racire = True
                else:
                    racire = False
            elif numarator_2 == 2:
                umiditatea = msg
                numarator_2 += 1
            elif numarator_2 == 3:
                rand = sensors(denumire="Receptie", timp=timp, temperatura=temperatura, umiditatea=umiditatea)
                db.session.add(rand)
                db.session.commit()
                numarator_2 = 1

        if adr[0] == ('client_3_IP_address'):
            if numarator_3 == 1:
                acum = datetime.datetime.now()
                timp = (acum.strftime("%Y-%m-%d %H:%M:%S"))
                temperatura = msg
                numarator_3 += 1
                if float(temperatura) >= 22:
                    racire = True
                else:
                    racire = False
            elif numarator_3 == 2:
                umiditatea = msg
                numarator_3 += 1
            elif numarator_3 == 3:
                rand = sensors(denumire="Expeditie", timp=timp, temperatura=temperatura, umiditatea=umiditatea)
                db.session.add(rand)
                db.session.commit()
                numarator_3 = 1

        if adr[0] == ('client_4_IP_address'):
            if racire:
                con.send("1".encode(FORMAT))
            else:
                con.send("0".encode(FORMAT))
            print(racire)

        if msg == DECONECTARE:
            conectat = False

    con.close()


def start():
    server.listen()
    print(f"Serverul ascultă IP {SERVER}")

    while True:
        con, adr = server.accept() #asteapta o noua conexiune la server
        fir = threading.Thread(target=gestiune_client, args=(con, adr))
        fir.start()
        print(f"[CONEXIUNI ACTIVE] {threading.active_count()-1}")


print("[START] serverul porneste ... ")
start()
