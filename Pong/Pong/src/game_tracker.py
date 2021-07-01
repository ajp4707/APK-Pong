import csv
import time

class GameTracker():
    def __init__(self, t):
        self.f = open("gamedata_" + time.strftime("%Y%m%d-%H%M%S") + '.csv', 'w')
        field_names = ['time', 'paddleA_position', 'paddleB_position', 'ball_xposition', 'ball_yposition', \
            'ball_angle', 'ball_velocity', 'sync_count']
        self.writer = csv.DictWriter(self.f, fieldnames=field_names, lineterminator='\n')
        self.writer.writeheader()
        self.start_time = t

    def __del__(self):
        self.f.close()

    def add_row(self, paddleA_position, paddleB_position, ball_xposition, ball_yposition, ball_angle, ball_velocity, sync_count): 
        row = {
            'time': (time.time() - self.start_time),
            'paddleA_position': paddleA_position,
            'paddleB_position': paddleB_position,
            'ball_xposition': ball_xposition,
            'ball_yposition': ball_yposition,
            'ball_angle': ball_angle,
            'ball_velocity': ball_velocity,
            'sync_count' : sync_count,
        }
        self.writer.writerow(row)
