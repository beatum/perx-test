import asyncio
import random
from datetime import datetime
import time
from ..constants import *


async def make_progression(n: int, d: float, n1: int, interval: float) -> dict:
    start_time = time.monotonic()
    if use_print:
        print('------------------------------------------------')
        print('Создание прогрессии в карутине ')
        print('------------------------------------------------')
    """
    Асинхронный генератор (карутина) арифметической прогрессии
    :param n: int - натуральное число (2 <= n > 0), предел последовательности
    :param d: float - положительное или отрицательное число с десятичной дробью, разделитель в виде точки
    (-0.01 <= d => 0.01), шаг или разность последовательности (дельта)
    :param n1: int - натуральное число (n1 > n), начальный член прогрессии, который по значению не должен превышать,
    общее кол-во членов прогрессии n
    :param interval: float время в секундах между итерациями
    :return: dict - словарь с входящими аргументами и возрастающей (при d > 0) или убывающей (при d < 0)
    арифметической прогрессией
    """
    data = {'n': n, 'd': round(d, 3), 'n1': round(n1, 3), 'interval': interval}
    result = list()
    try:
        if n <= 0 or n <= n1 or d <= 0:
            raise
        else:
            for i in range(n):
                item = n1 + i * d
                result.append(round(item, 2))
                if use_print:
                    print(f'item = {item}')
                if use_sleep:
                    await asyncio.sleep(random.random())
                    if use_print:
                        print(f'sleep = {random.random()}')
                else:
                    await asyncio.sleep(0)
    except asyncio.CancelledError:
        raise
    finally:
        data['result'] = result
        stop_time = time.monotonic() - start_time
        if use_print:
            print(f'Результат: {data}')
            print('------------------------------------------------')
            print(f'Карутина завершила работу за {stop_time:.2f} c.')
            print('------------------------------------------------')
        return data


async def get_items(queue, item):
    """
    Берёт элемент из очереди, дожидается его обработки и возвращает его обратно
    :param queue: Очередь задач
    :param item: Текущий элемент
    :return: item object
    """
    sleep = random.uniform(0.01, 0.05)
    try:
        while True:
            await queue.get()
            item['status'] = 'В процессе'
            if use_print:
                print(f'Взяли задачу {item["num_in_queue"]} в процесс')
            if use_sleep:
                await asyncio.sleep(sleep)
            else:
                await asyncio.sleep(0)
            if use_print:
                print(f'Спим {sleep:.2f} c.')
            queue.task_done()
            if use_print:
                print(f'Уведомили очередь что задача {item["num_in_queue"]} обработана')
    except asyncio.CancelledError:
        raise


async def put_items(random_items):
    """
    Генерирует элементы
    :param random_items: int - Предел арифметической прогрессии, константа задаётся в фаиле constants.py
    :return: task object
    """
    if use_print:
        print('================================================')
        print(f'Создаём пустую очередь размером в {queue_max_size} элемент(ов)')
        print('================================================')

    queue = asyncio.Queue(maxsize=queue_max_size)

    data = list()

    tasks = []

    for i in range(1, random_items+1):
        try:
            item = await make_progression(
                round(random.randint(param_n[0], param_n[1]), 3),
                random.uniform(param_d[0], param_d[1]),
                random.randint(param_n1[0], param_n1[1]),
                round(random.uniform(param_interval[0], param_interval[1]), 3)
            )
        except asyncio.CancelledError:
            raise
        try:
            item['data_time'] = str(datetime.now())
            if queue_max_size:
                item['num_in_queue'] = i
            else:
                item['num_in_queue'] = None
            item['current_value'] = item['d']
            queue.put_nowait(item)
            start_time = time.monotonic()
            item['status'] = "В очереди"
            if use_print:
                print(f'Отправляем задачу {item["num_in_queue"]} в очередь')
        except asyncio.CancelledError:
            raise
        finally:
            if queue_max_size > 1:
                task = asyncio.create_task(get_items(queue, item))
                tasks.append(task)
            else:
                task = asyncio.create_task(get_items(queue, item))
                await queue.join()
                if use_print:
                    print(f'Завершаем работу с задачей {item["num_in_queue"]}')
                task.cancel()
                stop_time = time.monotonic() - start_time
                if use_print:
                    print(f'Задача выполненна за {stop_time:.4f} с.')
                item['total_time'] = f'{stop_time:.4f}'
        data.append(item)

    if queue_max_size > 1:
        await queue.join()
        for i in range(len(tasks)):
            for task in tasks:
                stop_time = time.monotonic() - start_time
                task.cancel()
                data[i]['total_time'] = f'{stop_time:.4f}'
        if use_print:
            print(f"Завершено {len(tasks)} задач(и)")

    #
    await asyncio.gather(*tasks, return_exceptions=True)

    if use_print:
        print('================================================')
        print(f'Возвращаем итоговый результат DATA:  {data}')
        print('================================================')
    return data


async def get_data():
    data = await put_items(random_items)
    return data
