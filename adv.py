from room import Room
from player import Player
from world import World
from maze import Maze

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

maze = Maze()
player = Player(world.starting_room)

def explore_world(player,world):

    world_length = len(world.rooms.items())
    print('world contains', world_length,'rooms')

    while maze.size < world_length:
        print('current room', player.current_room.id)
        room_id,exits = player.current_room.id,player.current_room.get_exits()
        maze.load_room(room_id,exits)
        new_way = maze.unexplore(room_id,player)
        if not new_way:
            print('reached a dead end')
            print('dead end room: ', room_id, maze.rooms[room_id])
            trail = maze.bfs(room_id)
            if trail == None:  #needed if entire world explored.  then bfs not returning any path to a '?'
                break
            print('backtrack trail', trail)
            maze.backtrack(trail,player)
            continue

        player.travel(new_way)
        print(f'player traveled {new_way} to {player.current_room.id}')
        next_id,next_exits = player.current_room.id, player.current_room.get_exits()
        maze.load_room(next_id, next_exits)
        rz = maze.update_rooms(room_id,new_way,next_id)
    print(maze)

explore_world(player,world)











# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
