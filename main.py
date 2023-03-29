import pygame 
from pygame._sdl2 import Window, Renderer


from interface import ObjectsGroup
from object import Button, Circle, Edge, buttons
from helper_function import make_rows, grid, redraw_table


SIZE = WIDTH,  HEIGHT = 800, 640
FPS = 120


W_BUTTON = 150
H_BUTTON = 50



#Entry point
def main():
    
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    
    btn = Button(550, 30, W_BUTTON + 100, H_BUTTON,"Видалити вершину зі збереженням зв'зку")
    btn_1 = Button(350, 30, W_BUTTON, H_BUTTON,"Матриця суміжності")
    btn_2 = Button(150, 30, W_BUTTON, H_BUTTON,"Очистити вікно")


    objects_group = ObjectsGroup()
    

    win = 0 

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
                        for _ in range(objects_group.len_pairs()): 
                                
                            list_pairs = objects_group.get_pairs()
                            
                            for pair in list_pairs:
                                print(pair[0].score, pair[1].score)
                                pair = list(pair)
                                for el in pair:
                                    if el == e:
                                        objects_group.remove_pair(tuple(pair))
                                        objects_group.chose_edge_and_remove(pair[0].position,pair[1].position)
                                        pair.remove(e)
                                        objects_group.remove(e)    
                                        if delete:
                                            helper.append(changed_vertex.position)
                                            helper.append(pair[0].position)
                                            pair.append(changed_vertex)
                                            objects_group.add_edge(Edge(screen,changed_vertex.position, pair[0].position),helper)
                                            helper.clear()
                        delete = False

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

                if flag and not btn_2.check_collision(x,y):
                    objects_group.clear()
                    score = 0
                    redraw_table()

        for button in buttons:
            button.process(screen)
            
        objects_group.draw()
        objects_group.draw_edge()
        

        pygame.display.flip()
        clock.tick(FPS)
    
if __name__ == '__main__':
    main()