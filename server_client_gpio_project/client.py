#!/usr/bin/env python
import socket, sys

HEADER = 64
FORMAT = 'utf-8'
#DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = socket.gethostbyname(socket.gethostbyname())

def socket_client():
    try:
        PORT=int(input("enter PORT number: "))
        SERVER=str(input("enter IP adress: "))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[New socket] {client} is made.")

        client.connect((SERVER,PORT))
        while True:
            
            message= input("enter a message: ") 
            if message == "":
                client.close()
                break
            else:
                client.sendall(message.encode(FORMAT))
            print("message recieved ", client.recv(PORT).decode(FORMAT))

    except KeyboardInterrupt:
        print("\n keyboard interrupt")
        client.close()
        sys.exit()

    except socket.error as msg:
        print('failed to create socket with error code: ' + str(msg.args[0]) + ', error message: ' + msg.args[1])
        sys.exit()
print('hi')
    
if __name__ == '__main__':
    socket_client()
