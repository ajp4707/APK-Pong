## CHANGES FOR SMALLER PADDLES. what if it is full screen, will that even work if the velocity maxes out?
# Aidan: Possible improvements
# Resizable window
# wait for joystick

import pygame
import os
from time import time #time resolution is pretty high, not sure how high though

from src.paddle import PaddleLeft, PaddleRight
from src.ball import Ball
#from src.data_tracker import dataTracker #additional item/function added to track all relevant information during game.
#from src.game_tracker import GameTracker
#from src.shadow import Shadow

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
                    if self.joys[0].get_button(0) == 1 and self.joys[1].get_button(0) == 1:
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

    def firstServePage(self, ball):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(pygame.font.get_default_font(),int(SIZE[1]/10.))
        loop = True
        tick = 0
        infoTxt = ""
        if ball.leftServe:
            infoTxt = "Left serves first"
        else:
            infoTxt = "Right serves first"
        while loop:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                      self.nextPage = False
                      loop = False
            self.screen.fill(BLACK)
            if tick >= (TEXTPAUSELENGTH) * FPS:
                loop = False
                break
            text = font.render(infoTxt, True, WHITE)

            textrect = text.get_rect()
            textrect.center = (SIZE[0]//2,SIZE[1]//2)
            self.screen.blit(text, textrect)
            pygame.display.flip()
            tick = tick + 1
            self.clock.tick(FPS)  

    def gamePage(self):
        self.scoreA = 0
        self.scoreB = 0
        
        # -- sync signal
        syncCount = 0

        # -- game objects
        paddleA = PaddleLeft(WHITE, PADW, PADH, SIZE)
        paddleB = PaddleRight(WHITE, PADW, PADH, SIZE)
        ball = Ball(WHITE, BALLW, BALLH)

        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(paddleA)
        all_sprites_list.add(paddleB)
        all_sprites_list.add(ball)

        ## -- shadow sprites to optimize game performance. They cover up previous sprite locations
        #shadow_sprites_list = pygame.sprite.Group()
        #shadow_sprites_list.add(Shadow(paddleA))
        #shadow_sprites_list.add(Shadow(paddleB))
        #shadow_sprites_list.add(Shadow(ball))
        #shadowSurf = pygame.Surface((625, 60))
        #shadowSurf.fill((BLACK))
        
        # -- Display who is serving first
        self.firstServePage(ball)
        if not self.nextPage:
            return

        font = pygame.font.Font(None, 50)

        # -- Loop variables
        loop = True
        paused = False
        scoreEvent = True
        scorePause = False
        serveEvent = False
        servePause = True
        tick = 0
        self.round = 0
        tutorial = True
        tutTick = 0
        #winByTwo = False

        ball.returnToCenter(SIZE)

        # -- Initialize trackers 
        #tracker = dataTracker(time())
        #game_tracker = GameTracker(time())
        endTime = time() + MAXTIME # can update in seconds of time (just over 3 minutes)

        # -- Main game loop
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
                        elif event.key == pygame.K_p: # Pressing p will pause the game
                            #tracker.pause_toggle(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                            paused = not paused
                        elif event.key == pygame.K_F1: # Sync signal event will go here. For now, K_F1
                            syncCount += 1
                            #tracker.sync_pulse(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, syncCount)
                elif event.type == pygame.JOYBUTTONDOWN and servePause:
                    if self.joys[0].get_button(0) == 1 and ball.leftServe:
                        y = paddleA.rect.centery
                        mid = SCREENH//2
                        if SERVETYPE == ServeType.TWOSTEP and twoStepFollow:
                            twoStepFollow = False
                        elif SERVETYPE != ServeType.WITHINBOUND or (SERVETYPE == ServeType.WITHINBOUND and y < mid + BOUNDRADIUS and y > mid - BOUNDRADIUS):
                            ball.serve(paddleA)
                            serveEvent = True
                    elif self.joys[1].get_button(0) == 1 and not ball.leftServe:
                        y = paddleB.rect.centery
                        mid = SCREENH//2
                        if SERVETYPE == ServeType.TWOSTEP and twoStepFollow:
                            twoStepFollow = False
                        elif SERVETYPE != ServeType.WITHINBOUND or (SERVETYPE == ServeType.WITHINBOUND and y < mid + BOUNDRADIUS and y > mid - BOUNDRADIUS):
                            ball.serve(paddleB)
                            serveEvent = True
            ## record the continuous game data into a different csv
            #game_tracker.add_row(paddleA.rect.y, paddleB.rect.y, ball.x, ball.y, ball.angle, ball.velocity, syncCount) 

            if paused: # allows us to pause the game using p key.
                self.clock.tick(FPS)
                continue

            keys = pygame.key.get_pressed()
            paddleA.adjustJoystick(self.joys[0].get_axis(0), SCREENH)
            paddleB.adjustJoystick(self.joys[1].get_axis(0), SCREENH)

            if scoreEvent:
                if scorePause: # pauses the screen immediately after the serve
                    tick = tick + 1
                    ball.velocity = 0
                    if tick >= FPS * PAUSELENGTH:
                        tick = 0
                        scorePause = False
                        servePause = True
                        ball.returnToCenter(SIZE)
                        #tracker.ball_reset(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                    self.clock.tick(FPS)
                    continue

                if (self.scoreA >= WINSCORE or self.scoreB >= WINSCORE):
                    if abs(self.scoreA-self.scoreB) < 2:   # win by 2 condition
                        winByTwo = True
                    else:
                        loop = False

                if (SERVETYPE == ServeType.STRAIGHT or SERVETYPE == ServeType.TOWARDCENTER or (SERVETYPE == ServeType.TWOSTEP and twoStepFollow)) and servePause:
                    ball.followPaddle(paddleA, paddleB)
    
                if serveEvent:
                    #tracker.serve_event(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                    scoreEvent = servePause = serveEvent = False
                    winByTwo = False
                    self.screen.fill(BLACK)

            # --- Game logic
            all_sprites_list.update()
    
            #Check if the ball is bouncing against any of the 4 walls:
            #if ball.rect.x >= 1035: # if ball hits Rside of screen
            if ball.rect.x >= SCREENW-BALLW:
                if not pygame.sprite.collide_mask(ball, paddleB): #and also is not hitting the paddle
                    scoreEvent = scorePause = True
                    self.scoreA += 1
                    self.updateRound(ball)
                    ball.rect.x = SCREENW-BALLW
                    ball.collideVertical()
                    #tracker.wall_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
            elif ball.rect.x <= 0: # Lside of screen
                if not pygame.sprite.collide_mask(ball, paddleA):
                    scoreEvent = scorePause = True
                    self.scoreB += 1
                    self.updateRound(ball)
                    ball.rect.x = 0
                    ball.collideVertical()
                    #tracker.wall_left(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
            #if ball.rect.y >= 735: # if the boundary of the screen is hit -- the bottom of the screen
            if ball.rect.y >= SCREENH-BALLH:
                ball.rect.y = SCREENH-BALLH
                ball.collideHorizontal()
                # ball.speedUpCondition() # place here to include in bounce count
                # tracker.wall_top(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                #tracker.wall_bottom(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
            elif ball.rect.y <= 0: #top of screen is hit
                ball.rect.y = 0
                ball.collideHorizontal()
                # ball.speedUpCondition() # place here to include in bounce count
                #tracker.wall_bottom(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)
                #tracker.wall_top(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y)  
        
            #Detect collisions between the ball and the paddles
            if pygame.sprite.collide_mask(ball, paddleA):
                ball.speedUpCondition()  # detect collisions for counter
                collision_percentile = ball.bounce(paddleA)
                #ball.rect.x = 18  # keep from getting stuck on the paddle
                ball.rect.x = PADW + 1
                # ball.collision_percentile(paddleA)
                #tracker.paddle_left(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, collision_percentile)
            elif pygame.sprite.collide_mask(ball, paddleB):
                ball.speedUpCondition()  # detecting collisions for counter
                collision_percentile = ball.bounce(paddleB)
                # ball.rect.x = 1017  # prevent sticking to paddleB
                ball.rect.x = SCREENW - PADW - BALLW - 1
                # ball.collision_percentile(paddleB)
                #tracker.paddle_right(time(), (ball.x, ball.y), ball.velocity, ball.angle, paddleA.rect.y, paddleB.rect.y, collision_percentile) #or 
            
            # shadows update after their counterparts
            #shadow_sprites_list.update()

            # --- Drawing 

            # Clear the screen
            self.screen.fill(BLACK)
            #shadow_sprites_list.draw(self.screen)   # clears old paddles and ball
            #self.screen.blit(shadowSurf, (263, 10)) # clears old score
            
            # Draw the net and sprites
            pygame.draw.line(self.screen, GRAY, [SCREENW//2, 0], [SCREENW//2, SCREENH], 13)
            all_sprites_list.draw(self.screen)

            ##Display scores: COMPETITIVE
            #text = font.render(str(self.scoreA), 1, WHITE)
            #self.screen.blit(text, (263,10))
            #text = font.render(str(self.scoreB), 1, WHITE)
            #self.screen.blit(text, (788,10))

            #C#OOPERATION scorekeeping will be one that adds them together. THERESA FIXED IT, SUCK IT TREBECK
            #font = pygame.font.Font(None, 74)
            #text = font.render(str(self.scoreA+self.scoreB), 1, WHITE)
            #self.screen.blit(text, (250,10))
            #text = font.render(str(self.scoreA+self.scoreB), 1, WHITE)
            #self.screen.blit(text, (420,10))

            # -- Display tutorial messages
            if tutorial:
                if tutTick >= ( 50 ) * FPS:
                    tutorial = False
                elif tutTick <= 8 * FPS:
                    text = font.render("Spin your joystick to move your paddle", True, WHITE)
                elif tutTick <= 16 * FPS:
                    text = font.render("You can aim your serve with the position of your paddle", True, WHITE)
                elif tutTick <= 25 * FPS:
                     text = font.render("When you have the ball, press your button to serve", True, WHITE)
                elif tutTick <= 32 * FPS:
                     text = font.render("The server alternates every 5 rounds in the actual game", True, WHITE)
                else:
                    text = font.render("", True, WHITE)

                textrect = text.get_rect()
                textrect.center = (SIZE[0]//2,SIZE[1]//6)
                self.screen.blit(text, textrect)
                tutTick += 1

            ## -- Display "win by two" message
            #if winByTwo: 
            #    text = font.render("Win by 2!", 1, WHITE)
            #    self.screen.blit(text, ((SCREENW - text.get_width()) // 2, SCREENH // 4) )

            pygame.display.flip()
            self.clock.tick(FPS)

        #tracker.finalize()  

    def updateRound(self, ball):
        self.round += 1
        if self.round >= SWITCHROUNDS:
            ball.serveToggle()
            self.round = 0

    def scorePage(self):
        loop = True
        #winnerTxt = ""
        #if self.scoreA > self.scoreB:
        #    winnerTxt = "Left wins!"
        #elif self.scoreB > self.scoreA:
        #    winnerTxt = "Right wins!"
        #else:
        #    winnerTxt = "Tie game!"
        winnerTxt = "Great job!"
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
            self.screen.blit(text, ((SCREENW - text.get_width()) // 2, (SCREENH - text.get_height()) // 2) )
            #self.screen.blit(text, ((SCREENW - text.get_width()) // 2, SCREENH // 3) )
            #text = font.render(str(self.scoreA), 1, WHITE)
            #self.screen.blit(text, (SCREENW//3 - text.get_width()//2, 2 * SCREENH//3))
            #text = font.render(str(self.scoreB), 1, WHITE)
            #self.screen.blit(text, (2 * SCREENW//3 - text.get_width()//2, 2 * SCREENH//3))
            pygame.display.flip()
            self.clock.tick(FPS)


# game = MainWindow()

