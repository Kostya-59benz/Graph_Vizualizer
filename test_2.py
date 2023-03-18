




def count_holes(path:str) -> int:
    up = count = 0

   
    for move in path:
        if move == 'U':
            up +=1

        if move == 'D':
            up -=1

        if up == 0 and move == 'U':
            count +=1

    return count


assert count_holes('UUDDU') == 3




