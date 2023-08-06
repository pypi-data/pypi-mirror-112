import time

import numba
import numpy as np
from base_method import BaseOneDimensionMethod

@numba.jit(nopython=True, nogil=True, fastmath=True)
def numba_jit_step(function, current_borders: np.array, count_of_intervals: np.float64, current_delta) -> np.float64:
    current_min_coords = np.array([current_borders[0], function(current_borders[0])])
    for i in range(1, count_of_intervals + 1):
        x_i = current_borders[0] + i * current_delta
        y = function(x_i)
        if y < current_min_coords[1]:
            current_min_coords = np.asarray([x_i, y])
    return current_min_coords

'''
@numba.jit(parallel=True, nopython=False)
def numba_parallel_step(function, current_borders, count_of_intervals, current_delta):
    current_min_coords = numba.typed.Dict.empty(
        key_type=numba.core.types.int64,
        value_type=numba.core.types.float64[:],
    )
    for i in numba.prange(0, count_of_intervals + 1):
        x_i = current_borders[0] + i * current_delta
        y = function(x_i)
        if current_min_coords.get(i) in None:
            current_min_coords[i] = np.array([x_i, y])
            continue
        if current_min_coords.get(i)[1] > y:
            current_min_coords[i] = np.array([x_i, y])
    result_min_coords = current_min_coords[0]
    for i in range(1, count_of_intervals + 1):
        if current_min_coords[i][1] < result_min_coords[1]:
            result_min_coords = current_min_coords[i]
    return result_min_coords
'''

class UniformFunction:
    """Class UniformFunction is one of variants one-dimensions optimization

    Warning: We use numba, which translate your code to C/C++ and compile it. If you use your function in many places,
    including appmath or numba, add jit decorator. It will reduce costs on function compilation:
    function = numba.jit()(your_function). Also at first step method can take more time than next steps.
    This realization can be useful when needed a lot of iterations.

    Attributes
    ----------
    function: def/@jit def
        Your one-dimension function
    borders: np.array([left search border, right search border])
    count_of_intervals: int
        Diving into count_of_intervals parts of your interval for calculation f(x_i)
    eps: np.float64
        Result error
    count_of_iterations_limit: np.int64
        Limit of deepening iterations
    is_jitted: bool
        If you give @jit def you must set True for this parameter

    Methods
    -------
    step()
        Delegate calculations at one interval to compiled by numba code

    predict()
        Calculate min for your task. Returns np.array([argminF(x), f(argminF(x))])

    """

    def __init__(self, function, borders: np.array, count_of_intervals: np.int64 = 200, eps: np.float64 = 0.1,
                 count_of_iterations_limit: np.int64 = -1, is_jitted: bool = False):
        if is_jitted:
            self.function = function
        else:
            self.function = numba.njit()(function)

        assert borders.shape[0] == 2, "Border shape must have 2 parameters: left border, right border"
        self.start_borders = borders
        self.current_borders = self.start_borders
        assert count_of_intervals > 1, "Count of intervals must be more than one"
        self.count_of_intervals = count_of_intervals
        assert eps > 0, "Epsilon must be more than zero"
        self.eps = eps
        self.current_min_coords: np.float64 = None
        self.iterations_limit = count_of_iterations_limit
        self.current_delta = 0

    def set_borders(self, current_borders: np.array) -> None:
        if current_borders[0] < self.start_borders[0]:
            self.current_borders[0] = self.start_borders[0]
        else:
            self.current_borders[0] = current_borders[0]
        if current_borders[1] > self.start_borders[1]:
            self.current_borders[1] = self.start_borders[1]
        else:
            self.current_borders[1] = current_borders[1]
        return

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """
        self.current_min_coords = numba_jit_step(function=self.function, current_borders=self.current_borders,
                                                 count_of_intervals=self.count_of_intervals,
                                                 current_delta=self.current_delta)

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        current_count_of_iterations: np.int64 = 0
        while self.current_borders[1] - self.current_borders[0] > self.eps:
            self.current_delta = (self.current_borders[1] - self.current_borders[0]) / self.count_of_intervals
            self.step()
            self.set_borders(np.array([self.current_min_coords[0] - self.current_delta, self.current_min_coords[0] +
                                       self.current_delta]))
            if self.iterations_limit != -1:
                current_count_of_iterations += 1
                if current_count_of_iterations > self.iterations_limit:
                    break
        return self.current_min_coords


def f(x: float) -> float:
    return x ** 38

f2 = numba.njit()(f)
numba_jit_step(f2, np.array([-10., 10.]), 10000, 0.1)

unf = UniformFunction(f2, np.array([-1000., 1000.], dtype=np.float64), 200, count_of_iterations_limit=10000,
                      eps=0.00001, is_jitted=True)
unf.predict()

class StandardUniformFunction(BaseOneDimensionMethod):
    """Class StandartUniformFunction is one of variants one-dimensions optimization

    Note: It's standard method which don't use numba's compilation

    Attributes
    ----------
    function: def
        Your one-dimension function
    borders: np.array([left search border, right search border])
    count_of_intervals: int
        Diving into count_of_intervals parts of your interval for calculation f(x_i)
    eps: np.float64
        Result error
    count_of_iterations_limit: np.int64
        Limit of deepening iterations

    Methods
    -------
    step()
        Delegate calculations at one interval to compiled by numba code

    predict()
        Calculate min for your task. Returns np.array([argminF(x), f(argminF(x))])

    """

    def __init__(self, function, borders: np.array, count_of_intervals: np.int64 = 200, eps: np.float64 = 0.1,
                 count_of_iterations_limit: np.int64 = -1):
        super().__init__(function, borders, eps, count_of_iterations_limit)
        assert count_of_intervals > 1, "Count of intervals must be more than one"
        self.count_of_intervals = count_of_intervals
        self.current_delta = 0

    def _set_borders(self, current_borders: np.array) -> None:
        super()._set_borders(current_borders)

    def _is_not_ended_increase_current_iteration(self) -> bool:
        return super()._is_not_ended_increase_current_iteration()

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """

        current_min_coords = np.array([self.current_borders[0], self.function(self.current_borders[0])])
        for i in range(1, self.count_of_intervals + 1):
            x_i = self.current_borders[0] + i * self.current_delta
            y = self.function(x_i)
            if y < current_min_coords[1]:
                current_min_coords = np.asarray([x_i, y])
        self.current_min_coords = current_min_coords

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        while self._is_not_ended_increase_current_iteration():
            self.current_delta = (self.current_borders[1] - self.current_borders[0]) / self.count_of_intervals
            self.step()
            self._set_borders(np.array([self.current_min_coords[0] - self.current_delta, self.current_min_coords[0] +
                                       self.current_delta]))

        return self.current_min_coords

'''
class ParallelUniformFunction:
    """Class StandartUniformFunction is one of variants one-dimensions optimization

    Note: It's standard method which don't use numba's compilation

    Attributes
    ----------
    function: def
        Your one-dimension function
    borders: np.array([left search border, right search border])
    count_of_intervals: int
        Diving into count_of_intervals parts of your interval for calculation f(x_i)
    eps: np.float64
        Result error
    count_of_iterations_limit: np.int64
        Limit of deepening iterations

    Methods
    -------
    step()
        Delegate calculations at one interval to compiled by numba code

    predict()
        Calculate min for your task. Returns np.array([argminF(x), f(argminF(x))])

    """

    def __init__(self, function, borders: np.array, count_of_intervals: np.int64 = 200, eps: np.float64 = 0.1,
                 count_of_iterations_limit: np.int64 = -1, workers: np.int64 = 1):
        self.function = function
        assert borders.shape[0] == 2, "Border shape must have 2 parameters: left border, right border"
        self.start_borders = borders
        self.current_borders = self.start_borders
        assert count_of_intervals > 1, "Count of intervals must be more than one"
        self.count_of_intervals = count_of_intervals
        assert eps > 0, "Epsilon must be more than zero"
        self.eps = eps
        self.current_min_coords: np.float64 = None
        self.iterations_limit = count_of_iterations_limit
        self.current_delta = 0
        self.workers = workers
        if self.workers >= 4:
            self.count_of_intervals = self.workers

    def set_borders(self, current_borders: np.array) -> None:
        if current_borders[0] < self.start_borders[0]:
            self.current_borders[0] = self.start_borders[0]
        else:
            self.current_borders[0] = current_borders[0]
        if current_borders[1] > self.start_borders[1]:
            self.current_borders[1] = self.start_borders[1]
        else:
            self.current_borders[1] = current_borders[1]
        return

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """
        if self.workers >= 4:
            self.current_min_coords = numba_parallel_step(self.function, self.current_borders, self.count_of_intervals,
                                                          self.current_delta)
        else:
            current_min_coords = np.array([self.current_borders[0], self.function(self.current_borders[0])])
            for i in range(1, self.count_of_intervals + 1):
                x_i = self.current_borders[0] + i * self.current_delta
                y = self.function(x_i)
                if y < current_min_coords[1]:
                    current_min_coords = np.asarray([x_i, y])
            self.current_min_coords = current_min_coords

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        current_count_of_iterations: np.int64 = 0
        while self.current_borders[1] - self.current_borders[0] > self.eps:
            self.current_delta = (self.current_borders[1] - self.current_borders[0]) / self.count_of_intervals
            self.step()
            self.set_borders(np.array([self.current_min_coords[0] - self.current_delta, self.current_min_coords[0] +
                                       self.current_delta]))
            if self.iterations_limit != -1:
                current_count_of_iterations += 1
                if current_count_of_iterations > self.iterations_limit:
                    break
        return self.current_min_coords

'''

