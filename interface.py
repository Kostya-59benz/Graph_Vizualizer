
from typing import Union
from object import Drawable, HasColissions


from pygame._sdl2 import messagebox

# INTERFACE 
class ObjectsGroup:
    def __init__(self):
        self._objects: list[Union[Drawable, HasColissions]] = []
        self._objects_edges: list[Union[Drawable, HasColissions]] = []
        self.pairs = []

    def add(self, element: Union[Drawable, HasColissions]):
        self._objects.append(element)

    def add_edge(self, element: Union[Drawable, HasColissions], helper = None):
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
        self._objects.copy()
    



    
    def draw(self):
        for e in self._objects:
            e.draw()


    def change_direction(self,val: int):
        for el in self._objects:
            if el.score == val:
                return el                
                
        


    
    def _make_pairs(self,vertex1: tuple ,vertex2: tuple):
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


    def remove_pair(self, pair):
        for saved_pair in self.pairs:
            
            if saved_pair == pair:
                print(saved_pair,pair)
                self.pairs.remove(pair)
    


    def draw_edge(self):
        for e in self._objects_edges:
            e.draw()    


    

    def check_colission(self, x: int, y: int):
        result = []

        for e in self._objects:
            if e.check_collision(x, y):
                result.append(e)
        return result

"""  
    def error(self,vertex):
        for pair in self.pairs:
            if vertex in pair:
                answer = messagebox(
                        "Вы не можете видалити вершину",
                        "спочатку видаліть дугу між вершинами!",
                        info=True,
                        buttons=("Yes", "No"),
                        return_button=0,
                        escape_button=1,
                    )
                return False
            else: return True
            
            
 """