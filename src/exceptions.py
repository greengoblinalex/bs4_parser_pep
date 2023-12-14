class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class NoPepVersionsFoundException(Exception):
    """Вызывается, когда парсер не нашел версии pep."""
    pass
