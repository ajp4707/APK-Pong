import csv
import time
from datetime import datetime   # using only for csv title

class GameTracker():
    def __init__(self, t):
        start_dt = datetime.now()
        file_start_str = start_dt.strftime("%Y-%m-%d-%H-%M-%S")
        start_str = start_dt.strftime("%Y%m%d%H%M%S%f")
        self.f = open("gamedata_" + file_start_str + '.csv', 'w')
        
        self.writer1 = csv.writer(self.f, lineterminator='\n')
        self.writer1.writerow([start_str])
        
        field_names = ['time', 'paddleA_position', 'paddleB_position', 'ball_xposition', 'ball_yposition', \
            'ball_angle', 'ball_velocity', 'sync_count']
        self.writer = csv.DictWriter(self.f, fieldnames=field_names, lineterminator='\n')
        self.writer.writeheader()
        self.start_time = t

    def __del__(self):
        end_dt = datetime.now()
        end_str = end_dt.strftime("%Y%m%d%H%M%S%f")
        self.writer1.writerow([end_str])
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
