import pygame


SIZE = WIDTH, HEIGHT = 700, 700

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Tree Vizualizer")

BLACK = (0, 0, 0)
GRAY = (150, 150, 150)


def near(p, center, radius):
    d2 = (p[0] - center[0])**2 + (p[1] - center[1])**2
    return d2 <= radius**2


class Node:
    def __init__(self, x, y, radius, color) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.__left = self.__right = None

        print(f'pos : {self.x},{self.y}')

    def getPos(self):
        return (self.x, self.y)

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    @left.setter
    def left(self, left):
        self.__left = left

    @right.setter
    def right(self, right):
        self.__right = right

    def getRadius(self):
        return self.radius

    def getColor(self):
        return self.color


def create_nodes(width, lvls):
    nodes = []
    final_total = 2 ** (lvls - 1)
    diametr = (width // final_total) / 2
    radius = diametr / 2
    val = 2
    for lvl in range(lvls):
        total_lvl = 2 ** lvl
        start = (width // total_lvl) / val
        print(f'start: {start}')
        for node in range(total_lvl):
            print(f'node : {node}')
            nodes.append(Node(start + ((width//total_lvl) * node), (width//lvls/2)
                         * lvl + (width // lvls / 2), radius, BLACK))

    for i in range(len(nodes)+2):
        if 2 * i + 1 < len(nodes) and nodes[2*i+1]:
            nodes[i].left = nodes[2*i+1]
        if 2 * i + 2 < len(nodes) and nodes[2*i+2]:
            nodes[i].right = nodes[2*i+2]

    return nodes


def draw_lines(screen, nodes):
    for node in nodes:
        if node.left != None and node.right != None:
            pygame.draw.line(screen, BLACK, node.getPos(),
                             node.left.getPos(), 5)
            pygame.draw.line(screen, BLACK, node.getPos(),
                             node.right.getPos(), 5)


def draw_circles(screen, width, lvls, nodes):
    for node in nodes:
        pygame.draw.circle(screen, node.getColor(),
                           node.getPos(), node.getRadius())


def draw(screen, width, lvls, nodes):
    draw_circles(screen, width, lvls, nodes)
    draw_lines(screen, nodes)


def main(screen, width):
    pygame.init()
    lvls = 4
    nodes = create_nodes(width, lvls)
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = not running

        screen.fill(GRAY)
        # nodes.draw(screen)

        draw(screen, width, lvls, nodes)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main(screen, WIDTH)
