import pygame
from random import randint, choice
from math import sin, cos, radians, atan2, degrees, tan
from src.config import VELOCITYMIN, VELOCITYMAX, BLACK, SPEEDUPCTR, SERVETYPE, ServeType, SCREENW, SCREENH, BOUNDRADIUS

#SPEEDUPCTR = 4  # starting counter; number of paddle hits or collisions before speed increases

BOUNCE_RANGE = 120  # 120 degree range. 60 degrees up, or 60 degrees down

#POSSIBLE_STARTING_ANGLES = [0,  45, 315, 135, 180, 225]
#POSSIBLE_STARTING_ANGLES = [0]


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height, paddleA = None, paddleB = None):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        # arbitrary background color that will not be displayed
        # Cannot be Black because it messes with the ShadowBall
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = VELOCITYMIN  # distance it can move per frame, in pixels
        self.max_vel = VELOCITYMAX
        self.angle = 0 #self.startAngle()  # current traveling angle
        self.speedUpCtr = SPEEDUPCTR  # number of paddle hits or collisions before speed increases the first time.

        self.xVector = 0
        self.yVector = 0

        self._original_velocity = self.velocity
        self._original_angle = self.angle

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        
        self._overrideFlag = False

        # Keeps track of who's serving. 1 is left. 0 is right.
        self.leftServe = randint(0,1)

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
        self.rect.centerx += self.xVector
        self.rect.centery += self.yVector

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
        if self.speedUpCtr == 0:
            # Adjust Speed!
            # number of paddle hits or collisions before speed increases the next time
            self.speedUpCtr = SPEEDUPCTR  # resets counter back to 4
            if self.velocity <= self.max_vel: #tried to establish a cap speed for purposes of cooperation trials. will max out at 16 in reality because velocity @ 12 + randint(2) = 14. ##CHANGED FROM 13 ON 5/5/21 FOR PILOT GAMES. 
                self.velocity += randint(1, 2) #increase if the ball is slow enough. was originally (1,3) #XXXXX
            #else: 
            #    self.velocity += 0 # otherwise cap it out at a max speed.
        self.updateDirection() 
        return

    def collideHorizontal(self):
        """
        the ball has collided with one of the horizontal running walls (top or bottom)
        adjust ball angle/speed accordingly.
        """
        self.angle = (360 - self.angle) % 360
        self.updateDirection()
        return

    def collideVertical(self):
        """
        the ball has collided with one of the vertical running walls (left or right)
        adjust ball angle/speed accordingly.
        """
        self.angle = (180 - self.angle) % 360
        self.updateDirection()
        return

    def resetSpeed(self):
        """
        called by main - alters balls speed back to original
        """
        self.velocity = self._original_velocity
        self.updateDirection()
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
        
        if paddle.rect.x == 0:
            # collided with paddle A
            self.angle = (BOUNCE_RANGE * collision_percentile - BOUNCE_RANGE/2 + randomness) % 360   # --> wrong command? 
        else:
            # collided with paddle B
            self.angle = (BOUNCE_RANGE * (1-collision_percentile) + (180 - BOUNCE_RANGE/2) + randomness) % 360 # += randint(-1,1)
        self.updateDirection()
        return collision_percentile

    def updateDirection(self):
        self.xVector = ( cos(radians(self.angle)) * self.velocity + 0.5 ) // 1
        self.yVector = ( sin(radians(self.angle)) * self.velocity + 0.5 ) // 1

    #def startAngle(self):
    #    return choice(POSSIBLE_STARTING_ANGLES)

    def serveToggle(self):
        self.leftServe = not self.leftServe

    ## Old version of method to return ball to the exact center of the screen    
    #def returnToCenter(self, sizeTuple):
    #    width, height = sizeTuple
    #    self.rect.centerx = width // 2 # starting location x
    #    self.rect.centery = height // 2

    def returnToCenter(self, sizeTuple):
        width, height = sizeTuple
        if self.leftServe:
            self.rect.centerx = 40
        else:
            self.rect.centerx = width - 40
        self.rect.centery = height // 2
        self.velocity = 0
        self.updateDirection()

    ## -- Old serve function. Sets the angle of the ball to inital serve position. Called by main. 
    #def serve(self):
    #    if self.leftServe:
    #        self.angle = choice(POSSIBLE_STARTING_ANGLES[0:3])
    #    else:
    #        self.angle = choice(POSSIBLE_STARTING_ANGLES[3:])
    #def serve(self, paddle):
    #    self.resetSpeed()
    #    percent = paddle.getservePercent()
    #    if self.leftServe: 
    #        self.angle = -(paddle.getservePercent() - 0.5) * BOUNCE_RANGE
    #    else:
    #        self.angle = 180 + (paddle.getservePercent() - 0.5) * BOUNCE_RANGE
    #    self.updateDirection()
    def serve(self, paddle):
        if SERVETYPE == ServeType.STRAIGHT:
            self.serveStraight(paddle)
        elif SERVETYPE == ServeType.TOWARDCENTER:
            self.serveTowardCenter(paddle)
        elif SERVETYPE == ServeType.WITHINBOUND:
            self.serveWithinBound(paddle)
        elif SERVETYPE == ServeType.TWOSTEP:
            self.serveTwoStep(paddle)

    def serveStraight(self, paddle):
        self.resetSpeed()
        if self.leftServe:
            self.angle = 0
        else:
            self.angle = 180
        self.updateDirection()

    def serveTowardCenter(self, paddle):
        self.resetSpeed()
        xdiff = SCREENW/2 - self.rect.centerx
        ydiff = SCREENH/2 - self.rect.centery
        self.angle = degrees(atan2(ydiff, xdiff)) % 360
        self.updateDirection()

    def serveWithinBound(self, paddle):
        self.resetSpeed()
        maxSlope = tan(radians(BOUNCE_RANGE/2))
        ydiff = SCREENH/2 - paddle.rect.centery
        slope = ydiff/BOUNDRADIUS * maxSlope
        if self.leftServe:
            self.angle = degrees(atan2(slope, 1)) % 360
        else:
            self.angle = degrees(atan2(slope, -1)) % 360
        self.updateDirection()

    def serveTwoStep(self, paddle):
        self.resetSpeed()
        maxSlope = tan(radians(BOUNCE_RANGE/2))
        ydiff = self.rect.centery - paddle.rect.centery
        xdiff = self.rect.centerx - paddle.rect.centerx
        slope = ydiff/xdiff
        if slope > maxSlope:
            slope = maxSlope
        elif slope < -maxSlope:
            slope = -maxSlope
        if self.leftServe:
            self.angle = degrees(atan2(slope, 1)) % 360
        else:
            self.angle = degrees(atan2(-slope, -1)) % 360
        self.updateDirection()

    def followPaddle(self, paddleA, paddleB):
        if self.leftServe:
            self.rect.centery = paddleA.rect.centery
        else: 
            self.rect.centery = paddleB.rect.centery
