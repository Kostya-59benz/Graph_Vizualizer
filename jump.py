import pygame


SIZE = WIDTH, HEIGHT = 700, 700
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Graph-Vizualizer")

usr_wdh = 60

usr_hh = 100

usr_x = WIDTH //3
usr_y = HEIGHT - usr_hh - 100

make_jump = False

jump_cnt = 30


def main():
    global make_jump

    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = not running
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            make_jump = True
        
        if make_jump:
            jump()

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (247,240,22), (usr_x,usr_y, usr_wdh, usr_hh))

        clock.tick(60)
        pygame.display.update()
        
    pygame.quit()


def jump():
    global usr_y, jump_cnt, make_jump

    if jump_cnt >= -30:
        usr_y -= jump_cnt/2.5
        jump_cnt -= 1
        print(jump_cnt)
    else:
        jump_cnt = 30
        make_jump = False
    print(usr_y)

if __name__ == '__main__' :
    main()