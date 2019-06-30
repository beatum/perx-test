# Асинхронный сервер для подсчёта арифметической прогрессии

Разработал: Иван Семерняков beatuminflow@gmail.com / direct@beatum-group.ru

Приложение реализовано в качестве демо версии.

## Физическая архитектура

Приложение тестировалась на ПК со следующими характеристиками:

* ОС Ubuntu 18.04 LTE
* Память 8 Гб.
* Процессор Intel® Core™ i3-3240 CPU @ 3.40GHz × 4
* Тип ОС 64-бит

## Основные зависимости

* pipenv
* aiohttp
* aiohttp-jinja2
* python 3.6 / 3.7 (тестировалось на Python 3.7)

## Инструкция по развёртыванию
```
sudo apt install python3.7 python3-venv python3.7-venv
git clone https://github.com/beatum/perx-test.git && cd $_
python3.7 -m venv env
source env/bin/activate
pip install --upgrade pip pipenv
pipenv install
python run.py
```
## Инструкция по применению

Основные параметры задаются в фаиле constants.py:

Количество случайных элементов
```
random_items = 1
```
Количество элементов в очереди - этот параметр отвечает
за общее количество одновременно выполняемых (асинхронных) операций
```
queue_max_size = 1
```
Для ускорения вычеслительных процессов, установите значения:
```
# Применение таймаутов
use_sleep = False

# Вывод в консоль
use_print = False
```
Подробно изучите фаил constants.py для того, чтобы можно было устанавливать нужные вам параметры работы приложения.
Наслаждаемся работой сервиса по адресу localhost:8000

### Лицензия

Приложение разработано под лицензией: [MIT License](http://opensource.org/licenses/MIT).
