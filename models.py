class Light:
    def __init__(self, light_color, timer):
        self.light_color = light_color
        self.timer = timer


class Crossing:
    def __init__(self, crossingID, laneID, time, avg_speed, avg_acc, textSpeed, textAcc, density, accident):
        self.crossingID = crossingID
        self.laneID = laneID
        self.time = time
        self.avg_speed = avg_speed
        self.avg_acc = avg_acc
        self.textSpeed = textSpeed
        self.textAcc = textAcc
        self.density = density
        self.accident = accident