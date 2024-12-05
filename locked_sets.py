"""Поиск замкнутых множеств (naked subsets), 
   скрытых множеств (hidden subsets) и решёток без брака (fish)."""

from itertools import product

def rc_bp(r, c):
    """Вспомогательная функция,
    преобразование координат (r, c) в (b, p) и наоборот."""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

def universal_locked_set(dim, m):
    """Вспомогательная функция,
    поиск замкнутых множеств размерности dim >=2 в строках матрицы m."""
    res = ()
    for i0, j0 in product(range(9), repeat=2): # начало поиска замкнутого множества
                                               # с ячейки (i0, j0)
        if isinstance(m[i0][j0], int) or len(m[i0][j0]) > dim: 
            continue
        pos, cand = [], []
        pos.append(j0)
        cand.append(m[i0][j0])
        start = j0 # стартовая позиция для поиска новой ячейки
        while 0 < len(pos) < dim: # поиск следующей ячейки
            for j in range(start + 1, 9):
                if isinstance(m[i0][j], set) and len(m[i0][j] | cand[-1]) <= dim:
                    cand.append(m[i0][j] | cand[-1])
                    pos.append(j) # создание новой ячейки и 
                    start = j     # переход к поиску следующей ячейки
                    break
            else:
                start = pos.pop() # удаление последней ячейки и 
                del cand[-1]      # возврат к поиску предыдущей ячейки
        if not pos:  # множество не найдено
            continue # переход к новой ячейке (i0, j0)
        # поиск удаляемых кандидатов
        for j, v in product(range(9), cand[-1]):
            if j not in pos and isinstance(m[i0][j], set) and v in m[i0][j]:
                res += j, v
        if not res: # не найден ни один удаляемый кандидат
            continue
        return i0, res, pos, cand[-1]

def call_locked_set(dim):
    def locked_set(rc, bp):
        """Вывод на экран результата поиска замкнутых множеств (naked subsets)
           размерности dim >=2 и передача данных основному модулю."""
        if dim == 2: pr1 = 'пара'
        if dim == 3: pr1 = 'тройка'
        if dim == 4: pr1 = 'четвёрка'
        if dim == 5: pr1 = 'пятёрка'
        res = ()
        for h in range(3): # h - блок, строка или столбец
            if h == 0: m, pr2 = bp, 'в блоке'
            if h == 1: m, pr2 = rc, 'в строке'
            if h == 2: m, pr2=[[rc[r][c] for r in range(9)] for c in range(9)],\
                                'в столбце'
            info = universal_locked_set(dim, m)
            if not info:
                continue
            res_, cand = info[1], info[3]            
            print('Замкнутая', pr1, *cand, pr2, info[0] + 1,': ', end = '')
            for k in range(0, len(res_), 2):
                if h == 0: r, c = rc_bp(info[0], res_[k]) 
                if h == 1: r, c = info[0], res_[k]
                if h == 2: r, c = res_[k], info[0]
                res += r, c, -res_[k + 1]
                print(f'r{r + 1}c{c + 1} {-res_[k + 1]} ', end = '')
            print()
            return res 
    return locked_set       

def call_hidden_set(dim):
    def hidden_set(rn, cn, bn):
        """Вывод на экран результата поиска скрытых множеств (hidden subsets)
           размерности dim >=2 и передача данных основному модулю."""
        if dim == 2: pr1 = 'пара'
        if dim == 3: pr1 = 'тройка'
        if dim == 4: pr1 = 'четвёрка'
        res = ()
        for h in range(3): # h - блок, строка или столбец
            if h == 0: m, pr2 = bn, 'в блоке'
            if h == 1: m, pr2 = rn, 'в строке'
            if h == 2: m, pr2 = cn, 'в столбце'
            info = universal_locked_set(dim, m)
            if not info:
                continue
            res_ = info[1]
            cand = [n + 1 for n in info[2]]
            print('Скрытая', pr1, *cand, pr2, info[0] + 1, ': ', end = '')
            for k in range(0, len(res_), 2):
                if h == 0: r, c = rc_bp(info[0], res_[k + 1] - 1)
                if h == 1: r, c = info[0], res_[k + 1] - 1
                if h == 2: r, c = res_[k + 1] - 1, info[0]
                res += r, c, -res_[k] - 1
                print(f'r{r + 1}c{c + 1} {-res_[k] - 1} ', end = '')
            print()
            return res
    return hidden_set

def call_fish(dim):
    def fish(rn, cn):
        """Вывод на экран результата поиска решёток без брака (fish)
           размерности dim >=2 и передача данных основному модулю."""
        res = ()
        for h in range(2): # 0/1 - направляющие строки/столбцы
            if h == 0:
                m = [[rn[r][n] for r in range(9)] for n in range(9)]
                pr1, pr2 = 'строками', 'и столбцами'
            else:
                m = [[cn[c][n] for c in range(9)] for n in range(9)]
                pr1, pr2 = 'столбцами', ' и строками'
            info = universal_locked_set(dim, m)
            if not info:
                continue
            res_ = info[1]
            primary = [j + 1 for j in info[2]]
            print(f'{dim}-решётка ({info[0] + 1}) с направляющими', pr1,\
                  *primary, pr2, *info[3], ': ', end = '')
            for k in range(0, len(res_), 2):
                if h == 0: r, c = res_[k], res_[k + 1] - 1
                if h == 1: r, c = res_[k + 1] - 1, res_[k]
                res += r, c, -info[0] - 1
                print(f'r{r + 1}c{c + 1} {-info[0] - 1} ', end = '')
            print()
            return res
    return fish    
