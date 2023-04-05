import pygame

class Picker:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 30)
        self.confirmed = [0, 0]
        self.pos = ['Rabbit', 'Owl', 'Giraffe', 'Kangaroo', 'Cheetah', 'Beetle']  # pos, as in possibilities
        self.on1 = 0
        self.on2 = 0
        self.imgs = {'Rabbit': pygame.transform.scale(pygame.image.load('images/rabbit.png').subsurface(pygame.Rect(54, 212, 32, 32)), (256, 256)),
                     'Owl': pygame.transform.scale(pygame.transform.scale2x(pygame.image.load('images/owl.png').subsurface(pygame.Rect(16, 48, 16, 16))), (256, 256)),
                     'Giraffe': pygame.transform.scale(pygame.transform.scale(pygame.image.load('images/giraffe.png').subsurface(pygame.Rect(110, 0, 110, 160)), (64, 32)), (128, 256)),
                     'Kangaroo': pygame.transform.scale(pygame.transform.scale(pygame.image.load('images/kangaroo.png').subsurface(pygame.Rect(200, 0, 100, 131)), (32, 32)), (256, 256)),
                     'Cheetah': pygame.transform.scale(pygame.transform.scale(pygame.image.load('images/cheetah.png'), (320, 64)).subsurface(pygame.Rect(80, 16, 32, 32)), (256, 256)),
                     'Beetle': pygame.transform.scale(pygame.transform.scale2x(pygame.image.load('images/beetle.png').subsurface(pygame.Rect(0, 110, 32, 16))), (256, 128))
                    }
        self.imgs['Owl'].set_colorkey((180, 203, 224))
        self.imgs['Giraffe'].set_colorkey((255, 255, 255))
        self.imgs['Cheetah'].set_colorkey((2, 139, 218))
        # Speed, jump height, jump distance, strength (default 2, 2, 5, 3)
        self.stats = {'Rabbit': [4, 2, 7, 4],
                      'Owl': [2, 4, 5, 2],
                      'Giraffe': [3, 3, 5, 3],
                      'Kangaroo': [2, 4, 8, 3.5],
                      'Cheetah': [7, 1, 4, 1],
                      'Beetle': [5, 3, 4, 1.5]
                    }
        self.basketball = pygame.transform.scale(pygame.image.load('images/basketball.png'), (256, 256))

    def pick(self):
        while not all(self.confirmed):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and not self.confirmed[0]:
                        self.on1 += 1
                        if self.on1 >= len(self.pos):
                            self.on1 = 0
                    elif event.key == pygame.K_a and not self.confirmed[0]:
                        self.on1 -= 1
                        if self.on1 < 0:
                            self.on1 = len(self.pos) - 1
                    elif event.key == pygame.K_RIGHT and not self.confirmed[1]:
                        self.on2 += 1
                        if self.on2 >= len(self.pos):
                            self.on2 = 0
                    elif event.key == pygame.K_LEFT and not self.confirmed[1]:
                        self.on2 -= 1
                        if self.on2 < 0:
                            self.on2 = len(self.pos) - 1
                    elif event.key == pygame.K_w and not self.confirmed[0]:
                        self.confirmed[0] = self.pos[self.on1]
                    elif event.key == pygame.K_UP and not self.confirmed[1]:
                        self.confirmed[1] = self.pos[self.on2]
            self.screen.fill((0,100,0))
            self.screen.blit(self.imgs[self.pos[self.on1]], (20 + (64 if self.pos[self.on1] == 'Giraffe' else 0), 20 + (64 if self.pos[self.on1] == 'Beetle' else 0)))
            self.screen.blit(self.imgs[self.pos[self.on2]], (724 + (64 if self.pos[self.on2] == 'Giraffe' else 0), 20 + (64 if self.pos[self.on2] == 'Beetle' else 0)))
            #self.screen.blit(self.font.render(self.descripts[self.pos[self.on1]], 1, (255,255,255)), (20, 300))
            #self.screen.blit(self.font.render(self.descripts[self.pos[self.on2]], 1, (255,255,255)), (724, 300))
            self.screen.blit(self.font.render('Speed ', 1, (255,255,255)), (20, 300))
            self.screen.blit(self.font.render('Jump Height ', 1, (255,255,255)), (20, 330))
            self.screen.blit(self.font.render('Jump Distance ', 1, (255,255,255)), (20, 360))
            self.screen.blit(self.font.render('Strength', 1, (255,255,255)), (20, 390))
            self.screen.blit(self.font.render('Speed', 1, (255,255,255)), (920, 300))
            self.screen.blit(self.font.render('Jump Height', 1, (255,255,255)), (856, 330))
            self.screen.blit(self.font.render('Jump Distance', 1, (255,255,255)), (836, 360))
            self.screen.blit(self.font.render('Strength', 1, (255,255,255)), (906, 390))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(215, 310, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(215, 340, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(215, 370, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(215, 400, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(600, 310, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(600, 340, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(600, 370, 200, 20))
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(600, 400, 200, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(215, 310, self.stats[self.pos[self.on1]][0] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(215, 340, self.stats[self.pos[self.on1]][1] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(215, 370, self.stats[self.pos[self.on1]][2] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(215, 400, self.stats[self.pos[self.on1]][3] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(800 - self.stats[self.pos[self.on2]][0] * 20, 310, self.stats[self.pos[self.on2]][0] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(800 - self.stats[self.pos[self.on2]][1] * 20, 340, self.stats[self.pos[self.on2]][1] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(800 - self.stats[self.pos[self.on2]][2] * 20, 370, self.stats[self.pos[self.on2]][2] * 20, 20))
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(800 - self.stats[self.pos[self.on2]][3] * 20, 400, self.stats[self.pos[self.on2]][3] * 20, 20))
            self.screen.blit(self.basketball, (378, 400))
            pygame.display.update()
        return self.confirmed

if __name__ == '__main__':
    # Test the picker
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_icon(pygame.image.load('images/Basketball.png'))
    pygame.display.set_caption('Animal Basketball v1.0')
    print(Picker(screen).pick())
    pygame.quit()
