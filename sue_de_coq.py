def rc_bp(r, c):
    """Преобразование координат (r, c) в (b, p) и наоборот"""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

def almost_locked_pair(rc, bp, rn, cn, bn):
    """Реализация частного случая метода 'Sue de Coq'."""
    res = ()
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    V_LAYERS = {1, 4, 7}, {2, 5, 8}, {3, 6, 9}
    for pos0 in range(81): # поиск двузначной ячейки
        r0, c0 = pos0 //9, pos0 %9
        b0, p0 = rc_bp(r0, c0)
        if type(rc[r0][c0]) == int or len(rc[r0][c0]) != 2: continue
        n1, n2 = tuple(rc[r0][c0])
        for h in range(4):# 0/1 - блок&строка/столбец; 2/3 - строка/столбец&блок
            layers = H_LAYERS
            if h == 0: m1, m2, x0, y0, pr1 = rn, rc, r0, c0, 'в блоке'
            if h == 1:
                m1, x0, y0, pr1 = cn, c0, r0, 'в блоке'
                m2 = [[rc[i][j] for i in range(9)] for j in range(9)]
            if h == 2: m1, m2, x0, y0, pr1 = bn, bp, b0, p0, 'в строке'
            if h == 3: m1, m2, x0, y0, pr1, layers =\
               bn, bp, b0, p0, 'в столбце', V_LAYERS
            for l in layers:
                if y0 +1 in l: break
            for k in range(1, 3): # перебор двух строк/столбцов/блоков                
                x1 = (x0 + 3*k)%9 if h==3 else x0 + k -((x0 + k)//3 - x0 //3)*3 
                if type(m1[x1][n1-1]) == int or type(m1[x1][n2-1]) == int or\
                 len(m1[x1][n1-1] - l)!=1 or m1[x1][n1-1] -l != m1[x1][n2-1] -l:
                    continue
                y1 = list(m1[x1][n1-1] - l)[0] - 1
                if h == 0: r1, c1, pr2, pr3 = x1, y1, b0+1, 'и строке'
                if h == 1: r1, c1, pr2, pr3 = y1, x1, b0+1, 'и столбце'
                if h == 2: r1, c1, pr2, pr3 = *rc_bp(x1, y1), r0+1,'и блоке'
                if h == 3: r1, c1, pr2, pr3 = *rc_bp(x1, y1), c0+1,'и блоке'
                for n in m2[x1][y1] - m2[x0][y0]:             
                    res += r1, c1, -n
                for k_ in range(1, 3):
                    x2 =(x1 + 3*k_)%9 if h==3 else x1+k_-((x1 +k_)//3 - x1//3)*3
                    for y2 in l:
                        if (x2, y2 -1) == (x0, y0): continue
                        for n in m2[x0][y0]:
                            if type(m2[x2][y2 -1])==set and n in m2[x2][y2 -1]:
                                if h == 0: res += x2, y2 -1, -n
                                if h == 1: res += y2 -1, x2, -n
                                if h == 2: res += *rc_bp(x2, y2 -1), -n
                                if h == 3: res += *rc_bp(x2, y2 -1), -n
                if not res: continue
                print(f'Почти замкнутая пара {n1} {n2} {pr1} {pr2}',\
                      f'{pr3} {x1+1} (r{r1+1}c{c1+1}): ', end = '')
                for k in range(0, len(res), 3):
                    print(f'r{res[k] +1}c{res[k+1] +1} {res[k+2]} ',end = '')
                print()
                return res
