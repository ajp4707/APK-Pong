import csv
import time

### needs to be updated to (maybe) include synch events
class dataTracker():
    def __init__(self, t):
        # (time, (impact_x, impact_y), ball.velocity, ball.angle) #these are the events, we need the meta-data related to the events. 
        self.ball_collision = {
            "paddle_left_impacts":[],
            "paddle_right_impacts":[],
            "wall_top_impacts":[],
            "wall_bottom_impacts":[],
            "wall_left_impacts":[],
            "wall_right_impacts":[],
            "pause_toggled":[],           
        } #curly braces are a dictionary, ds.

        self.start_time = t
        
    def _dict_to_csv(self, ds): # ds = dictionary string. This section renamed the events to the column name for below. 
        dtc = {
            "paddle_left_impacts":'paddleA_time',
            "paddle_right_impacts":'paddleB_time',
            "wall_top_impacts":'Top_time',
            "wall_bottom_impacts":'Bottom_time',
            "wall_left_impacts":'Left_time',
            "wall_right_impacts":'Right_time',
            "pause_toggled": 'Pause_time',
        }
        return dtc[ds]

    def _pad_rest(self):
        pad_len = len(max(self.ball_collision.values(), key=len))
        for k in self.ball_collision.keys():
            if len(self.ball_collision[k]) < pad_len:
                self.ball_collision[k].append(None)

### add in the percentile that it is hitting each time on the paddle -- add ,percentile_left, percentile_right to the end of each def and then update what is reported in the main files.

    def paddle_left(self, time, location, velocity, angle, paddle_left, paddle_right, collision_percentile): #pass parameter to the function, need to include what you want
        self.ball_collision["paddle_left_impacts"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, collision_percentile)) #event-centric data. adding ball meta-data.
        #? self.paddleA["paddle_left_loc"].append((time - self.start_time, location))
        self._pad_rest() # _pad_rest() helps avoid a lot of extra mathy bits.
    def paddle_right(self, time, location, velocity, angle, paddle_left, paddle_right, collision_percentile):
        self.ball_collision["paddle_right_impacts"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, collision_percentile))
        #add another line for paddle location? self.paddleB[]
        self._pad_rest()
    def wall_top(self, time, location, velocity, angle, paddle_left, paddle_right):
        self.ball_collision["wall_top_impacts"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, None))
        self._pad_rest()
    def wall_bottom(self, time, location, velocity, angle, paddle_left, paddle_right):
        self.ball_collision["wall_bottom_impacts"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, None))
        self._pad_rest()
    def wall_left(self, time, location, velocity, angle, paddle_left, paddle_right):
        self.ball_collision["wall_left_impacts"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, None))
        # paddleA position?
        self._pad_rest()
    def wall_right(self, time, location, velocity, angle, paddle_left, paddle_right):
        self.ball_collision["wall_right_impacts"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, None))
        self._pad_rest()
        #paddleB position?
    def pause_toggle(self, time, location, velocity, angle, paddle_left, paddle_right):
        self.ball_collision["pause_toggled"].append((time - self.start_time, location, velocity, angle, paddle_left, paddle_right, None))
        self._pad_rest()

    def finalize(self):
        # write out all data to .csv
        # aggregate .csv.
        #####################################################################################
        # event_timestamp_col1, event_col2, event_col3, ..., event_coln, impact_x, impact_y #
        #####################################################################################
        # with open('data.csv', 'a') as csvfile: #if data.csv exists in the folder, this will append data to the end of it.
        with open("pongdata_" + time.strftime("%Y%m%d-%H%M%S") + '.csv', 'w') as csvfile:
            field_names = ['paddleA_time', 'paddleB_time', 'Left_time', 'Right_time', 'Top_time', 'Bottom_time', 'Pause_time', 'impact_x', 'impact_y', 'ball_speed', 'ball_post_bounce_angle', 'paddle_left_y', 'paddle_right_y', 'collision_percentile'] #accounts for all variables, you need to update this list if you add more variables to measure, and ALSO need to update in main.
            writer = csv.DictWriter(csvfile, fieldnames=field_names) #write out/creates the csv file. 
            writer.writeheader()
            for i in range(len(self.ball_collision["paddle_left_impacts"])):
                row = {}
                for k in self.ball_collision.keys():
                    if self.ball_collision[k][i] != None:
                        print(self.ball_collision[k][i])
                        t , xy, v, a, l, r, p = self.ball_collision[k][i] # pulls meta data that has been stored to be put into csv.
                        impact_x, impact_y = xy
                        row[self._dict_to_csv(k)] = t #set up a row in the CSV 
                        row['impact_x'] = impact_x
                        row['impact_y'] = impact_y
                        row['ball_speed'] = v
                        row['ball_post_bounce_angle'] = a
                        row['paddle_left_y'] = l
                        row['paddle_right_y'] = r
                        row['collision_percentile'] = p
                writer.writerow(row) #writes one row to the CSV file. 
        return