import socket
import threading
import ast

class Server:

    server = None
    host = "localhost"
    port_number = 6000
    running = False
    connections = []
    messages_stack = []

    def __init__(self):
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        print("Socket created.")
        self.server.bind((self.host, self.port_number))
        print(f"Socket bound to address {self.host} and port number {self.port_number}")

    def start(self):
        def handle(self,client,client_addr):
            
            while(True):
                print(self.messages_stack)
                state = self.receive_msg(client)
                #send out all messages in stack to all clients connected. Except the one that sent the message
                if(len(self.messages_stack) > 0):
                    for msg in self.messages_stack:
                        self.send_msg_to_all_connections(msg)
                    self.messages_stack = []
                if(state):
                    client.close()
                    
        self.server.listen(30)
        self.running = True
        print("Listening for client.")
        while True:
            client, client_addr = self.server.accept()
            print("Connection established with client at address {}".format(client_addr))
            self.connections.append(client)

            thread = threading.Thread(target=handle, args=(self,client,client_addr))
            thread.start()

    def is_running(self):
        return self.running

    def receive_msg(self,client):
        # message recieved will be a json string, in the form:
        # {"uid": 1, "user_name": "jojo", "message": "hello"} 

        msg = client.recv(1024).decode()
        print("Message received from the client:")

        #convert json string to python dict
        msg = ast.literal_eval(msg)
        print(msg["user_name"] + ": " + msg["message"])
        self.messages_stack.append(msg)
        self.send_ack(client,msg)
        return msg["message"].lower() in ["exit", "q", "quit", "leave"]
            

    def send_ack(self,client,msg):
        user_name = msg["user_name"]
        message = msg["message"]
        print("Sending acknowledgment to the client.")
        msg_out = f"{user_name}: {message}".encode()
        client.send(msg_out)
            
    def send_msg_to_all_connections(self, msg):
        user_name = msg["user_name"]
        message = msg["message"]
        print(message)
        msg_out = f"{user_name}: {message}".encode()
        
        for client in self.connections:
            client.send(msg_out)