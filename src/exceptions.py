class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class NoVersionsFoundException(Exception):
    """Вызывается, когда парсер не нашел версии pep."""
    pass
