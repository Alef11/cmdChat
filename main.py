import socket
import sys
import threading
import socketserver

UDP_IP = "141.60.1.1"
CHATTERS = []
UDP_PORT = 1141
USERNAME = "Alex"

USERNAME = input("Enter your Username: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(USERNAME + " joined the Chat.", "utf-8"), (UDP_IP, UDP_PORT))

print(sock.getsockname()[0])

MESSAGE = "(" + USERNAME + "): "
for i in range(1, len(sys.argv)):
    MESSAGE = MESSAGE + " " + sys.argv[i]

class MyUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):

        msgRecvd = self.rfile.readline().strip()
        if(not self.client_address[0] in CHATTERS):
            CHATTERS.append(self.client_address[0])
        print(self.client_address[0] + msgRecvd.decode("utf-8"))

def send_message(message):
    for i in CHATTERS:
        message = "(" + USERNAME + "): " + message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(bytes(message, "utf-8"), (i, UDP_PORT)) 

def background():
    listen_addr = ('0.0.0.0', 1141)

    socketserver.UDPServer.allow_reuse_address = True 

    serverUDP = socketserver.UDPServer(listen_addr, MyUDPHandler)
    serverUDP.serve_forever()

b = threading.Thread(name='background', target=background)

b.daemon = True

b.start()

while(1):
    send_message(input("> "))