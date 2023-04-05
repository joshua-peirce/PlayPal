"""
Server class
"""

import redis
import game

redis_host = 'localhost'
redis_port = 6379

user_ids = [1, 2, 3, 4]
pwds = [5, 6, 7, 8]

redis_client = redis.Redis(host=redis_host, port=redis_port)

# ! Rachel: started making Server class, feel free to make architectural changes


class Server:

    def __init__(self, host, port):
        self.host = redis_host
        self.port = redis_port
        self._start_server()
        self.queue = []
        # ! Rachel: do we store locally as well? or grab from Redis every time
        #self.player_id_list = []
        self.next_player_id = 1
        self.next_game_id = 1

    def _start_server(self):
        pass

    def register_player(self):
        # should add player to queue
        # increment next player id
        pass

    def match_players(self):
        # based on queue, matches players by first come, first serve

        # if the queue is ever, people are matched with person next to them
        # each pair is assigned to the next game ID, need to add to game ID as many as there were pairs
        if self.queue % 2 == 0:
            pass
        else:
            # ignore the last person
            pass






class ServerSidePlayer:
    def __init__(self, rc, ps, id):
        print("Making server side player", id)
        self.ps=ps
        self.rc=rc
        self.id=id

    def play(self, board):
        self.rc.publish("game", "a" + self.id + str(board.get_seed()))
        while True:
            for message in self.ps.listen():
                if message["type"] == "message":
                    data = str(message["data"])[2:-1]
                    if data[0] == "b":
                        move = int(data[1:])
                        if move in board.get_empty_cells_integer():
                            return board.convert_integer_to_tuple(move)
                    
    def win(self, hist):
        pass

    def lose(self, hist):
        pass

def start_server():
    ps = redis_client.pubsub()
    ps.subscribe("game")
    ids = []
    redis_client.lpush("player_ids", 0)
    while True:
        for message in ps.listen():
            if message["type"] == "message":
                data = str(message["data"])[2:-1]
                if data[0] == "j":
                    ids.append(int(data[data.find(":")+1]))
                    if len(ids) == 2:
                        p1 = ServerSidePlayer(redis_client, ps, "X")
                        p2 = ServerSidePlayer(redis_client, ps, "O")
                        g = game.Game(p1, p2)
                        print("game played", g.play())
                        redis_client.publish("game", "eeeee")
                elif data[0] == "e":
                    print("Ending server")
                    return

if __name__ == "__main__":
    start_server()
                    
