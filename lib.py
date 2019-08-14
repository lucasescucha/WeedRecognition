class Utils:    
    def openBounds(file_name):
        from collections import defaultdict
        frames_bounds = defaultdict(list) 
        with open(file_name, 'r') as f:
            bound_n = 0
            for line in f.readlines()[1:]:
                values = [int(x) for x in line.split(',')]
                frames_bounds[values[0]].append(values[1:])
                bound_n = values[-1]
        return frames_bounds, (bound_n + 1)

class RingBuffer:
    def __init__(self, size):
        self.data = [None for i in range(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data  
    
class RACapWrapper:
    def __init__(self, cap, mlenght):
        self.cap = cap
        self.mlenght = mlenght
        self.frameHistory = RingBuffer(mlenght)
        self.actualFrame = -1    
    
    def readAt(self, frameN):       
        if frameN == self.actualFrame:
            return self.frameHistory.get()[-1].copy(), frameN
        elif frameN > self.actualFrame:
            if self.cap.isOpened():
                _, frame = self.cap.read()
                self.frameHistory.append(frame)
                self.actualFrame += 1
                
                return self.readAt(frameN)
            else:
                raise Exception("Cap is close")
        elif frameN < self.actualFrame:
            if (self.actualFrame - frameN) >= self.mlenght:
                frameN = self.actualFrame - self.mlenght + 1
            
            return self.frameHistory.data[frameN - self.actualFrame - 1].copy(), frameN