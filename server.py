"""
Server class
"""

import redis
import game
from ServerSidePlayer import ServerSidePlayer

redis_host = 'localhost'
redis_port = 6379

user_ids = [1, 2, 3, 4]
pwds = [5, 6, 7, 8]

rc = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
ps = rc.pubsub()

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

    # def match_players(self):
    #     # based on queue, matches players by first come, first serve
    #
    #     # if the queue is ever, people are matched with person next to them
    #     # each pair is assigned to the next game ID, need to add to game ID as many as there were pairs
    #     if self.queue % 2 == 0:
    #         pass
    #     else:
    #         # ignore the last person
    #         pass

def start_server():

    # open a channel for the next player to join
    new_id = rc.llen('player_ids') + 1
    ps.subscribe(f'player{new_id}')

    ids = []
    while True:
        for message in ps.listen():

            # this is casting the data to string
            # turn this into a internal function or method to make it cleaner
            if message["type"] == "message":
                data = str(message["data"])[2:-1]
                # j = player joined
                # a = request for a move (contains prev move)
                # b = response of the move
                # c = lose
                # d = win
                # e = over
                if data[0] == "j":
                    channel = message['channel']

                    # add player to queue
                    rc.lpush('queue', channel)

                    ids.append(int(data[data.find(":")+1]))
                    if len(ids) == 2:
                        # subscribe to all the player channels

                        p1 = ServerSidePlayer(rc, ps, "X")
                        p2 = ServerSidePlayer(rc, ps, "O")
                        g = game.Game(p1, p2)
                        print("game played", g.play())
                        # telling everyone that the game is over
                        rc.publish("game", "eeeee")
                elif data[0] == "e":
                    print("Ending server")
                    return


def matchmake():
    queue = rc.lrange('queue', 0, -1)
    channel1 = queue[0]
    channel2 = queue[1]

    p1 = ServerSidePlayer(rc, ps, channel1, "X")
    p2 = ServerSidePlayer(rc, ps, channel2, "O")
    g = game.Game(p1, p2)
    print("game played", g.play())
    # telling everyone that the game is over
    
    
if __name__ == "__main__":
    start_server()
