class ServerSidePlayer:
    def __init__(self, rc, ps, channel, id):
        print("Making server side player", id)
        self.ps = ps
        self.rc = rc
        self.channel = channel
        self.id = id

    def play(self, board):
        self.rc.publish(self.channel, "a" + self.id + str(board.get_seed()))
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
