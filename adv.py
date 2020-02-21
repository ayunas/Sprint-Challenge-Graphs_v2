from room import Room
from player import Player
from world import World
from maze import Maze
from test_traversal import test_traversal
import random,json,time
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"



# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()


player = Player(world.starting_room)
maze = Maze()

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
            maze.backtrack(trail,player)
            continue
        else:
            player.travel(new_way)
            maze.path.append(new_way)
            print(f'player traveled {new_way} to {player.current_room.id}')
            next_id,next_exits = player.current_room.id, player.current_room.get_exits()
            maze.load_room(next_id, next_exits)
            rz = maze.update_rooms(room_id,new_way,next_id)
    # print(maze.path)
    return maze

traversal_path = explore_world(player,world)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []

# TRAVERSAL TEST

if __name__ == '__main__':
    maze = explore_world(player,world)
    traversal_path = maze.path
    test_traversal(traversal_path,world,player,room_graph)

    # maze_json = json.dumps(maze.rooms, indent=2)
    # print(type(maze.rooms))
    import re
    fn = re.sub('maps/','',map_file)
    filename = re.sub('.txt','',fn)
    print(filename)

    with open(f'{filename}.json', 'w') as json_file:
        json.dump(maze.rooms, json_file, sort_keys=True, indent=3)



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
