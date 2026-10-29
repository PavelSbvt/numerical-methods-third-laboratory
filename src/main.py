from core.first_Gauss_formula import (
    diff_table,
    xi_mas, yi_mas, xj_mas,
    gauss_first_formula,
    cols, rows,
    cols_res, rows_res,
    print_gauss_polynomial_formula,
    x0, h,
    show_graphic_formula_extrapolation_and_interpolation,
    linear_approximation,
    gauss_results,
    show_approximate_and_interpolation_graphics,
    show_approximation_graphic)
from utils.output_rich import Rich

# варианты лабораторной - 4, 10

# Первая формула Гаусса


if __name__== "__main__":
    Rich.print_spacer()
    Rich.simple_log("Расчет таблицы конечных разностей")

    Rich.print_table("Таблица конечных разностей", cols, rows)
    Rich.success_log("Таблица разностей построена")

    Rich.print_spacer()
    Rich.success_log("Вычисление значений по Первой формуле Гаусса")

    print_gauss_polynomial_formula(x0, h, diff_table)

    show_graphic_formula_extrapolation_and_interpolation()

    for x in xi_mas:
        y_val = gauss_first_formula(x, x0, h, diff_table)

    cols_inter = ["xi", "yi"]
    rows_inter = []
    for i in range(len(xi_mas)):
        rows_inter.append([f"{xi_mas[i]}", f"{yi_mas[i]}"])
    Rich.print_table("входные данные", cols_inter, rows_inter)

    for x in xj_mas:
        y_val = gauss_first_formula(x, x0, h, diff_table)

    Rich.print_table("Результаты экстраполяции и интерполяции", cols_res, rows_res)

    Rich.success_log("Вычисления по Гауссу завершены")

    a, b = linear_approximation(xi_mas, yi_mas, True)

    approx_results = [a * x + b for x in xj_mas]

    cols_approx = ["x_j", "Гаусс (P_n)", "МНК (F(x))", "Разница"]
    rows_approx = []
    for i, x in enumerate(xj_mas):
        rows_approx.append([
            f"{x:.3f}",
            f"{gauss_results[i]:.6f}",
            f"{approx_results[i]:.6f}",
            f"{abs(gauss_results[i] - approx_results[i]):.6f}"
        ])
    Rich.print_table("Сравнение интерполяции и аппроксимации", cols_approx, rows_approx)

    Rich.success_log("Аппроксимация выполнена")

    Rich.print_spacer()
    Rich.simple_log("Построение графика аппроксимации")
    show_approximation_graphic()

    Rich.print_spacer()
    Rich.simple_log("Построение графика наложения интерполяции и линейной аппроксимации")

    show_approximate_and_interpolation_graphics()
