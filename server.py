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
                    
