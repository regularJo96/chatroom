import threading
import os
from Client import Client
from Server import Server
import random

#meant for testing without having to open 2 different programs all the time. Official use will be opening a client
# program each time somebody wants to connect. Or to add an "add client connection" function to this file (main.py). Most
# likely will go the way of the former.

## TODO need to setup waiting condition to not accept incoming messages until ack from the last sent from most recent client?

## TODO create User class to store user information. Use User class to create clients 1 per user.
def main():
    if __name__ == "__main__":
        server = Server()
        server.start()
        # # client = Client(1, "JoJo Onion")
        # # client_2 = Client(2, "Lo Dog")

        # server_p = threading.Thread(target=server.handle)
        # # client_p = threading.Thread(target=client.handle)
        # # client_p2 = threading.Thread(target=client_2.handle)

        # server_p.start()
        # # client_p.start()
        # # client_p2.start()
    
        # # client_p.join()
        # # client_p2.join()
        # server_p.join()

main()

input()