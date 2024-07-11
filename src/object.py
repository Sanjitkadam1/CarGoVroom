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
        self.turn4 = np.array(["White", "White", "White"], ["White", "White", "White"]) # This is for round trip values
        self.track = np.array([self.turn0, self.turn1, self.turn2, self.turn3, self.turn4])

    def add(obj):
        track[obj.turn][obj.row][obj.col] = obj.color


        
    

