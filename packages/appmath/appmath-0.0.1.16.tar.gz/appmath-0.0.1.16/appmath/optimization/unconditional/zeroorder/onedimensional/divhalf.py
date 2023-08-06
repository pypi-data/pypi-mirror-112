
import numpy as np



class StandardDivHalfFunction:
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
        self.function = function
        assert borders.shape[0] == 2, "Border shape must have 2 parameters: left border, right border"
        self.start_borders = borders
        self.current_borders = self.start_borders
        assert eps > 0, "Epsilon must be more than zero"
        self.eps = eps
        self.current_min_coords: np.float64 = None
        self.iterations_limit = count_of_iterations_limit
        self.current_delta = 0
        self.x_mean = (self.start_borders[1] - self.start_borders[0]) / 2
        self.y_mean = self.function(self.x_mean)

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
                self.current_borders[0] = x_left
                self.current_borders[1] = x_right
            else:
                self.current_borders[0] = self.x_mean
                self.x_mean = x_right
                self.y_mean = y_right
        else:
            self.current_borders[1] = x_right
            self.x_mean = x_left
            self.y_mean = y_left

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """
        current_count_of_iterations: np.int64 = 0
        while self.current_borders[1] - self.current_borders[0] > self.eps:
            self.step()
            if self.iterations_limit != -1:
                current_count_of_iterations += 1
                if current_count_of_iterations > self.iterations_limit:
                    break
        self.current_min_coords = np.array([self.x_mean, self.y_mean])
        return self.current_min_coords

