## CHANGES FOR SMALLER PADDLES. what if it is full screen, will that even work if the velocity maxes out?

# Import the pygame library and initialise the game engine
import pygame
import os
from time import time, sleep  #time resolution is pretty high, not sure how high though

from paddle import Paddle
from ball import Ball
from data_tracker import dataTracker #additional item/function added to track all relevant information during game.
from game_tracker import GameTracker

# Setting up globals
joys = [] # joystick tracker
FPS = 60 # FPS for the game
#SIZE = (1050, 750) #width, height - Screensize
SIZE = (1050, 750) #width, height - Screensize
BLACK = (0,0,0)
WHITE = (255,255,255)
screen = None # pygame screen
paddleA = None # Left Paddle
paddleB = None # Right Paddle
ball = None # the ball

# updated to show the change in range for a smaller paddle** 
def adjustJoystick(y, range=675): # how far paddle can move, math will need to change if paddle shrinks (e.g. smaller paddle range= 700)
    y = y * (range/2) + (range/2) # translates (-1,1) range to (0,675) pixel location
    return y

#opens game in center of screen consistently
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# Open a new window
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")

#paddleA = Paddle(WHITE, 15, 150) # color, width, height
paddleA = Paddle(WHITE, 15, 75) # color, width, height
paddleA.rect.x = 0 #starting position relative to screen size, x
paddleA.rect.y = 350 #starting position relative to size of screen, starting at y/2 more or less, y

#paddleB = Paddle(WHITE, 15, 150)
paddleB = Paddle(WHITE, 15, 75)
paddleB.rect.x = 1035
paddleB.rect.y = 350

ball = Ball(WHITE,15,15) #color, width, height of ball in px
ball.rect.x = 375 # starting location x
ball.rect.y = 525 

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
paused = False

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

#Initialize player scores
scoreA = 0
scoreB = 0

# Initialize data tracker
tracker = dataTracker(time())
game_tracker = GameTracker(time()) #does this belong here?


# Initialize the game
joys = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joys = list(filter(lambda j: 'paddle' in j.get_name().lower(), joys))
for j in joys:
    j.init()

pygame.event.pump()
screen.fill(BLACK)
myfont = pygame.font.SysFont(pygame.font.get_default_font(),int(SIZE[1]/10.))
text = myfont.render("Press both paddle buttons to start", True, WHITE) # players can initiate game together
textRect = text.get_rect()
textRect.center = (SIZE[0]//2,SIZE[1]//2)
screen.blit(text, textRect)
pygame.display.flip()
readyToStart = False
while not readyToStart:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if joys[0].get_button(0) is 1 and joys[1].get_button(0) is 1:
                readyToStart = True

# Display countdown screen
for i in range(5,0,-1):
    screen.fill(BLACK)
    text = myfont.render(str(i), True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SIZE[0]//2,SIZE[1]//2)
    screen.blit(text, textRect)
    pygame.display.flip()
    sleep(1)
screen.fill(BLACK)
text = myfont.render('GO!', True, WHITE)
textRect = text.get_rect()
textRect.center = (SIZE[0]//2,SIZE[1]//2)
screen.blit(text, textRect)
pygame.display.flip()
sleep(1)

endTime = time() + 185 # can update in seconds of time (just over 3 minutes)

# -------- Main Program Loop -----------
while carryOn:
    if time() > endTime:
        break
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_v: #Pressing the v Key will quit the game
                     carryOn=False
                elif event.key == pygame.K_b: # pressing b will pause the game
                    tracker.pause_toggle(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                    paused = not paused

    if paused: # allows us to pause the game using Y key.
        continue

    #Moving the paddles when the use uses "R/D" (player A) or "P/L" keys (player B) by 7.5 pixels.
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_r]:
    #     paddleA.moveUp(7.5) #originally 5
    #     # record button press/location movement by frame?
    # if keys[pygame.K_d]:
    #     paddleA.moveDown(7.5)
        
    # if keys[pygame.K_p]:
    #     paddleB.moveUp(7.5)
        
    # if keys[pygame.K_l]:
    #     paddleB.moveDown(7.5)
        
    # if keys[pygame.K_KP5]:
    #     ball.override()
    paddleA.rect.y = adjustJoystick(joys[0].get_axis(0))
    paddleB.rect.y = adjustJoystick(joys[1].get_axis(0))

    # --- Game logic should go here
    all_sprites_list.update()
    #print(ball.rect.x, ball.rect.y, paddleA.rect.y, paddleB.rect.y) # would this work here?

    # ----- does it go here?
    game_tracker.add_row(paddleA.rect.y, paddleB.rect.y, ball.x, ball.y, ball.angle, ball.velocity) 
    
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= 1035: # if ball hits Rside of screen
        if not pygame.sprite.collide_mask(ball, paddleB): #and also is not hitting the paddle
            scoreA += 1
            ball.rect.x = 1035
            ball.collideVertical()
            ball.resetSpeed()
            tracker.wall_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
    if ball.rect.x <= 5: # Lside of screen
        if not pygame.sprite.collide_mask(ball, paddleA):
            scoreB += 1
            ball.rect.x = 5
            ball.collideVertical()
            ball.resetSpeed()
            tracker.wall_left(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
    if ball.rect.y >= 735: # if the boundary of the screen is hit -- the bottom of the screen
        ball.rect.y = 735
        ball.collideHorizontal()
        # ball.speedUpCondition() # place here to include in bounce count
        # tracker.wall_top(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
        tracker.wall_bottom(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
    if ball.rect.y <= 0: #top of screen is hit
        ball.rect.y = 0
        ball.collideHorizontal()
        # ball.speedUpCondition() # place here to include in bounce count
        #tracker.wall_bottom(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
        tracker.wall_top(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)

        
     # ----- record the continuous game data into a different csv   
    # game_tracker.add_row(paddleA.rect.y, paddleB.rect.y, (ball.x, ball.y), ball.angle, ball.velocity)     
        
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA):
        ball.speedUpCondition()  # detect collisions for counter
        collision_percentile = ball.bounce(paddleA)
        ball.rect.x = 18  # keep from getting stuck on the paddle
        # ball.collision_percentile(paddleA)
        tracker.paddle_left(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, collision_percentile)
    if pygame.sprite.collide_mask(ball, paddleB):
        ball.speedUpCondition()  # detecting collisions for counter
        collision_percentile = ball.bounce(paddleB)
        ball.rect.x = 1017  # prevent sticking to paddleB
        # ball.collision_percentile(paddleB)
        tracker.paddle_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, collision_percentile) #or 


    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [530, 0], [530, 750], 15) #changing from  [349, 0], [349, 500], 5

    #Now let's draw all the sprites in one go. (For now we only have 3 sprites!)
    all_sprites_list.draw(screen)

    #Display scores: COMPETITIVE
    font = pygame.font.Font(None, 87)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (263,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (788,10))

    #COOPERATION scorekeeping will be one that adds them together. THERESA FIXED IT, SUCK IT TREBECK
    #font = pygame.font.Font(None, 74)
    #text = font.render(str(scoreA+scoreB), 1, WHITE)
    #screen.blit(text, (250,10))
    #text = font.render(str(scoreA+scoreB), 1, WHITE)
    #screen.blit(text, (420,10))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(FPS)

#Once we have exited the main program loop we can stop the game engine:
tracker.finalize()
#game_tracker.finalize()
pygame.quit()



