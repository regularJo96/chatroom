class Packet:
    uid = None
    user_name = None
    message = None
    header_size = 8

    def __init__(self,uid,user_name,message):
        self.uid = uid
        self.user_name = user_name
        message = message + " "*(self.header_size-len(message))
        self.message = message
    