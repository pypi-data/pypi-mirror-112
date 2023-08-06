import time

from base_method import BaseOneDimensionMethod
import numpy as np
#TODO edit docs


class GoldenRatioMethod(BaseOneDimensionMethod):
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
        self.left_point = 0
        self.left_point_value = 0
        self.right_point = 0
        self.right_point_value = 0

    def _set_borders(self, current_borders: np.array) -> None:
        super()._set_borders(current_borders)

    def _is_not_ended_increase_current_iteration(self) -> bool:
        return super()._is_not_ended_increase_current_iteration()

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """

        if (self.right_point_value > self.left_point_value):
            self.current_borders[1] = self.right_point
            self.right_point_value = self.left_point_value
            self.right_point = self.left_point
            self.left_point = self.current_borders[0] + (3 - np.sqrt(5)) / 2 * (self.current_borders[1] -
                                                                                self.current_borders[0])
            self.left_point_value = self.function(self.left_point)
        else:
            self.current_borders[0] = self.left_point
            self.left_point_value = self.right_point_value
            self.left_point = self.right_point
            self.right_point = self.current_borders[1] - (3 - np.sqrt(5)) / 2 * (self.current_borders[1] -
                                                                                 self.current_borders[0])
            self.right_point_value = self.function(self.right_point)

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        self.left_point = self.current_borders[0] + (3 - np.sqrt(5)) / 2 * (self.current_borders[1] -
                                                                            self.current_borders[0])
        self.right_point = self.current_borders[1] - (3 - np.sqrt(5)) / 2 * (self.current_borders[1] -
                                                                             self.current_borders[0])
        self.left_point_value = self.function(self.left_point)
        self.right_point_value = self.function(self.right_point)
        while self._is_not_ended_increase_current_iteration():
            self.step()
        x_mean = (self.current_borders[1] + self.current_borders[0]) / 2
        return np.array([x_mean, self.function(x_mean)])



def y(x):
    return (x - 12) ** 2
