## CHANGES FOR SMALLER PADDLES. what if it is full screen, will that even work if the velocity maxes out?
# Aidan: Possible improvements
# Resizable window
# wait for joystick
# create serve event for data tracker. Create sync pulse variable

import pygame
import os, sys
from time import time, sleep  #time resolution is pretty high, not sure how high though

sys.path.append(".")

from src.paddle import PaddleLeft, PaddleRight
from src.ball import Ball
from src.data_tracker import dataTracker #additional item/function added to track all relevant information during game.
from src.game_tracker import GameTracker

from src.config import *

class MainWindow:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.initScreen()
        self.initPeripherals()
        self.startGame()
        pygame.quit()
        
    def initScreen(self):
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Pong")

    def initPeripherals(self):
        # initialize clock, font, and joysticks
        self.clock = pygame.time.Clock()
        self.joys = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joys = list(filter(lambda j: 'paddle' in j.get_name().lower(), self.joys))
        if len(self.joys) < 2:
            raise IndexError("IndexError. Please connect joysticks.")
        for j in self.joys:
            j.init()

    def startGame(self):
        self.nextPage = True
        self.startPage()
        if self.nextPage:
            self.countPage()
        if self.nextPage:
            self.gamePage()
        if self.nextPage:
            self.scorePage()

    def startPage(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(pygame.font.get_default_font(),int(SIZE[1]/10.))
        text = font.render("Press both paddle buttons to start", True, WHITE) # players can initiate game together
        textrect = text.get_rect()
        textrect.center = (SIZE[0]//2,SIZE[1]//2)
        self.screen.blit(text, textrect)
        pygame.display.flip()
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextPage = False
                    loop = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joys[0].get_button(0) is 1 and self.joys[1].get_button(0) is 1:
                        loop = False
                if event.type == pygame.KEYDOWN: # -- Alternatively, if using keyboard, press "A" and "L" to begin
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_a] and pressed[pygame.K_l]:
                        loop = False
    def countPage(self):
        font = pygame.font.SysFont(pygame.font.get_default_font(),int(SIZE[1]/10.))
        loop = True
        tick = 0
        while loop:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                      self.nextPage = False
                      loop = False
            self.screen.fill(BLACK)
            if tick >= (COUNTFROM + 1) * FPS:
                loop = False
                break
            elif tick >= COUNTFROM * FPS:
                text = font.render('Go!', True, WHITE)
            else:
                num = COUNTFROM - tick//FPS
                text = font.render(str(num), True, WHITE)

            textrect = text.get_rect()
            textrect.center = (SIZE[0]//2,SIZE[1]//2)
            self.screen.blit(text, textrect)
            pygame.display.flip()
            tick = tick + 1
            self.clock.tick(FPS)  
    def gamePage(self):
        self.scoreA = 0
        self.scoreB = 0

        tracker = dataTracker(time())
        game_tracker = GameTracker(time())
        endTime = time() + MAXTIME # can update in seconds of time (just over 3 minutes)
        
        # -- sync signal
        syncCount = 0

        # -- game objects
        paddleA = PaddleLeft(WHITE, PADW, PADH, SIZE)
        paddleB = PaddleRight(WHITE, PADW, PADH, SIZE)
        ball = Ball(WHITE, BALLW, BALLH)
        ball.returnToCenter(SIZE)

        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(paddleA)
        all_sprites_list.add(paddleB)
        all_sprites_list.add(ball)

        # -- Main game loop
        loop = True
        paused = False
        scoreEvent = True
        scorePause = False
        servePause = True
        leftServe = True
        tick = 0
        round = 0
        winByTwo = False
        while loop:
            if TIMELIMIT and time() > endTime:
                loop = False
            # --- Main event loop
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                      self.nextPage = False 
                      loop = False
                elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_v: # Pressing the v Key will quit the game
                             loop=False
                        elif event.key == pygame.K_b: # Pressing b will pause the game
                            tracker.pause_toggle(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                            paused = not paused
                        elif event.key == pygame.K_s: # Sync signal event will go here. For now, s
                            syncCount += 1
                            tracker.sync_pulse(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, syncCount)
            
            # update game time tracker, regardless of pauses
            game_tracker.add_row(paddleA.rect.y, paddleB.rect.y, ball.x, ball.y, ball.angle, ball.velocity, syncCount) 

            if paused: # allows us to pause the game using p key.
                self.clock.tick(FPS)
                continue
            if scoreEvent:
                if scorePause: # pauses the screen immediately after the serve
                    tick = tick + 1
                    if tick >= FPS * PAUSELENGTH:
                        tick = 0
                        scorePause = False
                        servePause = True
                        ball.returnToCenter(SIZE)
                    self.clock.tick(FPS)
                    continue
    
                if round >= SWITCHROUNDS: # alternates who serves every SWITCHROUNDS rounds
                    leftServe = not leftServe
                    round = 0

                if (self.scoreA >= WINSCORE or self.scoreB >= WINSCORE):
                    if abs(self.scoreA-self.scoreB) < 2:   # win by 2 condition
                        winByTwo = True
                    else:
                        loop = False
    
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
            keys = pygame.key.get_pressed()
            paddleA.adjustJoystick(self.joys[0].get_axis(0), SCREENH)
            paddleB.adjustJoystick(self.joys[1].get_axis(0), SCREENH)

            # --- Game logic
            all_sprites_list.update()
    
            #Check if the ball is bouncing against any of the 4 walls:
            #if ball.rect.x >= 1035: # if ball hits Rside of screen
            if ball.rect.x >= SCREENW-BALLW:
                if not pygame.sprite.collide_mask(ball, paddleB): #and also is not hitting the paddle
                    scoreEvent = scorePause = True
                    self.scoreA += 1
                    round += 1
                    ball.rect.x = SCREENW-BALLW
                    ball.collideVertical()
                    tracker.wall_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
            if ball.rect.x <= 0: # Lside of screen
                if not pygame.sprite.collide_mask(ball, paddleA):
                    scoreEvent = scorePause = True
                    self.scoreB += 1
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


            # --- Drawing 
            self.screen.fill(BLACK)
            #Draw the net
            pygame.draw.line(self.screen, GRAY, [SCREENW//2, 0], [SCREENW//2, SCREENH], 13)

            #Now let's draw all the sprites in one go. (For now we only have 3 sprites!)
            all_sprites_list.draw(self.screen)

            #Display scores: COMPETITIVE
            font = pygame.font.Font(None, 87)
            text = font.render(str(self.scoreA), 1, WHITE)
            self.screen.blit(text, (263,10))
            text = font.render(str(self.scoreB), 1, WHITE)
            self.screen.blit(text, (788,10))

            #COOPERATION scorekeeping will be one that adds them together. THERESA FIXED IT, SUCK IT TREBECK
            #font = pygame.font.Font(None, 74)
            #text = font.render(str(self.scoreA+self.scoreB), 1, WHITE)
            #self.screen.blit(text, (250,10))
            #text = font.render(str(self.scoreA+self.scoreB), 1, WHITE)
            #self.screen.blit(text, (420,10))

            # -- Display "win by two" message
            if winByTwo: 
                text = font.render("Win by 2!", 1, WHITE)
                self.screen.blit(text, ((SCREENW - text.get_width()) // 2, SCREENH // 4) )

            pygame.display.flip()
            self.clock.tick(FPS)

        tracker.finalize()  
    def scorePage(self):
        loop = True
        winnerTxt = ""
        if self.scoreA > self.scoreB:
            winnerTxt = "Left wins!"
        elif self.scoreB > self.scoreA:
            winnerTxt = "Right wins!"
        else:
            winnerTxt = "Tie game!"
        while loop:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    nextPage = False
                    loop = False
                elif event.type==pygame.KEYDOWN:
                    loop = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    loop = False
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 120)
            text = font.render(winnerTxt, 1, WHITE)
            self.screen.blit(text, ((SCREENW - text.get_width()) // 2, SCREENH // 3) )
            text = font.render(str(self.scoreA), 1, WHITE)
            self.screen.blit(text, (SCREENW//3 - text.get_width()//2, 2 * SCREENH//3))
            text = font.render(str(self.scoreB), 1, WHITE)
            self.screen.blit(text, (2 * SCREENW//3 - text.get_width()//2, 2 * SCREENH//3))
            pygame.display.flip()
            self.clock.tick(FPS)


