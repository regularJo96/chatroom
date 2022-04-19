from Client import Client
import threading

def main():
    client = Client(0)

    while(client.close==False):
        receive = threading.Thread(target=client.receive_msg)
        inp = threading.Thread(target=client.get_input)
        receive.daemon = True
        inp.daemon = True
        receive.start()
        inp.start()
        receive.join()

    client.close_connection()
    
main()