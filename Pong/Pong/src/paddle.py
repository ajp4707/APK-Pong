import pygame
BLACK = (0,0,0)

class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.height = height
        self.width = width

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y < 0: #top of the screen
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y > 600: #bottom of the screen
            self.rect.y = 600

    def adjustJoystick(self, joyInput, screenH): # called by main, should only be used with joysticks
        range = screenH - self.height
        self.rect.y = joyInput * (range/2) + (range/2) # translates (-1,1) range to (0,675) pixel location

class PaddleLeft(Paddle):
    def __init__(self, color, width, height, screenSizeTuple):
        super().__init__(color, width, height)
        screenW, screenH = screenSizeTuple
        self.rect.x = 0
        self.rect.centery = screenH // 2

class PaddleRight(Paddle):
    def __init__(self, color, width, height, screenSizeTuple):
        super().__init__(color, width, height)
        screenW, screenH = screenSizeTuple
        self.rect.x = screenW - width
        self.rect.centery = screenH // 2