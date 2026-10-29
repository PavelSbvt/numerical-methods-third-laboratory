from rich.console import Console
from rich.table import Table


console = Console()


class Rich:
    """
    Класс с методами вывода логов в консоль с использованием библиотеки Rich
    """


    @staticmethod
    def success_log(message: str) -> None:
        """
        Лог об успешном выполнении (используется при сообщении об успешном выполнении
        какой-то операции) - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает текст сообщения об успешном выполнении какой-то операции,
        который будет выведен в терминал (консоль)

        :return: None
        """

        console.log(f"[green][SUCCESS] {message}[/green]", _stack_offset=2)


    @staticmethod
    def simple_log(message: str) -> None:
        """
        Обычный лог (информационный) - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает текст лога (информационный), который будет выведен в
        терминал (консоль)

        :return: None
        """

        console.log(f"[cyan][INFO] {message}[/cyan]", _stack_offset=2)


    @staticmethod
    def debug_log(message: str) -> None:
        """
        Лог для логирования - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает текст лога, который будет выведен в терминал (консоль)

        :return: None
        """

        console.log(f"[grey46][Debug] {message}[/grey46]", _stack_offset=2)


    @staticmethod
    def print_spacer() -> None:
        """
        Разделитель для более наглядного показа лога процессов в консоли

        :return: None
        """

        console.log(f"[grey46][Debug] {'-' * 151}[/grey46]", _stack_offset=2)


    @staticmethod
    def print_table(title: str, cols: list, rows: list) -> None:
        """
        Функция для вывода таблицы в консоль с помощью библиотеки Rich

        :param title: Str - Принимает заголовок таблицы
        :param cols: list - Принимает список с содержимым столбцов
        :param rows: list - Принимает список с содержимым строк

        :return: None
        """

        table = Table(title=title)

        for col in cols:
            table.add_column(col)

        for row in rows:
            table.add_row(*[str(cell) for cell in row])

        console.print(table)
