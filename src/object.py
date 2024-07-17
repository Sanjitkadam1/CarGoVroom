import json
import numpy as np

class obj:
    def __init__(self, turn, num, color):
        self.turn = turn
        if (num%2==0):
            self.row = 2
            self.col = num/2
        else:
            self.row = 1
            self.col = num+1/2
        self.color = color


class track:
    def __init__(self):
        self.turn0 = np.array(["White", "White", "White"], ["White", "White", "White"])
        self.turn1 = np.array(["White", "White", "White"], ["White", "White", "White"])
        self.turn2 = np.array(["White", "White", "White"], ["White", "White", "White"])
        self.turn3 = np.array(["White", "White", "White"], ["White", "White", "White"])
        self.track = np.array([self.turn0, self.turn1, self.turn2, self.turn3, self.turn4])

    def add(obj):
        track[obj.turn][obj.row][obj.col] = obj.color

    def getObjs(turn, set):
        return track[turn][0][(set+1/2)-1], track[turn][1][(set+1/2)-1]
    
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def plot():
        cordinatesx = [1000, 1500, 2000, 1000, 1500, 2000, 2600, 2600, 2600, 2400, 2400, 2400, 2000, 1500, 1000, 2000, 1500, 1000, 400, 400, 400, 600, 600, 600]
        cordinatesy = [2600, 2600, 2600, 2400, 2400, 2400, 2000, 1500, 1000, 2000, 1500, 1000, 600, 600, 600, 400, 400, 400, 1000, 1500, 2000, 1000, 1500, 2000] 

        greenX = []
        greenY = []
        redX = []
        redY = []

        for i in range(4):
            for j in range(2):
                for k in range(3):
                    if track[i][j][k] == "green":
                        greenX = cordinatesx[(i*6) + (j*3) + k]
                        greenY = cordinatesy[(i*6) + (j*3) + k]
                    elif track[i][j][k] == "red":
                        redX = cordinatesx[(i*6) + (j*3) + k]
                        redY = cordinatesy[(i*6) + (j*3) + k]

        
        return greenX, greenY, redX, redY