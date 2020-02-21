import json

class Maze:
    def __init__(self):
        self.rooms = {}
        self.path = []
    
    def load_room(self,room_id,exits=None):
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        for way in exits:
            self.rooms[room_id][way] = '?'


    def __repr__(self):
        return json.dumps(self.rooms)

