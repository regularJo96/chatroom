import socket
import threading
import ast
import random

class Server:

    server = None
    host = "localhost"
    port_number = 6000
    connections = []
    clients = []
    uids = []

    def __init__(self):
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        print("Socket created.")
        self.server.bind((self.host, self.port_number))
        print(f"Socket bound to address {self.host} and port number {self.port_number}")

    def start(self):
        def handle(self,client,client_addr):
            
            while(True):
                if(self.receive_msg(client)==False):
                    break
            client.close()
                
        self.server.listen(30)
        print("Listening for client.")
        while True:
            client, client_addr = self.server.accept()
            print("Connection established with client at address {}".format(client_addr))
            self.clients.append(client)


            thread = threading.Thread(target=handle, args=(self,client,client_addr))
            thread.start()

    def receive_msg(self,client):
        # message recieved (if already assigned a uid) will be a json string, in the form:
        # {"uid": "user_name+number", "user_name": "jojo", "message": "hello"} 

        msg = client.recv(1024).decode()
        #convert json string to python dict
        msg = ast.literal_eval(msg)
        if(msg["uid"]==0):
            #assign a uid to the connection
            print(f"{msg['user_name']} connected.")
            # print(msg["message"])
            uid = msg["user_name"] + str(self.gen_id())
            print(f"assigning {msg['user_name']} with uid {uid}")
            self.connections.append(uid)
            print(f"current connections {self.connections}")
            self.assign_uid(client,uid)
            msg["message"] = f"{uid} connected"
            self.send_conn_alert(client,msg)

        elif(msg["message"][:5]==".exit"):
            self.connections.remove(msg["uid"])
            self.send_close_ack(client,msg,msg["uid"])
            
            # change the uid to 0 after grabbing it so that the client registers that it's an
            # alert sent by the server
            uid = msg["uid"]
            msg["uid"] = 0
            msg["message"] = f"{uid} disconnected"
            self.send_conn_alert(client,msg)
            self.clients.remove(client)
            return False
            
        else:
            print(f"message received from {msg['uid']}/nsending acknowledgement to client.")
            self.send_ack(client,msg)
        return True
        
    def assign_uid(self,client,uid):
        print("sending uid to connection")
        msg_out = f"{uid}${self.connections}".encode()
        client.send(msg_out)

    def send_conn_alert(self,client,msg):
        msg_out = f"{msg}".encode()
        for client in self.clients:
            client.send(msg_out)

    def send_close_ack(self,client,msg,uid):
        print(f"connection with {uid} terminated.")
        client.send(f"{msg}".encode())
        print(f"current connections {self.connections}")

    def send_ack(self,client,msg):
        msg_out = f"{msg}".encode()
        for client in self.clients:
            client.send(msg_out)

    def gen_id(self):
        uid = random.randint(1,10000000)
        while(uid in self.uids):
            uid = random.randint(1,10000000)
        self.uids.append(uid)
        return uid