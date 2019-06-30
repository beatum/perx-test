import asyncio
import random
import time
from datetime import datetime


async def maker(n: int, d: float, n1: int, interval: float) -> None:
    """
    Асинхронный генератор (карутина) арифметической прогрессии
    :param n: int - натуральное число (2 <= n > 0), предел последовательности
    :param d: float - положительное или отрицательное число с десятичной дробью, разделитель в виде точки
    (-0.01 <= d => 0.01), шаг или разность последовательности (дельта)
    :param n1: int - натуральное число (n1 > n), начальный член прогрессии, который по значению должен превышать,
    общее кол-во членов прогрессии n
    :param interval: float время в секундах между итерациями
    :return: dict - Возвращает словарь с входящими аргументами и возрастающей (при d > 0) или убывающей (при d < 0)
    арифметической прогрессией
    """
    data = {'iter': n, 'start': n1, 'step': d}
    result = list()
    loop = asyncio.get_running_loop()
    try:
        if n <= 0 or n <= n1 or d <= 0:
            raise
        else:
            for i in range(n):
                item = n1 + i * d
                result.append(round(item, 2))
                print(f'Время итерации {loop.time()}')
                await asyncio.sleep(interval)
    except asyncio.CancelledError as e:
        print(e)
        raise
    except Exception as e:
        print(e)
    data['result'] = result
    print('Generator:', data)
    return data


async def consumer(queue, data):
    print(f'Начали обработку {data}')
    data['status'] = "В процессе"
    try:
        while True:
            try:
                print(f'{data} получили')
                await queue.get()
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{data} исключение {e!r}")
                raise
            finally:
                queue.task_done()
                print(f'Уведомляем очередь о том, что задача обработана')
                print(f'Закончили выполнение {data}, вернули данные')
    except asyncio.CancelledError:
        raise
    finally:
        print(f"Завершили обработку {data}")
        return data


async def producer():
    print(f'Создаём пустую очередь задач')
    queue = asyncio.Queue()

    print(f'Наполняем очередь')
    result = []
    data = await maker(random.randint(1, 10), random.randint(1, 5), random.randint(1, 2), random.random())
    for i in range(4):
        data['data_time'] = str(datetime.now())
        data['num_in_queue'] = i
        data['current_value'] = data['step']
        await queue.put(data)
        data['status'] = "В очереди"
        result.append(data)

    print(f'RESULT {result}')

    print(f'Размер очереди {queue.qsize()}')

    tasks = []
    print(f'Передаём очередь на обработку')
    for i in range(1):
        task = asyncio.create_task(consumer(queue, data))
        tasks.append(task)

    # Снятие блокировки, пока все задачи не будут выполнены
    await queue.join()
    print(f'Все задачи в очереди {queue} выполнены!')

    for task in tasks:
        task.cancel()
        print(f'Задача удалена')

    print(f'Ожидаем, пока все задачи не будут выполнены')
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')

    return data


async def get_data():
    data = await producer()
    print(f'GET DATA {data}')
    return data

# asyncio.run(handler(), debug=True)
