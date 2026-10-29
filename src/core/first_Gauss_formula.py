import numpy as np

import matplotlib.pyplot as plt

from utils.output_rich import Rich


xi_mas = np.array([1.375, 1.380, 1.385, 1.390, 1.395])
yi_mas = np.array([5.04192, 5.17744, 5.32016, 5.47069, 5.62968])

xj_mas = np.array([1.350, 1.355, 1.360, 1.365, 1.370])

h = xi_mas[1] - xi_mas[0]

n = len(xi_mas)

def build_difference_table(y):
    """
    Строит таблицу конечных разностей.
    Возвращает матрицу, где столбец j - это разности j-го порядка.
    """
    table = np.zeros((n, n))
    table[:, 0] = y
    for j in range(1, n):      # Порядок разности
        for i in range(n - j): # Индекс узла
            table[i][j] = table[i+1][j-1] - table[i][j-1]
    return table


diff_table = build_difference_table(yi_mas)

cols = ["x_i", "y_i", "Δy", "Δ²y", "Δ³y", "Δ⁴y", "Δ⁵y"]
rows = []
for i in range(n):
    row = [f"{xi_mas[i]:.3f}", f"{diff_table[i][0]:.5f}"]
    for j in range(1, n):
        if i < n - j:
            row.append(f"{diff_table[i][j]:.5f}")
        else:
            row.append("") # Пустые ячейки для красивого треугольника
    rows.append(row)


def gauss_first_formula(x: float, x0: float, h: float, table):
    """
    Вычисляет значение полинома по первой формуле Гаусса (стр. 16 методички).
    Для экстраполяции влево в качестве x0 берем первый узел (индекс 0).
    """

    q = (x - x0) / h

    # Извлекаем нужные разности из первой строки таблицы
    y0 = table[0][0]
    dy0 = table[0][1]
    d2y_1 = table[0][2]
    d3y_1 = table[0][3]
    d4y_2 = table[0][4]
    d5y_2 = table[0][5] if n > 5 else 0.0

    term1 = y0
    term2 = q * dy0
    term3 = (q * (q - 1) / 2) * d2y_1
    term4 = ((q + 1) * q * (q - 1) / 6) * d3y_1
    term5 = ((q + 1) * q * (q - 1) * (q - 2) / 24) * d4y_2
    term6 = ((q + 2) * (q + 1) * q * (q - 1) * (q - 2) / 120) * d5y_2

    return term1 + term2 + term3 + term4 + term5 + term6


# Вывод результатов в таблицу
cols_res = ["x_j", "P_n(x_j)", "q"]
rows_res = []
gauss_results = []

x0 = xi_mas[0]  # Опорная точка - первый узел (так как мы экстраполируем влево)

for x in xj_mas:
    y_val = gauss_first_formula(x, x0, h, diff_table)
    gauss_results.append(y_val)
    q_val = (x - x0) / h
    rows_res.append([f"{x:.3f}", f"{y_val:.6f}", f"{q_val:.4f}"])
