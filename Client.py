import socket
from Packet import Packet
import json
import ast

class Client:
    client = None
    host = "localhost"
    port_number = 6000
    uid = None
    user_name = None
    header_size = 1024
    received_message = ""
    msg = None
    close = False

    def __init__(self, uid):
        self.user_name = input("Welcome! Please enter a name to use while chatting:")
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        #print("Socket created.")
        self.uid = uid
        self.client.connect((self.host, self.port_number))
        print("Connection established with the server.")
        ## send username info
        print("Sending msg with username info to the server:")
        packet = Packet(self.uid,self.user_name, f"hello server. {self.user_name} here requesting a uid.")
        json_pkt = json.dumps(packet.__dict__)
        self.client.send(json_pkt.encode())
        msg_in = self.client.recv(self.header_size).decode("utf-8")
        msg_in = msg_in.split("$")
        self.uid = msg_in[0]
        print(f"currently connected clients: {msg_in[1]}")

    def receive_msg(self):
        msg_in = self.client.recv(self.header_size).decode("utf-8")
        msg_in = ast.literal_eval(msg_in)


        if(msg_in['uid']==0):
            self.received_message = f"{msg_in['message']}"
            print(self.received_message)
            self.received_message = ""
        elif(self.uid != msg_in['uid']):
            self.received_message = f"{msg_in['uid']}: {msg_in['message']}"
            print(self.received_message)
            self.received_message = ""
        elif(msg_in["message"][:5]==".exit"):
            #self.close_connection()
            self.close = True

    def get_input(self):
        self.msg = input()
        packet = Packet(self.uid,self.user_name, self.msg)
        json_pkt = json.dumps(packet.__dict__)
        self.client.send(json_pkt.encode())

    def close_connection(self):
        print("Terminating the Connection.")
        self.client.close()