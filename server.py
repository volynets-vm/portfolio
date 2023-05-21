from doctest import OutputChecker
import socket, sys, threading, time
from functions import lab1_task4
import  functions
import RPi.GPIO as GPIO

count = 0
flashing = False
numbers = False
one_occupied, two_occupied = False, False
numbers_state = 0
hz_flashing = 1 
hz_numbers = 1


def flashing_thread():
    global flashing
    led_pin = [3,5]
    GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.output(led_pin, GPIO.HIGH) 
    while True:
        if flashing == False:
            continue
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        time.sleep(hz_flashing)
        GPIO.output(3, GPIO.LOW)
        GPIO.output(5, GPIO.HIGH)
        time.sleep(hz_flashing)

        


def numbers_thread():
    functions.lab1_task4()

def system_messages(conn, addr):
    global flashing, numbers, one_occupied, two_occupied, hz_flashing, hz_numbers, numbers_state
    msg = conn.recv(1024)
    msg=msg.decode()
    

    while True:
        conn.sendall("Press 1 or 2".encode("utf-8"))
        msg = conn.recv(1024)
        msg=msg.decode()
        if msg == "1" and not one_occupied:
            conn.sendall("Flashing program: h - change freq, on - turn on, off- , status - ".encode("utf-8"))
            while True:
                msg = conn.recv(1024)
                msg=msg.decode()
                if msg == 'on':
                    flashing = True
                    conn.sendall("Flashing set on".encode("utf-8"))
                elif msg == 'off':
                    flashing = False
                    conn.sendall("Flashing set off".encode("utf-8"))
                elif 'hz' in msg:
                    hz_flashing = float(msg[2:])
                    conn.sendall(f"hz_flashing is set to {hz_flashing}".encode("utf-8"))
                elif msg == 'status':
                    conn.sendall(f"Flashing status is {flashing}".encode("utf-8"))
                elif msg == 'exit':
                    one_occupied = False
                    break
                else:
                    conn.sendall(f"Error?".encode("utf-8"))
        elif msg == '1':
            conn.sendall("Flashing program is occupied".encode("utf-8"))
        if msg == "2" and not two_occupied:
            conn.sendall("Flashing program: hz - change freq, on - turn on, off- , status -, state - s0,s1,s2 ".encode("utf-8"))
            while True:
                msg = conn.recv(1024)
                msg=msg.decode()
                if msg == 'on':
                    functions.stopper = False
                    conn.sendall("Flashing set on".encode("utf-8"))
                elif msg == 'off':
                    functions.stopper = False
                    conn.sendall("Flashing set off".encode("utf-8"))
                elif 'hz' in msg:
                    functions.hz = float(msg[2:])
                    conn.sendall(f"hz_flashing is set to {hz_flashing}".encode("utf-8"))
                elif msg == 'status':
                    conn.sendall(f"Flashing status is {functions.state}".encode("utf-8"))
                elif 's' in msg: # s1 state is 1
                    functions.state = int(msg[1])
                    conn.sendall(f"Flashing status is {functions.state}".encode("utf-8"))
                elif msg == 'exit':
                    two_occupied = False
                    break
                else:
                    conn.sendall(f"Error?".encode("utf-8"))
        elif "exit":
            conn.sendall("bye".encode("utf-8"))
        else:
            conn.sendall("error".encode("utf-8"))


def server():
    threading.Thread(target = flashing_thread).start()
    threading.Thread(target = numbers_thread).start()
    s = socket.socket()
    print ("socket is created")

    PORT = int(input("enter port: "))
    IP = str(input("enter IP: "))

    try:
        s.bind((IP,PORT))
        print ("socket connected to %s" %(PORT))
        s.listen(5)
        print ("listening...")
        
        while True:
            client, conn = s.accept()
            client.send("")
            threading.Thread(target=system_messages, args=(client, conn)).start()

    except KeyboardInterrupt:
        print("\n Keyboard interrupt")
        s.close()
        sys.exit()

    except socket.error as msg:
        print("failed to create socket, error message: "+ (msg.args[1]))
        sys.exit()

    finally:
        sys.exit()


server()
