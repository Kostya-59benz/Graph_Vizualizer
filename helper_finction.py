
import pygame
from pygame._sdl2 import Texture
from object import FONT_NAME



ctn_edge = ctn_vertex = 0






# TODO: REWORK FUNCION TO RENEW TABLE
def make_rows(vertex_t, edge_t, vertex, edge):

    global ctn_vertex, ctn_edge


    if vertex != None:
        vertex_t.append(vertex)
        ctn_vertex +=1
    if edge != None:
        edge_t.append(edge)
        ctn_edge +=1

    return ctn_vertex,ctn_edge



# draw table
def grid(renderer=None,cnt_vertex=0,cnt_edge=0,size=500,object_pair = None):   
    rows = cnt_vertex
    
    x = 0
    y = 0
    ctn = 0
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
