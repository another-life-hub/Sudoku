"""Вспомогательные функции для модулей 'one_digit_samples', 'wings'."""

def rc_bp(r, c):
    """Преобразование координат (r, c) в (b, p) и наоборот"""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

def join_chain_ends(rc, r1, c1, r2, c2, n):
    """Поиск всех удаляемых кандидатов для концов цепи (r1,c1,n) и (r2,c2,n)"""
    assert isinstance(rc[r1][c1], set) and isinstance(rc[r2][c2], set)\
           and n in rc[r1][c1] and n in rc[r2][c2]
    # Концы не лежат в одном доме - исключаем случай замкнутой цепи.
    assert rc_bp(r1, c1)[0] != rc_bp(r2, c2)[0] and r1 != r2 and c1 != c2
    ends = (r1, c1), (r2, c2)
    for h in range(2): # 0/1 - концы лежат в одном верт./гориз. слое
        if ends[0][h]//3 == ends[1][h]//3:
            pos = set()
            for i in range(2): # номер конца
                for coord in range(ends[i][h-1]//3 *3, ends[i][h-1]//3 *3 + 3):
                    if h == 0: pos |= {(ends[i-1][h], coord)}
                    if h == 1: pos |= {(coord, ends[i-1][h])}
            break
    else: # концы не лежат ни в одном слое
        pos = {(r1, c2), (r2, c1)}
    res = ()
    for r, c in pos:
        if isinstance(rc[r][c], int) or n not in rc[r][c]: continue
        res += r, c, -n
    return res     
