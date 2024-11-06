import socket
import sys
import threading
import socketserver
import os

UDP_IP = "141.60.1.1"
CHATTERS = []
UDP_PORT = 1141
USERNAME = "Alex"
SERVER_IP = "0"

USERNAME = input("Enter your Username: ")

if(sys.argv[1] != ""):
    CHATTERS.append(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(USERNAME + " joined the Chat.", "utf-8"), (UDP_IP, UDP_PORT))

MESSAGE = "(" + USERNAME + "): "
for i in range(1, len(sys.argv)):
    MESSAGE = MESSAGE + " " + sys.argv[i]

class MyUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):

        msgRecvd = self.rfile.readline().strip()
        if(not self.client_address[0] in CHATTERS):
            CHATTERS.append(self.client_address[0])
            send_message("/" + self.client_address[0])
        print(self.client_address[0] + msgRecvd.decode("utf-8"))

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def send_message(message):
    if(message[0] == "/"):
        if(message == "/exit"):
            exit()
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.sendto(bytes(message, "utf-8"), (i, UDP_PORT))
    else:
        for i in CHATTERS:
            message = "(" + USERNAME + "): " + message
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.sendto(bytes(message, "utf-8"), (i, UDP_PORT)) 

def background():
    listen_addr = ('0.0.0.0', 1141)

    socketserver.UDPServer.allow_reuse_address = True 

    serverUDP = socketserver.UDPServer(listen_addr, MyUDPHandler)
    serverUDP.serve_forever()

SERVER_IP = get_ip()
print("Host IP Address: " + SERVER_IP)
CHATTERS.append(SERVER_IP)

b = threading.Thread(name='background', target=background)

b.daemon = True

b.start()

while(1):
    send_message(input("> "))