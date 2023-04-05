import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.right_img = None
        self.left_img = None
        self.jump_left_img = None
        self.jump_right_img = None
        self.active_img = self.right_img
        self.holding_ball = False
        self.move = 0
        self.lmove = 0
        self.jumping = True
        self.speed = 2
        self.dy = 0.1
        self.w = 32
        self.h = 32
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.ball_img = pygame.image.load('images/basketball.png')
        self.anim_delay = 0
        self.jump_height = 2
        self.jump_dist = 5
        self.strength = 3

    def move_(self, x=0, jump=False):
        if x > 0 and not self.jumping:
            self.active_img = self.right_img
            self.move = self.speed
            self.lmove = self.move
        elif x < 0 and not self.jumping:
            self.active_img = self.left_img
            self.move = -self.speed
            self.lmove = self.move
        elif self.move:
            self.move = 0
        if jump and not self.jumping:
            self.jumping = True
            self.dy = -self.jump_height
            self.rect.y -= self.jump_height
            if self.lmove < 0:
                self.active_img = self.jump_left_img
            elif self.lmove >= 0:
                self.active_img = self.jump_right_img

    def update(self, dt, ground):
        super().update(dt)
        if self.jumping:
            self.dy += .25 / self.jump_dist
            if self.rect.colliderect(ground):
                self.dy = 0
                self.jumping = False
                if self.lmove < 0:
                    self.move = -self.speed
                    self.active_img = self.left_img
                elif self.lmove > 0:
                    self.move = self.speed
                    self.active_img = self.right_img
                else:
                    self.move = 0
                    self.active_img = self.right_img
            self.rect.y += self.dy
            self.rect.x += self.lmove
            if self.rect.x > 1000 - self.w:
                self.rect.x -= self.lmove
                self.lmove = -self.speed
                if self.active_img == self.jump_right_img:
                    self.active_img = self.jump_left_img
            elif self.rect.x < 0:
                self.rect.x += self.lmove
                self.lmove = self.speed
                if self.active_img == self.jump_left_img:
                    self.active_img = self.jump_right_img
        elif self.move != 0:
            self.rect.x += self.move
            if self.rect.x > 1000 - self.w:
                self.rect.x -= self.move
                self.move = -self.speed
                if self.active_img == self.right_img:
                    self.active_img = self.left_img
            elif self.rect.x < 0:
                self.rect.x += self.move
                self.move = self.speed
                if self.active_img == self.left_img:
                    self.active_img = self.right_img

    def draw(self, screen):
        try: # Animations are defaulted to no animation
            screen.blit(self.active_img, (self.rect.x, self.rect.y))
        except:
            self.anim_delay += 1
            if self.anim_delay <= 5:
                screen.blit(self.active_img[0], (self.rect.x, self.rect.y))
            elif self.anim_delay <= 10:
                screen.blit(self.active_img[1], (self.rect.x, self.rect.y))
            else:
                screen.blit(self.active_img[0], (self.rect.x, self.rect.y))
                self.anim_delay = 0
        if self.holding_ball:
            if self.lmove < 0 or self.move < 0:
                screen.blit(self.ball_img, (self.rect.x - self.w, self.rect.y))
            else:
                screen.blit(self.ball_img, (self.rect.x + self.w, self.rect.y))

class Rabbit(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        sheet = pygame.image.load('images/rabbit.png')
        self.right_img = sheet.subsurface(pygame.Rect(54, 212, 32, 32))
        self.left_img = sheet.subsurface(pygame.Rect(57, 284, 32, 32))
        self.jump_right_img = sheet.subsurface(pygame.Rect(84, 212, 40, 32))
        self.jump_left_img = sheet.subsurface(pygame.Rect(90, 284, 40, 32))
        self.active_img = self.right_img
        self.speed = 4
        self.jump_dist = 7
        self.strength = 4

class Owl(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        sheet = pygame.image.load('images/owl.png')
        self.right_img = pygame.transform.scale2x(sheet.subsurface(pygame.Rect(16, 48, 16, 16)))
        self.left_img = pygame.transform.flip(self.right_img, True, False)
        self.jump_left_img = self.jump_right_img = [
            pygame.transform.scale2x(sheet.subsurface(pygame.Rect(16, 16, 16, 16))),
            pygame.transform.scale2x(sheet.subsurface(pygame.Rect(48, 16, 16, 16)))
        ]
        self.right_img.set_colorkey((180, 203, 224))
        self.left_img.set_colorkey((180, 203, 224))
        self.jump_left_img[0].set_colorkey((180, 203, 224))
        self.jump_left_img[1].set_colorkey((180, 203, 224))
        self.active_img = self.right_img
        self.num = 0
        self.jump_height = 4
        self.strength = 2

    def move_(self, x=0, jump=False):
        if x > 0 and not self.jumping:
            self.active_img = self.right_img
            self.move = self.speed
            self.lmove = self.move
        elif x < 0 and not self.jumping:
            self.active_img = self.left_img
            self.move = -self.speed
            self.lmove = self.move
        elif self.move:
            self.move = 0
        if jump and ((not self.jumping) or self.num < 2):
            self.num += 1
            self.jumping = True
            self.dy = -self.jump_height
            self.rect.y -= self.jump_height
            if self.lmove < 0:
                self.active_img = self.jump_left_img
            elif self.lmove >= 0:
                self.active_img = self.jump_right_img

    def update(self, dt, ground):
        pygame.sprite.Sprite.update(self, dt)
        if self.jumping:
            self.dy += .25 / self.jump_dist
            if self.rect.colliderect(ground):
                self.dy = 0
                self.jumping = False
                self.num = 0
                if self.lmove < 0:
                    self.move = -self.speed
                    self.active_img = self.left_img
                elif self.lmove > 0:
                    self.move = self.speed
                    self.active_img = self.right_img
                else:
                    self.move = 0
                    self.active_img = self.right_img
            self.rect.y += self.dy
            self.rect.x += self.lmove
            if self.rect.x > 1000 - self.w:
                self.rect.x -= self.lmove
                self.lmove = -self.speed
                if self.active_img == self.jump_right_img:
                    self.active_img = self.jump_left_img
            elif self.rect.x < 0:
                self.rect.x += self.lmove
                self.lmove = self.speed
                if self.active_img == self.jump_left_img:
                    self.active_img = self.jump_right_img
        elif self.move != 0:
            self.rect.x += self.move
            if self.rect.x > 1000 - self.w:
                self.rect.x -= self.move
                self.move = -self.speed
                if self.active_img == self.right_img:
                    self.active_img = self.left_img
            elif self.rect.x < 0:
                self.rect.x += self.move
                self.move = self.speed
                if self.active_img == self.left_img:
                    self.active_img = self.right_img

class Giraffe(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 3
        self.w = 32
        self.h = 64
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.left_img = pygame.transform.scale(pygame.image.load('images/giraffe.png').subsurface(pygame.Rect(110, 0, 110, 160)), (32, 64))
        self.right_img = pygame.transform.flip(self.left_img, True, False)
        self.jump_left_img = pygame.transform.rotate(self.left_img, -30)
        self.jump_right_img = pygame.transform.rotate(self.right_img, 30)
        self.left_img.set_colorkey((255,255,255))
        self.right_img.set_colorkey((255,255,255))
        self.jump_left_img.set_colorkey((255,255,255))
        self.jump_right_img.set_colorkey((255,255,255))
        self.active_img = self.right_img
        self.jump_height = 3

class Kangaroo(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.right_img = pygame.transform.scale(pygame.image.load('images/kangaroo.png').subsurface(pygame.Rect(200, 0, 100, 131)), (32, 32))
        self.left_img = pygame.transform.flip(self.right_img, True, False)
        self.jump_left_img = pygame.transform.rotate(self.left_img, -10)
        self.jump_right_img = pygame.transform.rotate(self.right_img, 10)
        self.active_img = self.right_img
        self.jump_height = 4
        self.jump_distance = 8
        self.strength = 3.5

class Cheetah(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        sheet = pygame.transform.scale(pygame.image.load('images/cheetah.png'), (320, 64))
        self.left_img = sheet.subsurface(pygame.Rect(80, 16, 32, 32))
        self.right_img = pygame.transform.flip(self.left_img, True, False)
        self.jump_left_img = sheet.subsurface(pygame.Rect(16, 16, 32, 32))
        self.jump_right_img = pygame.transform.flip(self.jump_left_img, True, False)
        for i in [self.left_img, self.right_img, self.jump_left_img, self.jump_right_img]:
            i.set_colorkey((2, 139, 218))
        self.active_img = self.right_img
        self.jump_height = 1
        self.jump_distance = 4
        self.speed = 7
        self.strength = 1

class Beetle(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.w = 64
        self.h = 32
        self.rect = pygame.Rect(x, y, self.w, self.h)
        sheet = pygame.image.load('images/beetle.png')
        self.left_img = pygame.transform.scale2x(sheet.subsurface(0, 110, 32, 16))
        self.right_img = pygame.transform.scale2x(sheet.subsurface(pygame.Rect(96, 46, 32, 16)))
        self.jump_left_img = [pygame.transform.rotate(pygame.transform.scale2x(sheet.subsurface(pygame.Rect(96, 110, 32, 16))), -10),
                              pygame.transform.rotate(pygame.transform.scale2x(sheet.subsurface(pygame.Rect(96, 110, 32, 16))), 10)]
        self.jump_right_img = [pygame.transform.rotate(pygame.transform.scale2x(sheet.subsurface(pygame.Rect(0, 46, 32, 16))), -10),
                              pygame.transform.rotate(pygame.transform.scale2x(sheet.subsurface(pygame.Rect(0, 46, 32, 16))), 10)]
        self.active_img = self.right_img
        self.jump_height = 4
        self.jump_distance = 3
        self.speed = 5
        self.strength = 1.5
