def rc_bp(r, c):
    """Преобразование координат (r, c) в (b, p) и наоборот"""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

def intersections(rn, cn, bn):
    """Метод 'Locked Candidates' (пересечение блока и строки/столбца)
       count = 0/1 - блок&строка/столбец, метод 'Pointing'
       count = 2/3 - блок&строка/столбец, метод 'Claiming'"""
    H_LAYERS = {1, 2, 3}, {4, 5, 6}, {7, 8, 9}
    V_LAYERS = {1, 4, 7}, {2, 5, 8}, {3, 6, 9}
    res = ()
    for n in range(1, 10):
        for count in range(4): 
            for h in range(9): # h (house) - блок, строка или столбец
                if count == 0: layers, m = H_LAYERS, bn # m - matrix
                if count == 1: layers, m = V_LAYERS, bn
                if count == 2: layers, m = H_LAYERS, rn
                if count == 3: layers, m = H_LAYERS, cn
                for l in layers: # l (layer) - блок&строка/столбец в bn/rn/cn
                    if type(m[h][n - 1]) == int or not m[h][n - 1] <= l:
                        continue                                 
                    for k in range(1, 3): # поиск дома h_ с удалением кандидатов
                        h_=(h+3*k)%9 if count == 1 else h+k-((h+k)//3 - h//3)*3 
                        if type(m[h_][n - 1]) == int or not m[h_][n - 1] & l:
                            continue
                        for v in m[h_][n - 1] & l:
                            if count == 2: res += h_, v - 1, -n
                            if count == 3: res += v - 1, h_, -n
                            if count == 1 or count == 0: res +=\
                              *rc_bp(h_,v - 1), -n
                if not res: # не найден ни один удаляемый кандидат
                    continue
                if count == 0: pr=f'{h+1} и строки {(h_//3)*3 + (v-1)//3 + 1}: '                    
                if count == 1: pr=f'{h+1} и столбца {(h_% 3)*3 + (v-1)%3 + 1}: '
                if count == 2: pr=f'{h_//3*3 + (v-1)//3 + 1} и строки {h + 1}: '
                if count == 3: pr=f'{(v-1)//3*3 + h_//3 + 1} и столбца {h +1}: '
                print(f'Пересечение ({n}) блока', pr, end = '')
                for k in range(0, len(res), 3):
                    print(f'r{res[k] +1}c{res[k+1] +1} {res[k+2]} ',end = '')
                print()
                return res    
