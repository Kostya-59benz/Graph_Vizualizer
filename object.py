import pygame

from abc import abstractmethod

from math import sqrt

buttons = []
pygame.init()

FONT_SYS_FONT =  pygame.font.SysFont('Arial', 15)
FONT_NAME = pygame.font.match_font('Arial')

class Drawable:
    @abstractmethod
    def draw(self):
        pass


class HasColissions:
    @abstractmethod
    def check_collision(self, x: int, y: int):
        pass

        





class Circle(Drawable, HasColissions):
    
    def __init__(self, x: int, y: int, screen: pygame.Surface, score: int,radius: int = 20):
        self.x = x
        self.y = y
        self.screen = screen
        self.radius = radius
        self._score = score

    @property
    def position(self):
        return self.x, self.y


    @property
    def score(self):
        return self._score


    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255),
                           self.position, self.radius)
        
        self._draw_text(self.screen,self._score,18)

    def _draw_text(self,surf, score, size):
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(str(score), True, (255,255,255))
        if score <=9:
            surf.blit(text_surface,(self.x-4.5,self.y-8))
        else:
            surf.blit(text_surface,(self.x-10,self.y-8))


    def check_collision(self, x: int, y: int):
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2) <= self.radius


class Edge(Drawable):
    def __init__(self,screen: pygame.Surface,position1: tuple[int,int],position2: tuple[int,int]):
        self.screen = screen
        self.position1 = position1
        self.position2 = position2

    @property
    def positions(self):
        return (self.position1, self.position2)

    def draw(self):
        if self.position1 == self.position2:
            return
        pygame.draw.aaline(self.screen, (0, 0, 255),
                        self.position1, self.position2)


class Button(HasColissions):
    def __init__(self, x, y, width, height, buttonText='Nonamed Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#808080',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = FONT_SYS_FONT.render(buttonText, True, (20, 20, 20))
        buttons.append(self)

    def process(self,screen):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
        
        return self.alreadyPressed

    def check_collision(self, x: int, y: int):
        return not self.buttonRect.collidepoint(x,y)
    

        """ if self.buttonRect[0] <= x and x <= self.buttonRect[0] + self.width and self.buttonRect[1] <= y and y <= self.buttonRect[1] + self.height:
            return False
        else: return True """
