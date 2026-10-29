from core.first_Gauss_formula import (
    diff_table,
    xi_mas, yi_mas,
    cols, rows,
    cols_res, rows_res,
    print_gauss_polynomial_formula,
    x0, h,
    show_graphic_formula)
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

    Rich.print_table("Результаты интерполяции/экстраполяции", cols_res, rows_res)
    Rich.success_log("Вычисления по Гауссу завершены")

    print_gauss_polynomial_formula(x0, h, diff_table)

    show_graphic_formula()