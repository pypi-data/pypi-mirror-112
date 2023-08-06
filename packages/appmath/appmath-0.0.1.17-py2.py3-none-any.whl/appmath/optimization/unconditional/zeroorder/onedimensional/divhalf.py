
import numpy as np

from base_method import BaseOneDimensionMethod


class StandardDivHalfFunction(BaseOneDimensionMethod):
    """Class StandartDivHalfFunction is special case of UniformMethod with count_of_intervals = 4, which calculate
    function only in 2 points, instead 3 how in UniformMethod

    Note: This method don't use parallel calculations

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
        self.x_mean = (self.start_borders[1] - self.start_borders[0]) / 2
        self.y_mean = self.function(self.x_mean)

    def _set_borders(self, current_borders: np.array) -> None:
        super()._set_borders(current_borders)

    def _is_not_ended_increase_current_iteration(self) -> bool:
        return super()._is_not_ended_increase_current_iteration()

    def step(self):
        """
        Calculate functions at 2 points, compare value at 3 points and decrease interval
        :return: None
        """
        interval_delta = self.current_borders[1] - self.current_borders[0]
        x_left = self.current_borders[0] + interval_delta / 4
        y_left = self.function(x_left)
        x_right = self.current_borders[1] - interval_delta / 4
        y_right = self.function(x_right)
        if y_left > self.y_mean:
            if y_right > self.y_mean:
                self._set_borders(np.array([x_left, x_right]))
            else:
                self.current_borders[0] = self.x_mean
                self.x_mean = x_right
                self.y_mean = y_right
        else:
            self.current_borders[1] = x_right
            self.x_mean = x_left
            self.y_mean = y_left
        self.current_min_coords = np.array([self.x_mean, self.y_mean])

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        return super(StandardDivHalfFunction, self).predict()

def f(x):
    return (x+1)**2
print(StandardDivHalfFunction(f, np.array([-1000., 1000.]), 0.001).predict())