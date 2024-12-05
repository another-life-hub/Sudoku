"""
Основной модуль. Решение судоку при вводе исходных данных с клавиатуры.
Демонстрационные примеры можно найти в файле "Примеры.txt".

Под переменными r, c, b, p, n всюду в основном и вспомогательном модулях подразумеваются
row(строка), column(столбец), block(блок), position(позиция в блоке), number(число в
ячейке). Под переменными rc, bp, rn, cn, bn подразумеваются различные представления матрицы
9x9 судоку (системы координат), которые реализованы как списки 9x9: 
представление строка-столбец, блок-позиция, строка-номер, столбец-номер, блок-номер.

Примеры вывода информации на экран и её интерпретация:
'r5c7=1' - заполнение ячейки в строке 5 и столбце 7 цифрой 1
'b3p4=5' - заполнение ячейки в блоке 3 и позиции 4 цифрой 5
'r4c6 -1' - удаление кандидата 1 из ячейки в строке 4 и столбце 6
"""

from inspect import getfullargspec
from re import fullmatch
from singles import singles
from intersections import intersections
from locked_sets import call_locked_set, call_hidden_set, call_fish
from single_digit_patterns import skyscraper, finned_x_wing, two_string_kite,\
     grouped_2string_kite, turbot_fish, empty_rectangle, dual_empty_rectangle
from wings import w_wing, xy_wing, xyz_wing
from sue_de_coq import almost_locked_pair

def print_sudoku(sud):
    """Вывод судоку с разбиением на строки, столбцы и блоки.
       sud - список 9x9"""
    for r in range(11):
        if r != 3 and r != 7:
            print_sud = ''
            for c in range(0, 9):
                print_sud +=  ' ' if c % 3 else '|'
                print_sud += str(sud[r - r//4][c])
            print(print_sud + '|')
        else:
            print('-' *19)

def rc_bp(r, c):
    """Преобразование координат (r, c) в (b, p) и наоборот"""
    return r//3 *3 + c//3, (r % 3)*3 + c % 3

# Перечисление всех реализованных методов решения
subsets = call_locked_set(2), call_locked_set(3), call_hidden_set(2),\
          call_locked_set(4), call_hidden_set(3), call_locked_set(5)
fish_ = call_fish(2), call_fish(3), call_fish(4)
one_digit_samples = skyscraper, two_string_kite, turbot_fish,\
                    empty_rectangle,grouped_2string_kite,dual_empty_rectangle,\
                    finned_x_wing
wings = w_wing, xy_wing, xyz_wing
methods = singles + (intersections,) + subsets + fish_ + one_digit_samples +\
          wings + (almost_locked_pair,)
NUM = len(methods)

# Задание начальных значений количества точек и заданных цифр
row_points = [0 for k in range(9)]
column_points = row_points[:] 
block_points = row_points[:]
row_values = [set() for k in range(9)]
column_values = [set() for k in range(9)]
block_values = [set() for k in range(9)]

# Запрос и проверка исходных данных
initial = input('Задайте исходные данные (примеры есть в файле Примеры.txt): ')
match = fullmatch(r'[:][0-9]{4}[:](.+?)[:](.+?)[:](.+?)[:](.+?)', initial)
if match: # проверка на формат HoDoKu
    sud, tail = match.group(2, 3)
    hodoku = True 
elif len(initial) == 81: # проверка на обычный формат судоку
    hodoku = False 
    sud = initial[:]
    rc = [sud[r*9: r*9 +9] for r in range(9)]
    print('\nИсходные данные: ')
    print_sudoku(rc) # вывод исходных данных в наглядном представлении
else:
    print('\nНеправильный формат данных.')
    exit()
pos = 0 # счётчик символов, отличных от '+'
plus = False # маркер присутствия '+' на предыдущей позиции
for symbol in sud:
    if symbol == '+' and not plus: # после '+' ожидается следующий символ
        plus = True
        continue
    r, c = pos//9, pos % 9
    b = r//3 *3 + c//3
    if 49 <= ord(symbol) <= 57: # число от 1 до 9
       row_values[r] |= {int(symbol)}
       column_values[c] |= {int(symbol)}
       block_values[b] |= {int(symbol)}
    elif symbol == '.' and not plus:
       row_points[r] += 1
       column_points[c] += 1
       block_points[b] += 1
    else:
       print('\nНеправильный символ в исходных данных.')
       exit()
    pos += 1
    plus = False
if pos != 81 or plus:
    print('\nНеправильный формат данных.')
    exit()

# Проверка на совпадение цифр
for k in range(9):
    if row_points[k] + len(row_values[k]) != 9\
       or column_points[k] + len(column_values[k]) != 9\
       or block_points[k] + len(block_values[k]) != 9:
        print('\nЗаданы одинаковые цифры в одном доме.')
        exit()

# Определение rc-матрицы
FULL_HOUSE = set(range(1, 10))
sud = sud.replace('+', '')
rc = [[0 for c in range(9)] for r in range(9)]
for pos in range(81):
    r, c = pos//9, pos % 9
    b = r//3 *3 + c//3
    if sud[pos] != '.':
        rc[r][c] = int(sud[pos])
        continue
    rc[r][c] = FULL_HOUSE - (row_values[r] | column_values[c] | block_values[b])
    if not rc[r][c]:
        print('\nСудоку не имеет решения.')
        exit()

# Пересчёт rc-матрицы в соответствии с форматом HoDoKu
if hodoku and tail:
    tail = tail.split(' ')
    for triple in tail:
        if len(triple) != 3:
            print('\nНеправильный формат данных.')
            exit()
        for digit in triple:
            if 57 < ord(digit) or ord(digit) < 49: # число от 1 до 9
                print('\nНеправильный формат данных.')
                exit()
        r, c = int(triple[1]) - 1, int(triple[2]) - 1
        if type(rc[r][c]) == int or not rc[r][c] - {int(triple[0])}:
            print('\nНеправильный формат данных.')
            exit()
        rc[r][c] -= {int(triple[0])}

# Определение bp-, rn-, cn- и bn-матрицы
bp = [[set() for p in range(9)] for b in range(9)]
rn = [[set() for n in range(9)] for r in range(9)]
cn = [[set() for n in range(9)] for c in range(9)]
bn = [[set() for n in range(9)] for b in range(9)]
for r in range(9):
    for c in range(9):
        b, p = rc_bp(r, c)
        bp[b][p] = rc[r][c]
        if type(rc[r][c]) == int: # в позиции(r,c) стоит цифра
            n = rc[r][c]
            rn[r][n - 1] = c + 1
            cn[c][n - 1] = r + 1
            bn[b][n - 1] = p + 1
        else: # в позиции (r,c) стоят кандидаты
            for n in rc[r][c]:
                rn[r][n - 1] |= {c + 1}
                cn[c][n - 1] |= {r + 1}
                bn[b][n - 1] |= {p + 1}
print()

# Основной цикл обработки
fail = False
while True:
    # Проверка заполнения всех строк
    r = 0
    while r < 9 and row_points[r] == 0: r += 1
    if r == 9: break # задача решена

    for method_num in range(NUM):
        m = methods[method_num]
        # Применение метода method_num со своими аргументами:
        res = m(*[globals()[arg] for arg in getfullargspec(m)[0]])
        if res: # метод method_num сработал
            break
    else: # ни один метод не сработал
        fail = True
        break
    if res[2] > 0: # метод method_num заполняет ячейку
        r, c, n = res
        b, p = rc_bp(r, c)
        row_points[r] -= 1    # уменьшение количества
        column_points[c] -= 1 # незаполненных значений в строках,
        block_points[b] -= 1  # столбцах и блоках
        for k in rc[r][c]:
            if k != n:
                rn[r][k - 1] -= {c + 1} # Удаление кандидатов из ячеек,
                cn[c][k - 1] -= {r + 1} # соответствующих rc[r][c]
                bn[b][k - 1] -= {p + 1} # в rn-, cn-, bn-матрицах
        # Заполнение ячеек в rc-, bp-, rn-, cn-, bn-матрицах
        rc[r][c], bp[b][p] = n, n
        rn[r][n - 1], cn[c][n - 1], bn[b][n - 1] = c + 1, r + 1, p + 1
        cells  = {(r, c_) for c_ in range(9)} # строка r
        cells |= {(r_, c) for r_ in range(9)} # столбец c
        cells |= {rc_bp(b, p_) for p_ in range(9)} # блок b
        for r_, c_ in cells - {(r, c)}:
            if type(rc[r_][c_]) == int:
                continue
            rc[r_][c_] -= {n} # удаление кандидата n из rc-матрицы
            if not rc[r_][c_]: # проверка на пустое множество
                print('\nСудоку не имеет решения.')
                exit()
            b_, p_ = rc_bp(r_, c_)
            bp[b_][p_] = rc[r_][c_]
            if type(rn[r_][n - 1]) == set: # Удаление кандидатов из ячеек,
                rn[r_][n - 1] -= {c_ + 1} # соответствующих cells
            if type(cn[c_][n - 1]) == set:# в bp-, rn-, cn-, bn-матрицах
                cn[c_][n - 1] -= {r_ + 1}
            if type(bn[b_][n - 1]) == set:
                bn[b_][n - 1] -= {p_ + 1}
    else: # метод method_num удаляет кандидаты
        for k in range(0, len(res), 3):
            r, c, n = res[k], res[k + 1], -res[k + 2]
            rc[r][c] -= {n} # удаление из rc-матрицы
            if not rc[r][c]: # проверка на пустое множество
                print('\nСудоку не имеет решения.')
                exit()
            # Удаление из bp-, rn-, cn-, bn-матрицы
            b, p = rc_bp(r, c)
            bp[b][p] = rc[r][c]
            rn[r][n - 1] -= {c + 1}
            cn[c][n - 1] -= {r + 1}
            bn[b][n - 1] -= {p + 1}

if not fail:
    print('\nЗадача решена:')
    print_sudoku(rc)
else:
    print('\nДанными методами решить задачу не удалось. Промежуточный результат:')
    for row in rc:
        print(row)
