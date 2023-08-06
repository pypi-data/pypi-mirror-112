from base_method import BaseOneDimensionMethod
import numpy as np

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

    def __init__(self, function, borders: np.array, eps: np.float64 = 0.1,
                 count_of_iterations_limit: np.int64 = -1):
        super().__init__(function, borders, eps, count_of_iterations_limit)
        self.x_mean = 0
    def _set_borders(self, current_borders: np.array) -> None:
        super()._set_borders(current_borders)

    def _is_not_ended_increase_current_iteration(self) -> bool:
        return super()._is_not_ended_increase_current_iteration()

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """

        self.x_mean = (self.current_borders[0] + self.current_borders[1]) / 2
        x_left = self.x_mean - self.eps / 2.1
        x_right = self.x_mean + self.eps / 2.1
        y_left = self.function(x_left)
        y_right = self.function(x_right)
        if y_left > y_right:
            self.current_borders[0] = x_left
        else:
            self.current_borders[1] = x_right

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        while self._is_not_ended_increase_current_iteration():
            self.step()
        return np.array([self.x_mean, self.function(self.x_mean)])

