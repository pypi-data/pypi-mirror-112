from typing import Union, Any

import matplotlib.pyplot as plt
import numpy as np

import scipy.optimize as sco
from PyCurve.simulation import Simulation
from PyCurve.curve import Curve
from PyCurve.linear import LinearCurve
from PyCurve.cubic import CubicCurve
from PyCurve.svensson_nelson_siegel import NelsonSiegelAugmented
from PyCurve.bjork_christensen_augmented import BjorkChristensenAugmented

plt.style.use("bmh")


class HullWhite:

    def __init__(self, alpha: float, sigma: float, rt: float, time: float,
                 delta_time: float, instantaneous_forward: Curve, method: str) -> None:
        self._alpha = alpha
        self._sigma = sigma
        self._rt = rt
        self._dt = delta_time
        self._steps = int(time / delta_time)
        self._f_curve = self._is_valid_curve(instantaneous_forward)
        self._method = self.set_method(method)

    def get_attr(self, attr: str) -> Union[float, int]:
        return self.__getattribute__(attr)

    @staticmethod
    def set_method(method: Any) -> str:
        if method in ["cubic", "linear", "bjc", "nss"]:
            return method
        else:
            raise TypeError("method must be 'linear' , 'cubic' , 'bjc' , 'nss' ")

    @staticmethod
    def _is_valid_curve(curve: Any) -> Curve:
        """Check if an attribute is an instance of Curve"""
        if not (isinstance(curve, Curve)):
            raise ValueError("Curve parameter must be an instance of Curve")
        return curve

    def _sigma_part(self, n: int) -> float:
        return self.get_attr("_sigma") * np.sqrt(self.get_attr("_dt")) * np.random.normal(size=n)

    def _interp_forward(self, t):
        curve_interp = None
        if self._method == "linear":
            curve_interp = LinearCurve(self._f_curve)
        elif self._method == "cubic":
            curve_interp = CubicCurve(self._f_curve)
        elif self._method == "bjc":
            curve_interp = BjorkChristensenAugmented(1, 1, 1, 1, 1, 1)
            curve_interp.calibrate(self._f_curve)
        elif self._method == "nss":
            curve_interp = NelsonSiegelAugmented(1, 1, 1, 1, 1, 1)
            curve_interp.calibrate(self._f_curve)
        return curve_interp.d_rate(t)

    def _theta_part(self, t):
        sigma = (np.power(self._sigma, 2) / (2 * self._alpha)) * (1 - np.exp(-2 * self._alpha * t))
        return (self._interp_forward(t) - self._interp_forward(t - self._dt)) + self._alpha * self._interp_forward(
            t) + sigma

    def _mu_dt(self, rt: np.ndarray, t) -> float:
        return self.get_attr("_alpha") * (self._theta_part(t) - rt) * self.get_attr("_dt")

    def simulate_paths(self, n: int) -> np.array:
        simulation = np.zeros(shape=(self.get_attr("_steps"), n))
        simulation[0, :] = self._rt
        for i in range(1, self.get_attr("_steps"), 1):
            dr = self._mu_dt(simulation[i - 1, :], i * self.get_attr("_dt")) + self._sigma_part(n)
            simulation[i, :] = simulation[i - 1, :] + dr
        return Simulation(simulation, self.get_attr("_dt"))

    def calibration_func(self, x):
        output = np.zeros(len(self._f_curve.get_rate))
        compare = np.zeros(len(self._f_curve.get_rate))
        self._alpha = x[0]
        for i in range(len(self._f_curve.get_rate) - 1):
            output[i] = self._theta_part(self._f_curve.get_time[i + 1])
            compare[i] = self._f_curve.get_rate[i + 1]
        sqr_error_sum = ((output - compare) ** 2).sum()
        return sqr_error_sum

    def calibrate_alpha(self):
        x0 = np.array([1])
        boundaries = ((-np.inf, np.inf),)
        calibration_result = sco.minimize(self.calibration_func, x0, method='L-BFGS-B', bounds=boundaries)
        return calibration_result

    def plot_calibrated(self, simulation: Simulation) -> None:
        fig = plt.figure(figsize=(12.5, 8))
        fig.suptitle("Model Fitting Curve T=0")
        fig.canvas.set_window_title('Model Fitting Curve T=0')
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel('t, years')
        ax1.set_ylabel('Yield')
        ax1.plot(np.linspace(1, simulation.get_steps, simulation.get_steps) * simulation.get_dt,
                 simulation.get_sim, lw=0.5)
        ax1.plot(self._f_curve.get_time, self._f_curve.get_rate, c="darkred", label="Observed", lw=3)
        plt.show()
