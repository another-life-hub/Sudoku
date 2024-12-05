"""Реализация методов, связанных с поиском одиночек (singles)."""

def rc_bp(r, c):
    """Вспомогательная функция, 
    преобразование координат (r, c) в (b, p) и наоборот."""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

def full_house(block_points, row_points, column_points, rc, bp):
    """Метод 'Заполнение дома' (full house)."""
    for b in range(9):
        if block_points[b] == 1: # в блоке b проставлено 8 цифр
            for p in range(9):
                if isinstance(bp[b][p], set):
                    for n in bp[b][p]: pass
                    print(f'Заполнение блока {b + 1}: b{b + 1}p{p + 1}={n}')
                    return *rc_bp(b,p), n
    for r in range(9):
        if row_points[r] == 1: # в строке r проставлено 8 цифр
            for c in range(9):
                if isinstance(rc[r][c], set):
                    for n in rc[r][c]: pass
                    print(f'Заполнение строки {r + 1}: r{r + 1}c{c + 1}={n}')
                    return r, c, n
    for c in range(9):
        if column_points[c] == 1: # в столбце c проставлено 8 цифр
            for r in range(9):
                if isinstance(rc[r][c], set):
                    for n in rc[r][c]: pass
                    print(f'Заполнение столбца {c + 1}: r{r + 1}c{c + 1}={n}')
                    return r, c, n

def hidden_single(rn, cn, bn):
    """Поиск скрытых одиночек (hidden single)."""
    for n in range(1, 10):
        for b in range(9): # поиск по блокам
            cell = bn[b][n - 1]
            if isinstance(cell, set) and len(cell) == 1:
                for p in cell: pass
                print(f'Скрытая одиночка {n} в блоке {b + 1}: b{b + 1}p{p}={n}')
                return *rc_bp(b, p - 1), n
        for r in range(9): # поиск по строкам
            cell = rn[r][n - 1]
            if isinstance(cell, set) and len(cell) == 1:
                for c in cell: pass
                print(f'Скрытая одиночка {n} в строке {r + 1}: r{r + 1}c{c}={n}')
                return r, c - 1, n
        for c in range(9): # поиск по столбцам
            cell = cn[c][n - 1]
            if isinstance(cell, set) and len(cell) == 1:
                for r in cell: pass
                print(f'Скрытая одиночка {n} в столбце {c + 1}: r{r}c{c + 1}={n}')
                return r - 1, c, n

def naked_single(rc):
    """Поиск одиночек в ячейках (naked single)."""
    for r in range(9):
        for c in range(9):
            cell = rc[r][c]
            if isinstance(cell, set) and len(cell) == 1:
                for n in cell: pass 
                print(f'Одиночка в ячейке: r{r + 1}c{c + 1}={n}')
                return r, c, n      
    
singles = full_house, hidden_single, naked_single
