import logging

from requests import RequestException
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}),)
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def find_all_tags(soup, tag, attrs=None):
    searched_tags = soup.find_all(tag, attrs=(attrs or {}),)
    if len(searched_tags) == 0:
        error_msg = f'Не найдены теги {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tags


def uncorrect_status(url, status, expected_status):
    logging.warning(
        f'''Несовпадающие статусы:\n
        {url}\n
        Статус в карточке: {status}\n
        Ожидаемые статусы: {expected_status}'''
    )
