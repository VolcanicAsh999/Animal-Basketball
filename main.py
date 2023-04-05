import pygame
import ball
import player
import picker

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Animal Basketball v1.0')
pygame.display.set_icon(pygame.image.load('images/basketball.png'))

class Game:
    def __init__(self, p1, p2):
        self.screen = screen
        self.dt = 0.1
        self.clock = pygame.time.Clock()
        # Positions figured out by reset() call at end
        self.p1 = getattr(player, p1, player.Rabbit)(0, 0)
        self.p2 = getattr(player, p2, player.Rabbit)(0, 0)
        self.ground = pygame.Rect(0, 690, 1000, 10)
        self.catch_delay = 0
        self.steal_delay = 0
        self.score1 = 0
        self.score2 = 0
        self.hoop1_rect = pygame.Rect(0, 550, 30, 5)
        self.hoop2_rect = pygame.Rect(970, 550, 30, 5)
        self.font = pygame.font.SysFont('Arial', 30)
        self.reset()

    def update(self):
        self.keypress()
        if self.catch_delay > 0:
            self.catch_delay -= 1
        if self.steal_delay > 0:
            self.steal_delay -= 1
        if self.ball:
            self.ball.update(self.dt, self.ground)
            if self.p1.rect.colliderect(self.ball.rect) and self.catch_delay == 0:
                self.ball = None
                self.p1.holding_ball = True
            elif self.p2.rect.colliderect(self.ball.rect) and self.catch_delay == 0:
                self.ball = None
                self.p2.holding_ball = True
        else:
            if self.p1.rect.colliderect(self.p2.rect) and self.steal_delay == 0:
                if self.p1.holding_ball:
                    self.p1.holding_ball = False
                    self.p2.holding_ball = True
                elif self.p2.holding_ball:
                    self.p1.holding_ball = True
                    self.p2.holding_ball = False
                self.steal_delay = 50
        self.p1.update(self.dt, self.ground)
        self.p2.update(self.dt, self.ground)
        self.check_hoops()
        self.draw()

    def reset(self):
        self.ball = ball.Ball()
        self.ball.set_pos((485, 300))
        self.p1.rect.x = 10
        self.p1.rect.y = 600
        self.p2.rect.x = 990 - self.p2.w
        self.p2.rect.y = 600
        self.p1.move = 0
        self.p1.lmove = 0
        self.p2.move = 0
        self.p2.lmove = 0
        self.p1.jumping = True
        self.p1.dy = 0.1
        self.p2.jumping = True
        self.p2.dy = 0.1
        self.p1.active_img = self.p1.right_img
        self.p2.active_img = self.p2.left_img
        self.p1.holding_ball = False
        self.p2.holding_ball = False

    def check_hoops(self):
        if self.p1.holding_ball and self.p1.rect.colliderect(self.hoop2_rect):
            self.reset()
            self.score1 += 2
        elif self.p2.holding_ball and self.p2.rect.colliderect(self.hoop1_rect):
            self.reset()
            self.score2 += 2
        if self.ball:
            if self.ball.rect.colliderect(self.hoop1_rect) and self.ball.rect.y < self.hoop1_rect.y:
                self.reset()
                self.score2 += 3
            elif self.ball.rect.colliderect(self.hoop2_rect) and self.ball.rect.y < self.hoop2_rect.y:
                self.reset()
                self.score1 += 3

    def draw(self):
        self.screen.fill((0,100,0))
        self.screen.blit(self.font.render(f'Player 1: {str(self.score1).zfill(5)}', 1, (255,255,255)), (5, 5))
        self.screen.blit(self.font.render(f'Player 2: {str(self.score2).zfill(5)}', 1, (255,255,255)), (825, 5))
        pygame.draw.rect(self.screen, pygame.Color('orange'), self.hoop1_rect)
        pygame.draw.rect(self.screen, pygame.Color('orange'), self.hoop2_rect)
        if self.ball:
            self.ball.draw(self.screen)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.ground)
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        pygame.display.update()

    def shoot(self, player):
        self.ball = ball.Ball(player.rect.x + ((abs(player.lmove) / player.lmove) * player.rect.w), (700 - player.rect.y) - 20, ((abs(player.lmove) / player.lmove) * 20 * player.strength), 70)
        self.catch_delay = 10

    def keypress(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.p1.move_(-1)
                elif event.key == pygame.K_d:
                    self.p1.move_(1)
                elif event.key == pygame.K_w:
                    self.p1.move_(jump=True)
                elif event.key == pygame.K_s and self.p1.holding_ball:
                    self.p1.holding_ball = False
                    self.shoot(self.p1)
                elif event.key == pygame.K_LEFT:
                    self.p2.move_(-1)
                elif event.key == pygame.K_RIGHT:
                    self.p2.move_(1)
                elif event.key == pygame.K_UP:
                    self.p2.move_(jump=True)
                elif event.key == pygame.K_DOWN and self.p2.holding_ball:
                    self.p2.holding_ball = False
                    self.shoot(self.p2)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    self.p1.move_(0)
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.p2.move_(0)

    def loop(self):
        while True:
            self.clock.tick(60)
            self.update()

def main():
    pick = picker.Picker(screen)
    picked = pick.pick()
    game = Game(*picked)
    game.loop()

if __name__ == '__main__':
    main()
