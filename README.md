# Проект парсинга pep
<h1 align="center">Всем привет! Меня зовут <a href="https://github.com/greengoblinalex" target="_blank">Алексей</a> и я автор данного проекта
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

## Описание
Проект парсинга pep - это парсер, который выполняет такие действия(вывод данных может осуществляться как в консоль, так и в csv-файл):
- What`s new - парсит docs.python.org и выводит данные об обновлениях
- Latest versions - парсит и выдает все версии python, ссылки на их документации и статусы
- Download - скачивает архив, содержащий все документы для последней версии python
- Pep - парсит и выводит данные о количестве статусов pep

## Использованные технологии
- Requests-cache
- Tqdm
- Beautifulsoup4
- Argparse
- Logging