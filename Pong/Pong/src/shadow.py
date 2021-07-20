import pygame

class Shadow(pygame.sprite.Sprite):
    def __init__(self, sprite, color=(0,0,0)):
        super().__init__()
        
        # create image and rect for this shadow
        self.image = pygame.Surface([sprite.width, sprite.height])
        pygame.draw.rect(self.image, color, [0, 0, sprite.width, sprite.height])
        self.rect = self.image.get_rect()

        # vars to keep track of the sprite
        self.sprite = sprite
        self.oldx = self.sprite.rect.x
        self.oldy = self.sprite.rect.y

    def update(self):
        self.rect.x = self.oldx
        self.rect.y = self.oldy
        self.oldx = self.sprite.rect.x
        self.oldy = self.sprite.rect.y
        return