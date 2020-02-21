import json,random
from collections import deque

class Maze:
    def __init__(self):
        self.rooms = {}
        self.path = []
    
    def neighbors(self,room_id):
        neigh_ids = [r_id for (way,r_id) in self.rooms[room_id].items()]
        return neigh_ids

    def load_room(self,room_id,exits):
        if room_id in self.rooms:
            return self.rooms[room_id]
        
        self.rooms[room_id] = {}
        for way in exits:
            self.rooms[room_id][way] = '?'

    def unexplore(self,room_id,player):
        if room_id not in self.rooms:
            return None
        unexplored = {way : self.rooms[room_id][way] for way in self.rooms[room_id] if self.rooms[room_id][way] == '?'}
        print('unexplored rooms', unexplored)
        if not len(unexplored.items()):
            return None
        rand_way = random.choice([*unexplored.items()])
        print('rand_way', rand_way, 'for room: ', room_id)
        # rand_way = unexplored.popitem()  #randomly returns an key/val pair popped from the dictionary
        return rand_way[0]
    
    def backtrack(self,trail,player):
            print('reached a dead end, backtracking...')
            print('current room id', player.current_room.id)
            room_id = player.current_room.id
            print('trail in backtrack', trail)
            
            for step_id in trail[1:-1]:
                next_way = [way for way in self.rooms[room_id] if self.rooms[room_id][way] == step_id][0]
                player.travel(next_way)
                print(f'player backtracked from {room_id} to {step_id}')
                room_id = player.current_room.id
            print('room_id', room_id)
    
    def update_rooms(self,current_id,way,next_id):
        flipped = self.flip_way(way)
        self.rooms[next_id][flipped] = current_id
        self.rooms[current_id][way] = next_id
        return [self.rooms[current_id], self.rooms[next_id]]
    
    def flip_way(self,way):
        waze = {'n' : 's', 's': 'n', 'e' : 'w', 'w' : 'e'}
        return waze[way]
    
    def bfs(self,room_id):
        q = deque()
        q_enque = q.append
        q_deque = q.popleft
        print('room_id in bfs', room_id)

        visited = set()
        q_enque([room_id])
        
        while len(q) > 0:
            path = q_deque()
            r_id = path[-1]
            if r_id not in visited:
                if r_id == '?':
                    return path
                else:
                    visited.add(r_id)
                next_ids = self.neighbors(r_id)
                # print('next_ids', next_ids)
                for n_id in next_ids:
                    new_path = path.copy()
                    new_path.append(n_id)
                    q_enque(new_path)

    @property
    def size(self):
        return len(self.rooms.keys())


    def __repr__(self):
        return json.dumps(self.rooms)

