"""Реализация некоторых простых цепей (wings)."""

from join_chain_ends import join_chain_ends, rc_bp

def w_wing(rc, rn, cn, bn):
    """Реализация цепи с парой (x y) в двух ячейках и связующей струной (w-wing)."""
    for pos1 in range(81): # поиск первой двузначной ячейки
        r1, c1 = pos1 //9, pos1 %9 
        b1 = rc_bp(r1, c1)[0] 
        if type(rc[r1][c1]) == int or len(rc[r1][c1]) != 2: continue
        for pos2 in range(pos1, 81):    # поиск ячейки с таким же 
            r2, c2 = pos2 //9, pos2 %9  # множеством кандидатов 
            b2 = rc_bp(r2, c2)[0]
            if r1 == r2 or c1 == c2 or b1 == b2 or rc[r1][c1] != rc[r2][c2]:
                continue # ячейки не должны быть в одном доме
            for n_ in rc[r1][c1]: # n_ - цифра, которая удаляется
                res = join_chain_ends(rc, r1, c1, r2, c2, n_)
                if not res: continue # нет смысла искать связующую струну
                n = list(rc[r1][c1] - {n_})[0] # связующая цифра
                # e1/e2 - множество возможных I/II концов струны
                e1 = ({(r1, c-1) for c in rn[r1][n-1]} |\
                     {(r-1, c1) for r in cn[c1][n-1]} |\
                     {rc_bp(b1, p-1) for p in bn[b1][n-1]}) - {(r1, c1)}                
                e2 = ({(r2, c-1) for c in rn[r2][n-1]} |\
                     {(r-1, c2) for r in cn[c2][n-1]} |\
                     {rc_bp(b2, p-1) for p in bn[b2][n-1]}) - {(r2, c2)}                
                for r, c in e1:
                    b, p = rc_bp(r,c)
                    if len(rn[r][n-1]) == 2 and\
                       (r, list(rn[r][n-1] - {c+1})[0] -1) in e2:
                        pr, v = 'в строке', r+1
                    elif len(cn[c][n-1]) == 2 and\
                       (list(cn[c][n-1] - {r+1})[0] -1, c) in e2:
                        pr, v = 'в столбце', c+1             
                    elif len(bn[b][n-1]) == 2 and\
                       rc_bp(b, list(bn[b][n-1] - {p+1})[0] -1) in e2:
                        pr, v = 'в блоке', b+1
                    else: continue                    
                    print(f'Пара {n_} {n} в r{r1+1}c{c1+1} ', end = '')
                    print(f'r{r2+1}c{c2+1}, струна ({n}) {pr} {v}: ', end = '')
                    for k in range(0, len(res), 3):
                        print(f'r{res[k]+1}c{res[k+1]+1} {res[k+2]} ', end = '')
                    print()
                    return res

def xy_wing(rc, rn, cn, bn):
    """Метод 'Ножницы'. Реализация цепи с тремя двузначными ячейками (xy-wing)."""
    for pos1 in range(81): # поиск первой двузначной ячейки
        r1, c1 = pos1 //9, pos1 %9
        b1 = rc_bp(r1, c1)[0]
        if type(rc[r1][c1]) == int or len(rc[r1][c1]) != 2: continue
        for pos2 in range(pos1, 81):   # поиск двузначной ячейки, которая 
            r2, c2 = pos2 //9, pos2 %9 # имеет один общий кандидат с r1, c1
            b2 = rc_bp(r2, c2)[0]      # и не находится с ней в одном доме 
            if r1==r2 or c1==c2 or b1==b2 or type(rc[r2][c2]) == int or\
                len(rc[r2][c2])!=2 or len(rc[r1][c1] & rc[r2][c2])!=1: continue
            x = list(rc[r1][c1] & rc[r2][c2])[0] # x - цифра, которая удаляется
            res = join_chain_ends(rc, r1, c1, r2, c2, x)
            if not res: continue # нет смысла строить цепь
            # y, z - связующие цифры
            y, z = list(rc[r1][c1] - {x})[0], list(rc[r2][c2] - {x})[0]
            # e1/e2 - множество ячеек, связанных с I/II ячейкой
            e1 = ({(r1, c-1) for c in rn[r1][y-1]} |\
                  {(r-1, c1) for r in cn[c1][y-1]} |\
                  {rc_bp(b1, p-1) for p in bn[b1][y-1]}) - {(r1, c1)}
            e2 = ({(r2, c-1) for c in rn[r2][z-1]} |\
                  {(r-1, c2) for r in cn[c2][z-1]} |\
                  {rc_bp(b2, p-1) for p in bn[b2][z-1]}) - {(r2, c2)}
            for r, c in e1:
                if len(rc[r][c]) != 2 or (r, c) not in e2: continue
                print(f'Ножницы ({x}) с концами r{r1+1}c{c1+1} ', end = '')
                print(f'r{r2+1}c{c2+1} и центром r{r+1}c{c+1}: ', end = '')
                for k in range(0, len(res), 3):
                    print(f'r{res[k]+1}c{res[k+1]+1} {res[k+2]} ', end = '')
                print()
                return res

def xyz_wing(rc):
    """Метод 'Ножницы с браком'. Реализация структуры с двумя двузначными
       и одной трёхзначной ячейкой (xyz-wing)."""
    for pos1 in range(81): # поиск первой двузначной ячейки
        r1, c1 = pos1 //9, pos1 %9
        b1 = rc_bp(r1, c1)[0]
        if type(rc[r1][c1]) == int or len(rc[r1][c1]) != 2: continue
        for pos2 in range(pos1, 81):   # поиск двузначной ячейки, которая
            r2, c2 = pos2 //9, pos2 %9 # имеет один общий кандидат с r1, c1
            b2 = rc_bp(r2, c2)[0]      # и не находится с ней в одном доме
            if r1==r2 or c1==c2 or b1==b2 or type(rc[r2][c2]) == int or\
               len(rc[r2][c2])!=2 or len(rc[r1][c1] & rc[r2][c2])!=1: continue            
            ends = (r1, c1), (r2, c2)
            for h in range(2): # 0/1 - концы лежат в одном верт./гориз. слое
                if ends[0][h]//3 == ends[1][h]//3:
                    break
            else: continue # концы не лежат ни в одном слое
            for i in range(2): # номер конца
                s_ = range(ends[i][h-1]//3 *3, ends[i][h-1]//3 *3 + 3)
                if h == 0: s1 = {(ends[i-1][h], coord) for coord in s_}
                if h == 1: s1 = {(coord, ends[i-1][h]) for coord in s_}
                for r, c in s1:# s1 - три ячейки в одном блоке с одним из концов
                    if rc[r][c]==rc[r1][c1] | rc[r2][c2]: # найдена ячейка xyz
                        s2 = s1 - {(r, c)}
                        break
                else: continue
                break
            else: continue
            res = ()
            x = list(rc[r1][c1] & rc[r2][c2])[0] # x - цифра, которая удаляется
            for r_, c_ in s2:
                if type(rc[r_][c_]) == int or x not in rc[r_][c_]: continue
                res += r_, c_, -x
            if not res: continue
            print(f'Ножницы ({x}) с браком r{r+1}c{c+1} и концами ', end = '')
            print(f'r{r1+1}c{c1+1} r{r2+1}c{c2+1}: ', end = '')
            for k in range(0, len(res), 3):
                print(f'r{res[k]+1}c{res[k+1]+1} {res[k+2]} ', end = '')
            print()
            return res
