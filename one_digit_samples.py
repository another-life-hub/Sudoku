from join_chain_ends import join_chain_ends, rc_bp 

def skyscraper(rn, cn):
    """Метод 'Небоскрёб'"""
    res = ()
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    for n in range(1, 10):
        for h in range(2): # 0/1 - случай направляющих строк/столбцов      
            if h == 0: m, pr = rn, 'строками'
            if h == 1: m, pr = cn, 'столбцами'        
            for i0 in range(9): # поиск двузначной ячейки
                s0 = m[i0][n - 1]
                if type(s0) == int or len(s0) != 2:
                    continue
                # поиск двузначной ячейки, у которой один общий кандидат с s0,
                # в остальной части столбца со следующего слоя
                for i1 in range((i0//3 + 1) *3, 9):
                    s1 = m[i1][n-1] # s1, s0 (sets) - содержимое двух ячеек
                    if type(s1) == int or len(s1) != 2 or len(s1 & s0) != 1\
                       or {(s1 ^ s0 <= layer) for layer in H_LAYERS} == {False}:
                        continue
                    v = list(s1 - s0)[0], list(s0 - s1)[0] # v (value)
                    i = i0, i1
                    # поиск удаляемых кандидатов в четырёх ячейках
                    for j in range(2):
                        for k in range(1, 3): 
                            i_ = i[j] + k - ((i[j] + k)//3 - i[j]//3) *3 
                            if type(m[i_][n-1])== int or not v[j] in m[i_][n-1]:
                                continue
                            if h == 0: res += i_, v[j] - 1, -n
                            if h == 1: res += v[j] - 1, i_, -n
                    if not res: # не найден ни один удаляемый кандидат
                        continue
                    p = f'Небоскрёб ({n}) с направляющими {pr} {i0+1} {i1+1}: '
                    print(p, end = '')
                    for k in range(0, len(res), 3):
                        print(f'r{res[k] + 1}c{res[k+1] + 1} {-n} ', end = '')
                    print()
                    return res

def finned_x_wing(rn, cn):
    """Поиск 2-решёток с браком"""
    res = ()
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    for n in range(1, 10):
        for h in range(2): # 0/1 - случай направляющих строк/столбцов
            if h == 0: m, pr1, pr2 = rn, 'строками', 'и столбцами'
            if h == 1: m, pr1, pr2 = cn, 'столбцами', 'и строками'        
            for i0 in range(9): # поиск двузначной ячейки в столбце
                s0 = m[i0][n - 1]
                if type(s0) == int or len(s0) != 2:
                    continue
                for i1 in range(9): # поиск второй ячейки в столбце
                    s1 = m[i1][n - 1] # s1, s0 (sets) - содержимое двух ячеек
                    if type(s1) == int or i1 in range(i0//3 *3, i0//3 *3 + 3):
                        continue # исключение слоя, где находится i0
                    for layer in H_LAYERS: # поиск слоя 
                        if s1 ^ s0 <= layer and len(s0 & layer) == 1: break
                    else:
                        continue # поиск следующей второй ячейки
                    v = list(s0 & layer)[0] # v (value)
                    # поиск удаляемых кандидатов в двух ячейках
                    for k in range(1, 3):
                        i = i1 + k - ((i1 + k)//3 - i1//3) *3
                        if type(m[i][n-1])== int or not v in m[i][n-1]:
                            continue
                        if h == 0: res += i, v-1, -n
                        if h == 1: res += v-1, i, -n
                    if not res: # не найден ни один удаляемый кандидат
                        continue
                    if h == 0: f = [f'r{i1 + 1}c{v_},' for v_ in s1-s0]
                    if h == 1: f = [f'r{v_}c{i1 + 1},' for v_ in s1-s0]
                    print(f'2-решётка ({n}) с браком', *f, 'направляющими',\
                          pr1, i0 + 1, i1 + 1, pr2, *s0, ': ', end = '')
                    for k in range(0, len(res), 3):
                        print(f'r{res[k] + 1}c{res[k+1] + 1} {-n} ', end = '')
                    print()
                    return res

def two_string_kite(rn, cn):
    """Реализация цепи со струнами в строке и столбце"""
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    for n in range(1, 10):
        for r0 in range(9): # поиск первой струны - двузначной ячейки в rn
            s0 = rn[r0][n - 1]
            if type(s0) == int or len(s0) != 2:
                continue
            for layer in H_LAYERS:
                if len(s0 & layer) != 1:
                    continue
                c0 = list(s0 - layer)[0] - 1 # (r0, c0) - I конец I струны
                ends = set() # множество возможных I концов II струны
                for k in range(1, 3):
                    r = r0 + k - ((r0 + k)//3 - r0//3) *3
                    if type(rn[r][n-1]) == int: continue
                    ends |= {(r, c-1) for c in (layer - s0) & rn[r][n-1]}
                for r, c in ends:
                    if len(cn[c][n-1]) != 2:
                        continue
                    # (r1, c) - II конец II струны
                    r1 = list(cn[c][n-1] - {r+1})[0] - 1
                    if type(rn[r1][n-1]) == int or c0 + 1 not in rn[r1][n-1]:
                        continue
                    print(f'Две струны ({n}) в строке {r0+1} и столбце {c+1}:',\
                          f'r{r1+1}c{c0+1} {-n}')
                    return r1, c0, -n             


def grouped_2string_kite(rn, cn):
    """Реализация цепи с групповыми струнами в строке и столбце"""
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    for n in range(1, 10):
        for r0 in range(9): # поиск первой групповой струны
            for l1 in H_LAYERS: # l1 - слой, в котором находится строка
                if r0 + 1 in l1: break                    
            s0 = rn[r0][n - 1]
            if type(s0) == int: continue
            for l2 in H_LAYERS: # l2 - слой, в котором находится столбец
                if len(s0 - l2) != 1: continue
                pr1 = 'с группой ' if len(s0 & l2) != 1 else '' 
                c0 = list(s0 - l2)[0] - 1 # (r0, c0) - I конец I струны
                for c in l2 - s0:
                    s1 = cn[c-1][n-1]
                    if type(s1) == int or len(s1) == 1 or\
                       len(s1 - (l1 - {r0 + 1})) != 1: continue
                    pr2 = 'с группой ' if len(s1 & l1) != 1 else '' 
                    # (r1, c-1) - II конец II струны
                    r1 = list(s1 - (l1 - {r0 + 1}))[0] - 1
                    if type(rn[r1][n-1]) == int or c0 + 1 not in rn[r1][n-1]:
                        continue
                    print(f'Струна {pr1}({n}) в строке {r0+1} ', end = '')
                    print(f'и струна {pr2}в столбце {c}: r{r1+1}c{c0+1} {-n}')
                    return r1, c0, -n

def turbot_fish(rc, rn, cn, bn):
    """Реализация цепи со струнами в блоке и строке/столбце"""
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    V_LAYERS = {1, 4, 7}, {2, 5, 8}, {3, 6, 9}
    for n in range(1, 10):
        for b0 in range(9): # поиск струны в блоке - двузначной ячейки в bn
            s0 = bn[b0][n - 1]
            if type(s0) == int or len(s0) != 2: continue
            for h in range(2): # 0/1 - поиск струны в строке/столбце
                if h == 0: layers, m, pr = V_LAYERS, rn, 'и строке' 
                if h == 1: layers, m, pr = H_LAYERS, cn, 'и столбце'
                for layer in layers:
                    if len(s0 & layer) != 1: continue
                    ends = set()
                    for k in range(1, 3):
                        if h == 0: b = (b0 + 3*k) %9
                        if h == 1: b = b0 + k - ((b0 + k)//3 - b0//3) *3
                        if type(bn[b][n-1]) == int: continue
                        ends |= {rc_bp(b, p-1) for p in layer & bn[b][n-1]}
                    for pos in ends:
                        if len(m[pos[h]][n-1]) != 2: continue
                        coord = list(m[pos[h]][n-1] - {pos[h-1] + 1})[0] - 1
                        pos0 = rc_bp(b0, list(s0 - layer)[0] - 1)
                        if h == 0: r, c = pos0[h], coord
                        if h == 1: r, c = coord, pos0[h]
                        if type(rc[r][c]) == int or n not in rc[r][c]\
                           or rc_bp(r, c)[0] == b0: continue
                        print(f'Две струны ({n}) в блоке {b0 +1}',\
                              f'{pr} {pos[h] +1}: r{r+1}c{c+1} {-n}')
                        return r, c, -n                         
           
def empty_rectangle(rc, rn, cn, bn):
    """Реализация цепи с линейной связью в блоке 
       и струной в строке или столбце"""
    H_LAYERS = frozenset((1,2,3)), frozenset((4,5,6)), frozenset((7,8,9))
    V_LAYERS = frozenset((1,4,7)), frozenset((2,5,8)), frozenset((3,6,9))
    pairs = {(s1, s2) for s1 in V_LAYERS for s2 in H_LAYERS}
    for n in range(1, 10):
        for b0 in range(9):
            s0 = bn[b0][n - 1]
            if type(s0) == int or len(s0) == 2: # для двузначной ячейки 
                continue                      # работает метод 'Струна в блоке' 
            for pair in pairs:
                if s0 <= pair[0] | pair[1]: # найдены слои, в которых находятся
                    break                   # кандидаты цифры n в блоке b0
            else: continue
            for h in range(2): # 0/1 - поиск струны в строке/столбце
                if h == 0: m, pr = rn, 'в строке'
                if h == 1: m, pr = cn, 'в столбце'
                ends = set() # множество возможных I концов струны в стр./столб.
                for k in range(1, 3):
                    if h == 0: b = (b0 + 3*k) %9 
                    if h == 1: b = b0 + k - ((b0 + k)//3 - b0//3) *3
                    if type(bn[b][n-1]) == int: continue
                    ends |= {rc_bp(b, p-1) for p in pair[h] & bn[b][n-1]}
                for pos in ends:
                    if len(m[pos[h]][n-1]) != 2: continue
                    coord = list(m[pos[h]][n-1] - {pos[h-1] + 1})[0] - 1
                    pos0 = rc_bp(b0, list(pair[h-1])[0] - 1)
                    if h == 0: r, c = pos0[h], coord
                    if h == 1: r, c = coord, pos0[h]                    
                    if type(rc[r][c]) == int or n not in rc[r][c]\
                       or rc_bp(r, c)[0] == b0:
                        continue
                    print(f'Линейная связь ({n}) в блоке {b0 +1} и струна',\
                          f'{pr} {pos[h] +1}: r{r+1}c{c+1} {-n}')
                    return r, c, -n              

def dual_empty_rectangle(rc, rn, cn, bn):
    """Реализация цепи с линейной связью в блоке
       и двумя струнами в строке и столбце"""
    H_LAYERS = frozenset((1,2,3)), frozenset((4,5,6)), frozenset((7,8,9))
    V_LAYERS = frozenset((1,4,7)), frozenset((2,5,8)), frozenset((3,6,9))
    pairs = {(s1, s2) for s1 in V_LAYERS for s2 in H_LAYERS}
    res = ()
    for n in range(1, 10):
        for b0 in range(9):
            s0 = bn[b0][n - 1]
            if type(s0) == int or len(s0) == 2: continue
            for pair in pairs:
                if s0 <= pair[0] | pair[1]: # найдены слои, в которых находятся
                    break                   # кандидаты цифры n в блоке b0
            else: continue
            for h in range(2): # 0/1 - поиск струны в строке/столбце
                if h == 0: m, ends2_r = rn, set()
                if h == 1: m, ends2_c = cn, set()
                # ends2_r/c - множество возможных II концов струны в стр./столб.
                ends1 = set()# множество возможных I концов струны в стр./столб.
                for k in range(1, 3):
                    if h == 0: b = (b0 + 3*k) %9
                    if h == 1: b = b0 + k - ((b0 + k)//3 - b0//3) *3
                    if type(bn[b][n-1]) == int: continue
                    ends1 |= {rc_bp(b, p-1) for p in pair[h] & bn[b][n-1]}
                for pos in ends1:
                    if len(m[pos[h]][n-1]) != 2: continue
                    coord = list(m[pos[h]][n-1] - {pos[h-1] + 1})[0] - 1
                    if h == 0: ends2_r |= {(pos[h], coord)}
                    if h == 1: ends2_c |= {(coord, pos[h])}
            # Соединение концов цепи  
            for r1, c1 in ends2_r:
                for r2, c2 in ends2_c:
                    if r1 == r2 and c1 == c2:# ячейка r1,c1 заполняется цифрой n
                        res, pr = (r1, c1, n), ''
                    elif rc_bp(r1,c1)[0] == rc_bp(r2,c2)[0]:#концы в одном блоке
                        # случай замкнутой цепи                        
                        b1,p1,p2=rc_bp(r1,c1)[0],rc_bp(r1,c1)[1],rc_bp(r2,c2)[1]
                        for p in bn[b1][n-1]: # удаление из блока b1
                            if p-1 != p1 and p-1 != p2:  
                                res += *rc_bp(b1, p-1), -n                                 
                        r0 = rc_bp(b0, list(pair[1])[0] - 1)[0] 
                        for c in rn[r0][n-1]: # удаление из строки r0
                            if c-1 !=c2 and c-1 not in range(b0%3 *3,b0%3 *3 +3):                               
                                res += r0, c-1, -n 
                        c0 = rc_bp(b0, list(pair[0])[0] - 1)[1]
                        for r in cn[c0][n-1]: # удаление из столбца c0
                            if r-1!=r1 and r-1 not in range(b0//3*3,b0//3*3 +3):   
                                res+= r-1, c0, -n
                        pr = ' (замкнутая цепь)'
                    else: # концы не лежат в одном блоке
                        res, pr = join_chain_ends(rc, r1, c1, r2, c2, n), ''
                    if not res: continue # не найден ни один удаляемый кандидат
                    print(f'Линейная связь ({n}) в блоке {b0 +1}, струны',\
                          f'в строке {r1+1} и столбце {c2+1}{pr}: ', end = '')
                    for k in range(0, len(res), 3):
                        print(f'r{res[k]+1}c{res[k+1]+1} {res[k+2]} ', end = '')
                    print()
                    return res                   
