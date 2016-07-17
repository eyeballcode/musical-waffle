class Chatbot:
    def __init__(self, client, roomid):
        self.client = client
        self.room = client.get_room(roomid)
