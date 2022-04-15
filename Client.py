import socket
from Packet import Packet
import json

class Client:
    client = None
    host = "localhost"
    port_number = 6000
    uid = None
    user_name = None
    header_size = 1024
    received_message = False
    prompt_displayed = False

    def __init__(self, uid):
        self.user_name = input("Welcome! Please enter a name to use while chatting:")
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        print("Socket created.")
        self.uid = uid

    def handle(self):
        self.client.connect((self.host, self.port_number))
        print("Connection established with the server.")

        while True:
            #thread listening for input from server or thread listening for input from user
            if self.received_message:
                ## display received message(s)
                print("received")
                self.prompt_displayed = False
            else:
                if(not self.prompt_displayed):
                    msg = self.get_input()
                    self.prompt_displayed = True
            # msg = f"Hi I am a TCP client with id: {self.uid} created by {self.user_name}."
            print("Sending msg to the server:", msg)
            packet = Packet(self.uid,self.user_name, msg)
            json_pkt = json.dumps(packet.__dict__) 
            self.client.send(json_pkt.encode())
            msg_in = self.client.recv(self.header_size).decode("utf-8")
            print("Ack from the server:",msg_in)
            print(msg_in)

            
          
    
    # maybe have a separate thread in charge of getting input from user
    def get_input(self):
        return input(">>> ")

    def close_connection(self):
        print("Terminating the Connection.")
        self.client.close()