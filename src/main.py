import re
from urllib.parse import urljoin
import logging
from collections import defaultdict

import requests_cache
from tqdm import tqdm

from constants import (BASE_DIR, MAIN_DOC_URL,
                       PEP_DOC_URL, EXPECTED_STATUS)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import find_tag, find_all_tags, get_soup, uncorrect_status
from exceptions import NoPepVersionsFoundException


def whats_new(session: requests_cache.CachedSession):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')

    soup = get_soup(session, whats_new_url)

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})

    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})

    sections_by_python = find_all_tags(
        div_with_ul,
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)

        soup = get_soup(session, version_link)

        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')

        results.append(
            (version_link, h1.text, dl_text)
        )

    return results


def latest_versions(session: requests_cache.CachedSession):
    soup = get_soup(session, MAIN_DOC_URL)

    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = find_all_tags(sidebar, 'ul')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            for a_tag in a_tags:
                link = a_tag['href']
                text_match = re.search(pattern, a_tag.text)

                if text_match is not None:
                    version, status = text_match.groups()
                else:
                    version, status = a_tag.text, ''

                results.append((link, version, status))
            break
    else:
        raise NoPepVersionsFoundException('Ничего не нашлось')

    return results


def download(session: requests_cache.CachedSession):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')

    soup = get_soup(session, downloads_url)

    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag,  'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']

    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    # К сожалению, если я заменяю BASE_DIR / 'results' на DOWNLOADS_DIR
    # из константы, тесты перестают проходится
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    with open(archive_path, 'wb') as file:
        file.write(soup.encode('utf-8'))

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session: requests_cache.CachedSession):
    soup = get_soup(session, PEP_DOC_URL)

    table_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    table_body_tag = find_tag(table_tag, 'tbody')
    row_tags = find_all_tags(
        table_body_tag, 'tr',
        attrs={'class': re.compile('row')})

    status_count = defaultdict(int)

    for row_tag in tqdm(row_tags):
        table_status_tag = find_tag(row_tag, 'abbr')
        table_status_text = table_status_tag.text

        pep_tag = find_tag(
            row_tag, 'a',
            attrs={'class': 'pep reference internal'}
        )
        pep_link = pep_tag['href']
        pep_url = urljoin(PEP_DOC_URL, pep_link)

        soup = get_soup(session, pep_url)

        dl_tag = find_tag(
            soup, 'dl',
            attrs={'class': 'rfc2822 field-list simple'}
        )
        dt_tag = dl_tag.find(string=re.compile('Status')).parent
        status_text = dt_tag.find_next_sibling().text

        expected_status = EXPECTED_STATUS[table_status_text[1:]]
        if status_text not in expected_status:
            uncorrect_status(pep_url, status_text, expected_status)

        status_first_letter = status_text[0]
        if status_text in EXPECTED_STATUS.get(status_first_letter):
            status_count[status_first_letter] += 1

    results = [('Статус', 'Количество')]
    for key, value in EXPECTED_STATUS.items():
        results.append((value, status_count[key]))

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode

    try:
        results = MODE_TO_FUNCTION[parser_mode](session)
    except Exception:
        logging.exception('Возникла ошибка во время работы парсера')

    if results:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
