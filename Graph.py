from typing import Union, Final

import pygame
import os

from abc import abstractmethod
from math import sqrt

from pygame._sdl2 import *

    
SIZE = WIDTH,  HEIGHT = 800, 640
FPS: Final = 120
pygame.init()
FONT_SYS_FONT =  pygame.font.SysFont('Arial', 15)
FONT_NAME = pygame.font.match_font('Arial')
W_BUTTON = 150
H_BUTTON = 50
buttons = []

ctn_edge = 0
ctn_vertex = 0

class Drawable:
    @abstractmethod
    def draw(self):
        pass


class HasColissions:
    @abstractmethod
    def check_collision(self, x: int, y: int):
        pass

        


class Button(HasColissions):
    def __init__(self, x, y, width, height, buttonText='Nonamed Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#555555',
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
        if self.buttonRect[0] <= x and x <= self.buttonRect[0] + self.width and self.buttonRect[1] <= y and y <= self.buttonRect[1] + self.height:
            return False
        else: return True



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
        
        self.draw_text(self.screen,self._score,18)

    def draw_text(self,surf, score, size):
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




class ObjectsGroup:
    def __init__(self):
        self._objects: list[Union[Drawable, HasColissions]] = []
        self._objects_edges: list[Union[Drawable, HasColissions]] = []
        self.pairs = []

    def add(self, element: Union[Drawable, HasColissions]):
        self._objects.append(element)

    def add_edge(self, element: Union[Drawable, HasColissions], helper):
        self._objects_edges.append(element)
        self._make_pairs(*helper)

    def remove(self, element: Union[Drawable, HasColissions]):
        self._objects.remove(element)

    def remove_edge(self,element: Union[Drawable, HasColissions]):
        self._objects_edges.remove(element)

    def chose_edge_and_remove(self,pos1,pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        for e in self._objects_edges:
            if e.positions == (self.pos1, self.pos2) or e.positions == (self.pos2, self.pos1):
                self.remove_edge(e)

    def clear(self):
        self._objects = []
        self._objects_edges = []

    @property
    def objects(self):
        return self._objects.copy()

    
    def draw(self):
        for e in self._objects:
            e.draw()
    
    def _make_pairs(self,vertex1,vertex2):
        pair = []
        for el in (vertex1,vertex2):
            check = self.check_colission(*el)
            if len(check) >0:
                pair.append(*check)
                if len(pair) == 2:
                    self.pairs.append((pair[0],pair[1]))
                    pair.clear()
        

    def get_pairs(self):
        return self.pairs



    def draw_edge(self):
        for e in self._objects_edges:
            e.draw()    


    

    def check_colission(self, x: int, y: int):
        result = []

        for e in self._objects:
            if e.check_collision(x, y):
                result.append(e)
        return result



def make_rows(vertex_t, edge_t, vertex, edge):

    global ctn_edge, ctn_vertex

    if vertex != None:
        vertex_t.append(vertex)
        ctn_vertex +=1
    if edge != None:
        edge_t.append(edge)
        ctn_edge +=1
    return ctn_vertex, ctn_edge



# draw table
def grid(renderer=None,cnt_vertex=0,cnt_edge=0,size=500,object_pair = None):   
    rows = cnt_vertex
    x = 0
    y = 0
    ctn = 0
    print(rows)
    ones = object_pair.get_pairs()
    
    for el in ones:
        print(el[0].score, el[1].score)
        print('------------')

    
    

    
    if rows > 0:
        distance_btw_rows = size // rows
        step = distance_btw_rows//2 
        step_offset=step


        font = pygame.font.Font(FONT_NAME, distance_btw_rows//2)

        for _ in range(rows):
            x += distance_btw_rows
            y += distance_btw_rows
            print(x,y)
            renderer.draw_color = (255, 255, 255, 255)
            renderer.draw_line((x, 0), (x, size+100))
            renderer.draw_line((0, y), (size+100, y))

        x = 0
        y = -1
        
        text_surface = font.render(str(ctn), True, (255,255,255))
        tex2 = Texture.from_surface(renderer, text_surface)

        tex2.draw(dstrect=((x+step), (y+step_offset)))

        ctn +=1
        text_surface = font.render(str(ctn), True, (255,255,255))
        tex3 = Texture.from_surface(renderer, text_surface)
        step = distance_btw_rows + step
        
        for _ in range(rows+1):
            text_surface = font.render(str(ctn), True, (255,255,255))
            tex = Texture.from_surface(renderer, text_surface)
            tex.draw(dstrect=((x+step), (y+step_offset)))
            tex.draw(dstrect=((x+step_offset), (y+step)))
            tex2.draw(dstrect=((x+step), (y+step)))
            for pair in ones:
                if pair[0].score < pair[1].score and pair[0].score == ctn:
                        tex3.draw(dstrect=((x+step+50), (y+step)))
                elif pair[0].score > pair[1].score and pair[1].score == ctn:
                        tex3.draw(dstrect=((x+step+50), (y+step)))
                print(ctn)
            ctn +=1
            
            step = distance_btw_rows + step

        

            
        print('---------------')
        renderer.present()

    
def main():
    
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    
    btn = Button(550, 30, W_BUTTON, H_BUTTON,"Роз'єднати вершини")
    btn_1 = Button(350, 30, W_BUTTON, H_BUTTON,"Створити таблицю")
    btn_2 = Button(150, 30, W_BUTTON, H_BUTTON,"Очистити вікно")


    objects_group = ObjectsGroup()
    
    win = Window("Table", resizable =True, size=(500, 500))
   
    global ctn_vertex

    helper = []
    score = 0
    flag = False
    
    vertex_t = []
    edge_t = []

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif getattr(event, "window", None) == win:
                if event.type == pygame.WINDOWCLOSE:
                    win.destroy()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1 and btn.check_collision(x,y) and btn_1.check_collision(x,y):
                    score+=1
                    circle = Circle(x, y, screen,score)
                    objects_group.add(circle)
                    make_rows(vertex_t,edge_t,circle,None)
                elif event.button == 3:
                    for e in objects_group.check_colission(x, y):
                            helper.append(e.position)
                            if len(helper) == 2:
                                edge = Edge(screen,helper[0],helper[1])
                                objects_group.add_edge(
                                edge, helper)
                                make_rows(vertex_t,edge_t,None,edge)
                                helper.clear()
                elif event.button == 4:
                    for e in objects_group.check_colission(x, y):
                       objects_group.remove(e)
                for button in buttons:
                    if button.process(screen) == True:
                        flag = True
                if event.button == 5 and flag:
                    for e in objects_group.check_colission(x, y):
                        helper.append(e.position)
                        if len(helper) == 2:
                            objects_group.chose_edge_and_remove(helper[0],helper[1])
                            helper.clear()
                            flag = False         
                if flag and not btn_1.check_collision(x,y):
                    win = Window("Table",size=(500, 500))
                    renderer = Renderer(win)
                    grid(renderer,*make_rows(vertex_t,edge_t,None,None),400,objects_group)

                if flag and not btn_2.check_collision(x,y):
                    objects_group.clear()
                    score = 0
                    ctn_vertex = 0
                    
        for button in buttons:
            button.process(screen)
            
        objects_group.draw()
        objects_group.draw_edge()
        

        pygame.display.flip()
        clock.tick(FPS)
    


if __name__ == '__main__':
    main()
