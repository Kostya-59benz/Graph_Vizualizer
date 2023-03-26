import pygame 
import os



from interface import ObjectsGroup
from object import Button, Circle, Edge, buttons
from helper_finction import make_rows, grid
from pygame._sdl2 import Window, Renderer





SIZE = WIDTH,  HEIGHT = 800, 640
FPS = 120


W_BUTTON = 150
H_BUTTON = 50



#Entry point
def main():
    
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    
    btn = Button(550, 30, W_BUTTON + 100, H_BUTTON,"Видалити вершину зі збереженням зв'зку")
    btn_tested = Button(550, 100, W_BUTTON + 100, H_BUTTON,"Видалити вершину без збереження зв'зку")
    btn_1 = Button(350, 30, W_BUTTON, H_BUTTON,"Матриця суміжності")
    btn_2 = Button(150, 30, W_BUTTON, H_BUTTON,"Очистити вікно")


    objects_group = ObjectsGroup()
    
    win = Window()
   
    global ctn_vertex

    helper = []
    score = 0
    flag = False
    delete = False
    changed_vertex = None




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
                        if delete:
                            for _ in range(6): 
                                
                                list_pairs = objects_group.get_pairs()


                                for pair in list_pairs:

                                    pair = list(pair)
                                    for el in pair:
                                        if el == e:
                                            objects_group.remove_pair(tuple(pair))
                                            objects_group.chose_edge_and_remove(pair[0].position,pair[1].position)
                                            pair.remove(e)
                                            objects_group.remove(e)
                                            helper.append(changed_vertex.position)
                                            helper.append(pair[0].position)
                                            pair.append(changed_vertex)
                                            objects_group.add_edge(Edge(screen,changed_vertex.position, pair[0].position),helper)
                                            delete = False
                                            helper.clear()
                                    
                                                                    
                                #print(pair[0].score, pair[1].score)
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

                if flag and not btn.check_collision(x,y):
                    while True:
                        vertex_num = input("Зміна вершини\n")
                        if int(vertex_num) > score:
                            print('Вершины с таким номером еще нету на поле. Пожалуйста проверте свой выбор и введите правильне число!')
                        else: 
                            changed_vertex = objects_group.change_direction(int(vertex_num))
                            delete = True
                            break

                if flag and not btn_tested.check_collision(x,y):
                    while True:
                        ...


                #FIX THIS FUNC
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