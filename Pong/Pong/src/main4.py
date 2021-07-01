## CHANGES FOR SMALLER PADDLES. what if it is full screen, will that even work if the velocity maxes out?
# Aidan: Possible improvements
# Resizable window
# wait for joystick

# Import the pygame library and initialise the game engine
import pygame
import os
from time import time, sleep  #time resolution is pretty high, not sure how high though

from paddle import Paddle
from ball import Ball
from data_tracker import dataTracker #additional item/function added to track all relevant information during game.
from game_tracker import GameTracker

from config import *

# Setting up globals
joys = [] # joystick tracker
screen = None # pygame screen
paddleA = None # Left Paddle
paddleB = None # Right Paddle
ball = None # the ball

#opens game in center of screen consistently # this line stays in main
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.event.pump()

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -- Initialize joystick inputs
joys = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joys = list(filter(lambda j: 'paddle' in j.get_name().lower(), joys))
for j in joys:
    j.init()

# Open a new window
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")

nextPage = True # Indicates to move onto the next page. Turns false if Pygame.QUIT is called

# -- "Tap buttons to play" start page
myfont = pygame.font.SysFont(pygame.font.get_default_font(),int(SIZE[1]/10.))
screen.fill(BLACK)
text = myfont.render("Press both paddle buttons to start", True, WHITE) # players can initiate game together
textrect = text.get_rect()
textrect.center = (SIZE[0]//2,SIZE[1]//2)
screen.blit(text, textrect)
pygame.display.flip()
startPage = True
while startPage and nextPage:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            nextPage = False
        if event.type == pygame.JOYBUTTONDOWN:
            if joys[0].get_button(0) is 1 and joys[1].get_button(0) is 1:
                startPage = False
        if event.type == pygame.KEYDOWN: # -- Alternatively, if using keyboard, press "A" and "L" to begin
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a] and pressed[pygame.K_l]:
                startPage = False

# -- Countdown page
countPage = nextPage
tick = 0
while countPage and nextPage:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
              nextPage = False
    screen.fill(BLACK)
    if tick >= (COUNTFROM + 1) * FPS:
        countPage = False
        break
    elif tick >= COUNTFROM * FPS:
        text = myfont.render('Go!', True, WHITE)
    else:
        num = COUNTFROM - tick//FPS
        text = myfont.render(str(num), True, WHITE)

    textrect = text.get_rect()
    textrect.center = (SIZE[0]//2,SIZE[1]//2)
    screen.blit(text, textrect)
    pygame.display.flip()
    tick = tick + 1
    clock.tick(FPS)

paddleA = Paddle(WHITE, PADW, PADH) # color, width, height
paddleA.rect.x = 0 #starting position relative to screen size, x
paddleA.rect.centery = SCREENH // 2
# Aidan: This line ^ doesn't do anything when using joysticks because the paddles will go to joystick position
# Aidan: Still important for keyboard controls

paddleB = Paddle(WHITE, PADW, PADH)
paddleB.rect.x = SCREENW - PADW
# paddleB.rect.y = 350
paddleB.rect.centery = SCREENH // 2

ball = Ball(WHITE, BALLW, BALLH)
ball.returnToCenter(SIZE)

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
paused = False

#Initialize player scores
scoreA = 0
scoreB = 0

# -- Initialize data tracker
tracker = dataTracker(time())
game_tracker = GameTracker(time())
endTime = time() + MAXTIME # can update in seconds of time (just over 3 minutes)

# -------- Main Game Loop -----------
scoreEvent = True
scorePause = False
servePause = True
leftServe = True
tick = 0
round = 0
winByTwo = False

while carryOn and nextPage:
    # if time() > endTime:
        # break
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              nextPage = False 
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_v: #Pressing the v Key will quit the game
                     carryOn=False
                elif event.key == pygame.K_b: # pressing b will pause the game
                    tracker.pause_toggle(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                    paused = not paused

    if paused: # allows us to pause the game using Y key.
        continue
    if scoreEvent:
        if scorePause: # pauses the screen immediately after the serve
            tick = tick + 1
            if tick >= FPS * PAUSELENGTH:
                tick = 0
                scorePause = False
                servePause = True
                ball.returnToCenter(SIZE)
            clock.tick(FPS)
            continue
    
        if round >= 5: # alternates who serves every 5 rounds
            leftServe = not leftServe
            round = 0

        if (scoreA >= WINSCORE or scoreB >= WINSCORE):
            if abs(scoreA-scoreB) < 2:   # win by 2 condition
                winByTwo = True
            else:
                carryOn = False
    
        if servePause:
            ball.velocity = 0
            tick = tick + 1
            if tick >= FPS * PAUSELENGTH:
                ball.resetSpeed()
                ball.serve(leftServe)
                tick = 0
                # serve event to csv? --------------- Aidan to implement
                scoreEvent = servePause = False
                winByTwo = False

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
    paddleA.adjustJoystick(joys[0].get_axis(0), SCREENH)
    paddleB.adjustJoystick(joys[1].get_axis(0), SCREENH)

    # --- Game logic should go here
    all_sprites_list.update()
    #print(ball.rect.x, ball.rect.y, paddleA.rect.y, paddleB.rect.y) # would this work here?

    # ----- does it go here?
    game_tracker.add_row(paddleA.rect.y, paddleB.rect.y, ball.x, ball.y, ball.angle, ball.velocity) 
    
    
    #Check if the ball is bouncing against any of the 4 walls:
    #if ball.rect.x >= 1035: # if ball hits Rside of screen
    if ball.rect.x >= SCREENW-BALLW:
        if not pygame.sprite.collide_mask(ball, paddleB): #and also is not hitting the paddle
            scoreEvent = scorePause = True
            scoreA += 1
            round += 1
            #ball.rect.x = 1035
            ball.rect.x = SCREENW-BALLW
            ball.collideVertical()
            tracker.wall_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
    if ball.rect.x <= 0: # Lside of screen
        if not pygame.sprite.collide_mask(ball, paddleA):
            scoreEvent = scorePause = True
            scoreB += 1
            round += 1
            ball.rect.x = 0
            ball.collideVertical()
            tracker.wall_left(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
    #if ball.rect.y >= 735: # if the boundary of the screen is hit -- the bottom of the screen
    if ball.rect.y >= SCREENH-BALLH:
        #ball.rect.y = 735
        ball.rect.y = SCREENH-BALLH
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
        #ball.rect.x = 18  # keep from getting stuck on the paddle
        ball.rect.x = PADW + 3
        # ball.collision_percentile(paddleA)
        tracker.paddle_left(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, collision_percentile)
    if pygame.sprite.collide_mask(ball, paddleB):
        ball.speedUpCondition()  # detecting collisions for counter
        collision_percentile = ball.bounce(paddleB)
        # ball.rect.x = 1017  # prevent sticking to paddleB
        ball.rect.x = SCREENW - PADW - BALLW - 3
        # ball.collision_percentile(paddleB)
        tracker.paddle_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, collision_percentile) #or 


    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(BLACK)
    #Draw the net
    #pygame.draw.line(screen, (150, 150, 150), [525, 0], [525, 750], 13) #changing from  [349, 0], [349, 500], 5
    pygame.draw.line(screen, (150, 150, 150), [SCREENW//2, 0], [SCREENW//2, SCREENH], 13)

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

    # -- Display "win by two" message
    if winByTwo: 
        text = font.render("Win by 2!", 1, WHITE)
        screen.blit(text, ((SCREENW - text.get_width()) // 2, SCREENH // 4) )

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(FPS)

# -- finalize CSV readings
tracker.finalize()
#game_tracker.finalize()

# -- Display winner screen
displayPage = True
if nextPage:
    winnerTxt = ""
    if scoreA > scoreB:
        winnerTxt = "Left wins!"
    elif scoreB > scoreA:
        winnerTxt = "Right wins!"
    else:
        winnerTxt = "Tie game!"
while displayPage and nextPage:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            nextPage = False
        elif event.type==pygame.KEYDOWN:
            displayPage = False
        elif event.type == pygame.JOYBUTTONDOWN:
            displayPage = False
    screen.fill(BLACK)
    font = pygame.font.Font(None, 120)
    text = font.render(winnerTxt, 1, WHITE)
    screen.blit(text, ((SCREENW - text.get_width()) // 2, SCREENH // 3) )
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (SCREENW//3 - text.get_width()//2, 2 * SCREENH//3))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (2 * SCREENW//3 - text.get_width()//2, 2 * SCREENH//3))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()



