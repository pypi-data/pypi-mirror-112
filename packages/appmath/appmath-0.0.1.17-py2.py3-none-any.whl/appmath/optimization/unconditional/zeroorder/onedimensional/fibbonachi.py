import numpy as np

from base_method import BaseOneDimensionMethod


class FibbonachiMethod(BaseOneDimensionMethod):
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

    def __init__(self, function, borders: np.array, eps: np.float64 = 0.1,
                 count_of_iterations_limit: np.int64 = -1):
        super().__init__(function, borders, eps, count_of_iterations_limit)
        self.left_point: np.float64 = 0
        self.left_point_value: np.float64 = 0
        self.right_point: np.float64 = 0
        self.right_point_value: np.float64 = 0
        self.fib_values = dict()
        self.max_fib_number = 0

    def _calculate_fib_values(self, f_n: np.int64):
        i = 1
        self.fib_values[0] = 1
        self.fib_values[1] = 1
        while self.fib_values[i] < f_n:
            self.fib_values[i + 1] = self.fib_values[i] + self.fib_values[i - 1]
            i += 1
        self.max_fib_number = i

    def _set_borders(self, current_borders: np.array) -> None:
        super()._set_borders(current_borders)

    def _is_not_ended_increase_current_iteration(self) -> bool:
        #if not super()._is_not_ended_increase_current_iteration():
        #    self.current_min_coords = np.array([(self.current_borders[0] + self.current_borders[1]) / 2,
        #                                        self.function((self.current_borders[0] + self.current_borders[1]) / 2)])
        #    return 0
        self.current_iteration += 1
        if self.current_iteration == self.max_fib_number - 4:
            self.left_point = self.right_point
            self.right_point = self.left_point + self.eps / 10
            self.left_point_value = self.function(self.left_point)
            self.right_point_value = self.function(self.right_point)
            if self.left_point_value < self.right_point_value:
                self.current_min_coords = np.array([(self.current_borders[0] + self.right_point) / 2,
                                                    self.function((self.current_borders[0] + self.right_point) / 2)])
            else:
                self.current_min_coords = np.array([(self.left_point + self.current_borders[1]) / 2,
                                                    self.function((self.left_point + self.current_borders[1]) / 2)])
            return 0
        return 1

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """
        if self.left_point_value <= self.right_point_value:
            self.current_borders[1] = self.right_point
            self.right_point = self.left_point
            self.right_point_value = self.left_point_value
            self.left_point = self.current_borders[0] + self.fib_values[
                self.max_fib_number - 2 - self.current_iteration] / \
                              self.fib_values[self.max_fib_number - self.current_iteration] * (
                                      self.current_borders[1] - self.current_borders[0])
            self.left_point_value = self.function(self.left_point)
            #print(self.fib_values[self.max_fib_number - 2 - self.current_iteration], self.fib_values[self.max_fib_number - self.current_iteration], self.left_point, self.right_point, 1)
        else:
            self.current_borders[0] = self.left_point
            self.left_point = self.right_point
            self.left_point_value = self.right_point_value
            self.right_point = self.current_borders[0] + self.fib_values[
                self.max_fib_number - 1 - self.current_iteration] / \
                              self.fib_values[self.max_fib_number - self.current_iteration] * (
                                      self.current_borders[1] - self.current_borders[0])
            self.right_point_value = self.function(self.right_point)

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        f_n = (self.start_borders[1] - self.start_borders[0]) / self.eps
        self._calculate_fib_values(f_n)
        self.left_point = self.current_borders[0] + self.fib_values[
            self.max_fib_number - 2] / self.fib_values[self.max_fib_number] * (self.current_borders[1]
                                                                               - self.current_borders[0])
        self.right_point = self.current_borders[0] + self.fib_values[
            self.max_fib_number - 1] / self.fib_values[self.max_fib_number] * (self.current_borders[1]
                                                                               - self.current_borders[0])
        self.left_point_value = self.function(self.left_point)
        self.right_point_value = self.function(self.right_point)
        self.current_iteration = 0
        while self._is_not_ended_increase_current_iteration():
            self.step()

        return self.current_min_coords

def y(x):
    return (x - 1.5) ** 2

print(FibbonachiMethod(y, np.array([-10, 10]), 0.0001).predict())
