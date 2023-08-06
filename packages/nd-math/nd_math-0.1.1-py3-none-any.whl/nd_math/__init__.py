import math


def acos(x: float, eps: float=1e-15) -> float:
    try:
        return math.acos(x)
    except ValueError as e:
        if x > 1 >= x - eps:
            return math.acos(1)
        if x < -1 <= x + eps:
            return math.acos(-1)
        raise e


def ctan(x: float) -> float:
    """ Возвращает котангенс аргумента """

    return math.cos(x) / math.sin(x)


def sqrt(x: float, eps: float) -> float:
    """ Вычисляет квадратный корень аргумента 'x'. Если аргумент выходит в область отрицательных значений,
    но меньше чем на величину 'eps'-аргумента, возвращает 0 без возникновения ошибки. """

    try:
        return math.sqrt(x)
    except ValueError as e:
        if math.fabs(x) < eps:
            return 0
        else:
            raise e


def asin(x: float, eps: float = 0.0) -> float:
    """Function returns arcsine from 'x' with eps = eps"""
    try:
        return math.asin(x)
    except Exception as e:
        if (x < -1) and (x + eps) >= -1:
            return math.asin(-1)
        elif (x > 1) and (x - eps) <= 1:
            return math.asin(1)
        raise e

