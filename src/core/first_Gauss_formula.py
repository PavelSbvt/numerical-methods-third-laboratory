import numpy as np

import matplotlib.pyplot as plt

from utils.output_rich import Rich


xi_mas = np.array([1.375, 1.380, 1.385, 1.390, 1.395])
yi_mas = np.array([5.04192, 5.17744, 5.32016, 5.47069, 5.62968])

xj_mas = np.array([1.350, 1.355, 1.360,
                   1.365, 1.370, 1.375,
                   1.380, 1.385, 1.390,
                   1.395, 1.400])

h = xi_mas[1] - xi_mas[0]

n = len(xi_mas)

def build_difference_table(y: float) -> list[list]:
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

def gauss_first_formula(
        x: float, x0: float, h: float,
        table: list[list], show_logs: bool = False) -> float:
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

    result = term1 + term2 + term3 + term4 + term5 + term6

    if show_logs:
        Rich.print_spacer()
        Rich.debug_log(f"Пошаговый расчет для x = {x:.3f}")
        Rich.debug_log(f"1. Вычисление параметра q = (x - x0) / h")
        Rich.debug_log(f"   q = ({x:.3f} - {x0:.3f}) / {h:.3f} = {q:.4f}")

        Rich.debug_log(f"2. Подстановка в формулу Гаусса:")
        Rich.debug_log(f"   Слагаемое 1 (y0): {term1:.6f}")
        Rich.debug_log(f"   Слагаемое 2 (q * dy0): {term2:.6f}")
        Rich.debug_log(f"   Слагаемое 3 (q(q-1)/2 * d2y): {term3:.6f}")
        Rich.debug_log(f"   Слагаемое 4 ((q+1)q(q-1)/6 * d3y): {term4:.6f}")
        Rich.debug_log(f"   Слагаемое 5 ((q+1)q(q-1)(q-2)/24 * d4y): {term5:.6f}")
        Rich.debug_log(f"   Слагаемое 6 (d5y): {term6:.6f}")

        Rich.success_log(f"3. Итоговый результат P(x) = {result:.6f}")
        Rich.debug_log(f"Расчет для x = {x:.3f} завершен")

    return result


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

def print_gauss_polynomial_formula(x0: float, h: float, table: list[list]) -> None:
    """
    Выводит формулу полинома Гаусса в явном виде с подставленными числами.
    """

    y0 = table[0][0]
    dy0 = table[0][1]
    d2y_1 = table[0][2]
    d3y_1 = table[0][3]
    d4y_2 = table[0][4]

    # q = (x - x0) / h
    # Подставляем числа: q = (x - 1.375) / 0.005 = 200*x - 275
    q_expr = f"((x - {x0}) / {h:.3f})"

    # Формируем строку формулы
    formula = f"P(x) = {y0:.5f}"
    formula += f" + {dy0:.5f} * q"
    formula += f" + ({d2y_1:.5f} / 2) * q * (q - 1)"
    formula += f" + ({d3y_1:.5f} / 6) * (q + 1) * q * (q - 1)"
    formula += f" + ({d4y_2:.5f} / 24) * (q + 1) * q * (q - 1) * (q - 2)"

    Rich.print_spacer()
    Rich.simple_log("Аналитический вид интерполяционного полинома Гаусса")
    Rich.simple_log(f"где q = {q_expr}")
    Rich.simple_log(formula)


def show_approximation_graphic():
    """
    Функция для показа графика только аппроксимации (без интерполяции)
    """

    Rich.print_spacer()
    Rich.simple_log("Построение графика аппроксимации (МНК)")

    a, b = linear_approximation(xi_mas, yi_mas)

    Rich.simple_log(f"Уравнение аппроксимации: F(x) = {a:.5f} * x + {b:.5f}")

    approx_results = [a * x + b for x in xj_mas]

    x_min = min(min(xj_mas), min(xi_mas)) - 0.01
    x_max = max(max(xi_mas), max(xj_mas)) + 0.01
    x_smooth = np.linspace(x_min, x_max, 200)
    y_smooth = [a * xi + b for xi in x_smooth]

    plt.figure(figsize=(10, 6))

    plt.plot(x_smooth, y_smooth, label='Линейная аппроксимация (МНК)', color='magenta', linewidth=2)

    plt.scatter(xi_mas, yi_mas, color='red', marker='o', s=80, label='Исходные узлы (x_i, y_i)', zorder=5)

    plt.scatter(xj_mas, approx_results, color='cyan', marker='s', s=50, label='Вычисленные точки (x_j)', zorder=5)

    plt.title('Аппроксимация (Метод Наименьших Квадратов)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


def show_graphic_formula_extrapolation_and_interpolation() -> None:
    """
    Функция для показа графика экстраполяции с найденными точками yj
    :return:
    """

    Rich.print_spacer()
    Rich.simple_log("Построение графика интерполяции и экстраполяции")

    # 1. Создаем гладкую линию для полинома
    # Берем диапазон от минимального xj до максимального xi с запасом
    x_min = min(min(xj_mas), min(xi_mas)) - 0.01
    x_max = max(max(xi_mas), max(xj_mas)) + 0.01
    x_smooth = np.linspace(x_min, x_max, 200)

    y_smooth = [gauss_first_formula(xi, x0, h, diff_table) for xi in x_smooth]

    plt.figure(figsize=(10, 6))

    # Линия полинома
    plt.plot(x_smooth, y_smooth, label='Полином Гаусса', color='blue')

    # Исходные точки
    plt.scatter(xi_mas, yi_mas, color='red', marker='o', s=80, label='Исходные узлы (x_i, y_i)', zorder=5)

    # Вычисленные точки
    plt.scatter(xj_mas, gauss_results, color='green', marker='x', s=80, label='Вычисленные точки (y_j)', zorder=5)

    # Оформление
    plt.title('Интерполяция и экстраполяция (Первая формула Гаусса)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


def linear_approximation(x, y, show_logs=False):
    """
    Функция вычисления линейной аппроксимации методом наименьших квадратов.
    Возвращает коэффициенты a и b для уравнения y = ax + b.
    """
    n = len(x)

    # Вычисляем суммы
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi * xi for xi in x)

    denominator = n * sum_xx - sum_x**2

    # Минимальные логи (только если show_logs=True)
    if show_logs:
        Rich.print_spacer()
        Rich.simple_log("Вычисление коэффициентов линейной аппроксимации (МНК)")
        Rich.debug_log(f"Суммы: Σx = {sum_x:.5f}, Σy = {sum_y:.5f}, Σxy = {sum_xy:.5f}, Σx² = {sum_xx:.5f}")
        Rich.debug_log(f"Знаменатель: n*Σx² - (Σx)² = {n}*{sum_xx:.5f} - ({sum_x:.5f})² = {denominator:.5f}")

    a = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - a * sum_x) / n

    if show_logs:
        Rich.success_log(f"Коэффициенты: a = {a:.5f}, b = {b:.5f}")
        Rich.simple_log(f"Уравнение аппроксимации: F(x) = {a:.5f} * x + {b:.5f}")

    return a, b


def show_approximate_and_interpolation_graphics():
    """
    Построение графика наложения интерполяции и линейной аппроксимации
    """

    x_min = min(min(xj_mas), min(xi_mas)) - 0.01
    x_max = max(max(xi_mas), max(xj_mas)) + 0.01
    x_smooth = np.linspace(x_min, x_max, 200)

    a, b = linear_approximation(xi_mas, yi_mas)

    y_gauss_smooth = [gauss_first_formula(xi, x0, h, diff_table) for xi in x_smooth]
    y_approx_smooth = [a * xi + b for xi in x_smooth]

    plt.figure(figsize=(10, 6))
    plt.plot(x_smooth, y_gauss_smooth, label='Полином Гаусса', color='blue', linewidth=2)
    plt.plot(x_smooth, y_approx_smooth, label='Линейная аппроксимация', color='magenta', linestyle='--',
             linewidth=2)
    plt.scatter(xi_mas, yi_mas, color='red', marker='o', s=80, label='Исходные узлы', zorder=5)
    plt.scatter(xj_mas, gauss_results, color='green', marker='x', s=80, label='Точки Гаусса (x_j)', zorder=5)
    plt.title('Наложение: Интерполяция Гаусса и Аппроксимация МНК')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


