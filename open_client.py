import random
from Client import Client
import sys

def connect():
    client = Client(0)
    client.handle()
    if(client.close):
        del client
        sys.exit(0)

connect()