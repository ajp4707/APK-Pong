import pygame
from random import randint, choice
from math import sin, cos, radians

BLACK = (0, 0, 0)
SPEEDUPCTR = 4  # starting counter; number of paddle hits or collisions before speed increases

BOUNCE_RANGE = 120  # 120 degree range. 60 degrees up, or 60 degrees down

POSSIBLE_STARTING_ANGLES = [0,  45, 315, 135, 180, 225]
#POSSIBLE_STARTING_ANGLES = [0]


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = 9  # distance it can move per frame, in pixels
        # self.max_vel = 16
        self.angle = self.startAngle()  # current traveling angle
        self.speedUpCtr = SPEEDUPCTR  # number of paddle hits or collisions before speed increases the first time.

        self._original_velocity = self.velocity
        self._original_angle = self.angle

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        
        self._overrideFlag = False

    @property
    def x(self):
        return self.rect.x #when you ask for ball.x, it will give you the rect.x

    @property
    def y(self):
        return self.rect.y

    def update(self):
        """
        Called once per frame - handles moving of self.rect's position
        """
        #self.rect.centerx += cos(radians(self.angle)) * self.velocity
        self.rect.centerx += ( cos(radians(self.angle)) * self.velocity + 0.5 ) // 1
        self.rect.centery += ( sin(radians(self.angle)) * self.velocity + 0.5 ) // 1

        return

    def speedUpCondition(self):
        """
        Check to see if we need to increase speed of the ball
        Called by main.py when some speedUp condition is met.
        Should work if condition is paddle collision, wall collision, points scored, etc.
        Doesn't matter - just adjusts velocity of the ball for the next self.update()
        """
        # return  # XXX: remove this line to add speed back
        self.speedUpCtr -= 1
        if self.speedUpCtr is 0:
            # Adjust Speed!
            # number of paddle hits or collisions before speed increases the next time
            self.speedUpCtr = SPEEDUPCTR  # resets counter back to 4
            if self.velocity <= 14: #tried to establish a cap speed for purposes of cooperation trials. will max out at 16 in reality because velocity @ 12 + randint(2) = 14. ##CHANGED FROM 13 ON 5/5/21 FOR PILOT GAMES. 
                self.velocity += randint(1, 2) #increase if the ball is slow enough. was originally (1,3) #XXXXX
            else: 
                self.velocity += 0 # otherwise cap it out at a max speed. 
        return

    def collideHorizontal(self):
        """
        the ball has collided with one of the horizontal running walls (top or bottom)
        adjust ball angle/speed accordingly.
        """
        self.angle = (360 - self.angle) % 360
        return

    def collideVertical(self):
        """
        the ball has collided with one of the vertical running walls (left or right)
        adjust ball angle/speed accordingly.
        """
        self.angle = (180 - self.angle) % 360
        ##add line for time delay where it freezes in location briefly. maybe this would be another equation entirely?
        ##change location based on command for serving
        return

    def resetSpeed(self):
        """
        called by main - alters balls speed back to original
        """
        self.velocity = self._original_velocity
        return
    
    def override(self):
        """
        Called by main - allows the instructor to override an infinite volley by injecting randomness on next bounce
        """
        self._overrideFlag = True
        return

    def bounce(self, paddle):
        """
        called by main when ball contacts a paddle. Passes contacted paddle along for contact location
        :param paddle: contacted paddle
        """
        collision_percentile = (((self.rect.y + self.height) - paddle.rect.y) / (paddle.height + self.height * 2)) # + randint(-1,1)  # maybe add randint?
        
        if self._overrideFlag:
            randomness = randint(-10,10)
            self._overrideFlag = False
        else:
            randomness = randint(-5,5)
        
        if paddle.rect.x is 0:
            # collided with paddle A
            self.angle = (BOUNCE_RANGE * collision_percentile - BOUNCE_RANGE/2 + randomness) % 360   # --> wrong command? 
        else:
            # collided with paddle B
            self.angle = (BOUNCE_RANGE * (1-collision_percentile) + (180 - BOUNCE_RANGE/2) + randomness) % 360 # += randint(-1,1)

        return collision_percentile

    def startAngle(self):
        return choice(POSSIBLE_STARTING_ANGLES)

    # -- Sets the angle of the ball to inital serve position. Called by main. 
    # @param leftServe boolean of if Left is serving (ball will go right)
    def serve(self, leftServe):
        if leftServe:
            self.angle = choice(POSSIBLE_STARTING_ANGLES[0:3])
        else:
            self.angle = choice(POSSIBLE_STARTING_ANGLES[3:])
    
    def returnToCenter(self, sizeTuple):
        width, height = sizeTuple
        self.rect.centerx = width // 2 # starting location x
        self.rect.centery = height // 2
