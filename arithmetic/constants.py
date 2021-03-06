# Количество случайных элементов
random_items = 1

# Количество элементов в очереди
queue_max_size = 1

# Применение таймаутов
use_sleep = True

# Вывод в консоль
use_print = True

""" Параметры случайной генерации элементов прогрессии 
NB: ./views/back.py строка 14 
"""

# n - количество элементов целочисленное (int), от и до
param_n = (1, 10)

# d - дельта между элементами последовательности (float), от и до
param_d = (0.01, 0.05)

# n1 - Стартовое значение, всегда должно быть меньше, чем максимум от param_n
param_n1 = (1, 3)

# interval - интервал в секундах между итерациями (float)
param_interval = (0.01, 0.05)
