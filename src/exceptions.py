class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class NoPepVersionsFoundException(Exception):
    """Вызывается, когда парсер не нашел версии pep."""
    pass


class UncorrectPepStatusException(Exception):
    """Вызывается, когда статус из таблицы pep не совпадает
    со статусом на странице pep."""

    def __init__(self, url, status, expected_status):
        error_message = (
            f'''Несовпадающие статусы:\n
            {url}\n
            Статус в карточке: {status}\n
            Ожидаемые статусы: {expected_status}'''
        )
        super().__init__(error_message)
