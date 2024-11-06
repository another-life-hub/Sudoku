def rc_bp(r, c):
    """Преобразование координат (r, c) в (b, p) и наоборот"""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

def full_house(block_points, row_points, column_points, rc, bp):
    """Метод 'Заполнение дома'"""
    for b in range(9):
        if block_points[b] == 1: # в блоке b проставлено 8 цифр
            for p in range(9):
                if type(bp[b][p]) == set:
                    n = list(bp[b][p])[0]
                    print(f'Заполнение блока {b + 1}: b{b + 1}p{p + 1}={n}')
                    return *rc_bp(b,p), n
    for r in range(9):
        if row_points[r] == 1: # в строке r проставлено 8 цифр
            for c in range(9):
                if type(rc[r][c]) == set:
                    n = list(rc[r][c])[0]
                    print(f'Заполнение строки {r + 1}: r{r + 1}c{c + 1}={n}')
                    return r, c, n
    for c in range(9):
        if column_points[c] == 1: # в столбце c проставлено 8 цифр
            for r in range(9):
                if type(rc[r][c]) == set:
                    n = list(rc[r][c])[0]
                    print(f'Заполнение столбца {c + 1}: r{r + 1}c{c + 1}={n}')
                    return r, c, n

def hidden_single(rn, cn, bn):
    """Поиск скрытых одиночек"""
    for n in range(1, 10):
        for b in range(9): # поиск по блокам
            if type(bn[b][n - 1]) == set and len(bn[b][n - 1]) == 1:
                p = list(bn[b][n - 1])[0]
                print(f'Скрытая одиночка {n} в блоке {b + 1}: b{b + 1}p{p}={n}')
                return *rc_bp(b, p - 1), n
        for r in range(9): # поиск по строкам
            if type(rn[r][n - 1]) == set and len(rn[r][n - 1]) == 1:
                c = list(rn[r][n - 1])[0]
                print(f'Скрытая одиночка {n} в строке {r + 1}: r{r + 1}c{c}={n}')
                return r, c - 1, n
        for c in range(9): # поиск по столбцам
            if type(cn[c][n - 1]) == set and len(cn[c][n - 1]) == 1:
                r = list(cn[c][n - 1])[0]
                print(f'Скрытая одиночка {n} в столбце {c + 1}: r{r}c{c + 1}={n}')
                return r - 1, c, n

def naked_single(rc):
    """Поиск одиночек в ячейках"""
    for r in range(9):
        for c in range(9):
            if type(rc[r][c]) == set and len(rc[r][c]) == 1:
                n = list(rc[r][c])[0] 
                print(f'Одиночка в ячейке: r{r + 1}c{c + 1}={n}')
                return r, c, n      
    
singles = full_house, hidden_single, naked_single
