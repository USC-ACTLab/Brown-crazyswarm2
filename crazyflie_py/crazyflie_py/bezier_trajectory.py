#!/usr/bin/env python

import bezier
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb, perm
import math
import json
import random


# Single bezier curve class that extends the bezier package
class BezierCurve(bezier.Curve):
    def __init__(
        self,
        nodes,
        degree,
        ctrl_pts_yaw: np.ndarray = None,
        duration=None,
        *args,
        **kwargs,
    ):
        super().__init__(nodes, degree, *args, **kwargs)
        self.duration = duration if duration else 1.0

        self.ctrl_pts_x = nodes[0]
        self.ctrl_pts_y = nodes[1]
        if nodes.shape[0] == 3:
            self.ctrl_pts_z = nodes[2]
        if ctrl_pts_yaw is None:
            self.ctrl_pts_yaw = np.zeros_like(self.ctrl_pts_x)
        else:
            self.ctrl_pts_yaw = ctrl_pts_yaw

    @classmethod
    def from_nodes(cls, nodes: np.ndarray, duration: float = None) -> "BezierCurve":
        """Generate a BezierCurve instance from nodes.

        Args:
            nodes (np.ndarray): The nodes in the curve, where the columns represent
            each node white the rows are the dimension of the ambient space.
            duration (float, optional): The duration of the curve. Equivalent as
            the maximum parameter value (t) when evaluating the curve. Defaults to None.

        Returns:
            BezierCurve: The BezierCurve instance.
        """
        _, num_nodes = nodes.shape
        degree = num_nodes - 1
        return cls(nodes, degree, duration=duration)

    def derivative(self, k: int = 1):
        """Return the k-th derivative of the Bézier curve."""
        if k < 0:
            raise ValueError("k can't be negative.")
        if k > self.degree:
            raise ValueError(
                f"k can't be greater than the degree of the curve ({self.degree})."
            )

        nodes = self.nodes
        n = self.degree
        for _ in range(k):
            nodes = (nodes[:, 1:] - nodes[:, :-1]) * n
            n -= 1
        return BezierCurve(nodes / self.duration**k, n, self.duration)

    def eval(self, parameter: float, derivative_degree: int = 0) -> np.ndarray:
        """Evaluate the Bézier curve at a given parameter.

        Args:
            parameter (float): Parameter value to evaluate the curve. Must be in [0, duration].
            derivative_degree (int, optional): The degree of the derivative to evaluate. Defaults to 0.

        Returns:
            np.ndarray: The evaluated point in the ambient space.
        """
        # construct the bernsteinBasis
        basis_functions = self.bernstein_basis(
            self.degree, self.duration, parameter, derivative_degree
        )
        result = np.zeros((self.dimension,))
        for nodes_idx in range(self.degree + 1):  # number of nodes
            result += self.nodes[:, nodes_idx] * basis_functions[nodes_idx]

        return result

    @staticmethod
    def bernstein_basis(bezier_degree, max_parameter, parameter, derivative_degree):
        if parameter < 0 or parameter > max_parameter:
            raise ValueError(
                f"bernsteinBasis: given parameter is outside of [0, {max_parameter}]."
            )

        result = np.zeros(bezier_degree + 1)

        if max_parameter == 0:
            if derivative_degree == 0:
                result[0] = 1.0
            return result

        for i in range(bezier_degree + 1):
            base = 0.0
            mult = 1.0
            for j in range(bezier_degree - derivative_degree + 1):
                if j + derivative_degree >= i:
                    comb_result = comb(bezier_degree - i, j + derivative_degree - i)
                    perm_result = perm(j + derivative_degree, derivative_degree)
                    pow_result = np.power(1.0 / max_parameter, j + derivative_degree)
                    base += (
                        comb_result
                        * pow_result
                        * perm_result
                        * mult
                        * ((j + derivative_degree - i) % 2 == 0 and 1 or -1)
                    )
                mult *= parameter

            comb_result = comb(bezier_degree, i)
            base *= comb_result
            result[i] = base

        return result

    # Overrides the method defined in the Bezier package
    def plot(
        self,
        num_points=200,
        color="blue",
        show_control_points=True,
        control_color="black",
        ax=None,
        **kwargs,
    ):
        """Plot the Bézier curve. Currently supports 2D and 3D curves.

        Args:
            num_points (int, optional): Number of points to evaluate the curve. Defaults to 200.
            color (str, optional): Color of the curve. Defaults to "blue".
            show_control_points (bool, optional): Whether to show control points in the plot. Defaults to True.
            control_color (str, optional): Color of the control points. Defaults to "black".
            ax (optional): The matplotlib axis to plot the curve on. If None, will create
            a new axis. Otherwise will use the provided axis. Defaults to None.

        Raises:
            ValueError: If the dimension of the curve is not 2 or 3.
        """
        if self.dimension not in [2, 3]:
            raise ValueError(f"Unsupported dimension: {self.dimension}")

        t = np.linspace(0, self.duration, int(num_points * self.duration))
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d" if self.dimension == 3 else None)

        # ax.set_aspect("equal", "datalim")
        points = np.array([self.eval(ti, 0) for ti in t]).transpose()
        ax.plot(*points[: self.dimension], color=color, **kwargs)

        if show_control_points:
            ax.plot(*self.nodes[: self.dimension], "o--", color=control_color)


# Note: BezierTrajectory currently doesn't support yaw control points
class BezierTrajectory:
    def __init__(self, curve_list: list[BezierCurve]):
        self.curve_list = curve_list
        self.num_pieces = len(curve_list)
        self.control_points_list = [curve.nodes for curve in curve_list]
        self.duration_list = [curve.duration for curve in curve_list]
        self.total_time = sum(self.duration_list)

    @classmethod
    def from_control_points(
        cls, control_points_list: list[list[list[float]]], duration_list=None
    ):
        curve_list = []
        for i in range(len(control_points_list)):
            try:
                control_points = np.array(control_points_list[i])
            except ValueError:
                raise ValueError(f"Piece {i} is invalid. Check for dimension mismatch.")
            if i > 0 and control_points.shape[0] != curve_list[-1].dimension:
                raise ValueError(
                    f"Piece {i} has a different dimension than the previous piece."
                )
            max_param = duration_list[i] if duration_list is not None else None
            curve_list.append(BezierCurve.from_nodes(control_points, max_param))
        return cls(curve_list)

    @classmethod
    def from_json(cls, json_file: str):
        f = open(json_file)
        json_object = json.load(f)
        control_points_list = json_object.get("control_points", None)
        if control_points_list is None:
            raise ValueError("control_points key is missing in the JSON file.")
        parameter_list = json_object.get("parameters", None)
        return cls.from_control_points(control_points_list, parameter_list)

    def eval(self, parameter: float, derivative_degree: int = 0):
        if parameter < 0 or parameter > self.total_time:
            raise ValueError(
                f"Parameter {parameter} is outside of [0, {self.total_time}]."
            )

        piece_idx = 0
        tolerance = 1e-10  # Define a small tolerance value
        while parameter - self.duration_list[piece_idx] > tolerance:
            parameter -= self.duration_list[piece_idx]
            parameter = math.floor(parameter * 10**10) / 10**10
            piece_idx += 1

        return self.curve_list[piece_idx].eval(
            parameter, derivative_degree=derivative_degree
        )

    def visualize(
        self,
        derivatives=None,
        show_plot=True,
        show_gradient=False,
        resolution=20,
        ax=None,
        **kwargs,
    ):
        """Visualizes the piecewise Bézier curve.

        Args:
            derivatives (list, optional): List of derivatives to visualize. Defaults to None.
            show_plot (bool, optional): Whether to display the plot. Defaults to True. Set to False if you
            want to use this function as a helper and display the plot later.
            color (tuple, optional): Color of the curve in tuples of three floats in [0, 1]. Uses a random color
            if not provided. Defaults to None (will use random color).
            show_gradient (bool, optional): Whether to show the color gradient.
            Showing the color gradient makes the rendering much slower. Defaults to False.
            resolution (int, optional): Number of points per 1 in t. Defaults to 20.
            Increasing the resolution will make the gradient smoother, but will also increase the rendering time.
            **kwargs: Additional keyword arguments to pass to the plot function.

        """
        color = kwargs.get("color", "blue")
        label = kwargs.get("label", None)
        if derivatives is None:
            derivatives = [0]
        dim = self.curve_list[0].dimension

        for d in derivatives:
            if ax is None:
                fig = plt.figure()
                axis = fig.add_subplot(111, projection="3d" if dim == 3 else None)
            else:
                axis = ax

            # change this parameter to increase/decrease resolution
            points_count = int(resolution * self.total_time)
            t = np.linspace(0, self.total_time, points_count)
            t[-1] = self.total_time
            points = np.array([self.eval(ti, d) for ti in t]).transpose()

            if show_gradient:
                if len(color) == 4:  # if color is RGBA
                    color = color[:3]

                alphas = np.linspace(0.1, 1, points_count - 1)

                for i in range(points_count - 1):
                    axis.plot(
                        *points[:dim, i : i + 2],
                        color=color,
                        alpha=alphas[i],
                    )

            else:
                axis.plot(*points[:dim], color=color, label=label)

            title = (
                f"{d}-th derivative for Bézier trajectory"
                if d != 0
                else "Original Bézier trajectory"
            )
            axis.set_title(title)

            if show_plot:
                plt.show()
                plt.close(fig)
                axis = ax


if __name__ == "__main__":
    # Example usage

    a = 0.9
    b = 0.5
    c = 0.5

    # Define the control points for each piece of the trajectory

    # BezierCurve 1 with control points at (0, 0, 0), (0, 0, 0), (1, a, 0), (1, 0, 0)
    control_pts1 = [[0, 0, 1, 1], [0, 0, a, 0], [0, 0, 0, 0]]

    # Bezier Curve 2 with control points at (1, 0, 0), (1, -a, 0), (b, -c, 0), (0, 0, 0)
    control_pts2 = [[1, 1, b, 0], [0, -a, -c, 0], [0, 0, 0, 0]]

    # Bezier Curve 3 with control points at (0, 0, 0), (-b, c, 0), (-1, a, 0), (-1, 0, 0)
    control_pts3 = [[0, -b, -1, -1], [0, c, a, 0], [0, 0, 0, 0]]

    # Bezier Curve 4 with control points at (-1, 0, 0), (-1, -a, 0), (0, 0, 0), (0, 0, 0)
    control_pts4 = [[-1, -1, 0, 0], [0, -a, 0, 0], [0, 0, 0, 0]]

    # Plot one curve
    curve = BezierCurve.from_nodes(np.array(control_pts1))
    curve.plot()
    plt.show()

    # Plot the entire trajectory
    control_pts_list = [control_pts1, control_pts2, control_pts3, control_pts4]
    bezier_traj = BezierTrajectory.from_control_points(control_pts_list)
    # Alternatively, load from json
    bezier_traj = BezierTrajectory.from_json(
        "crazyflie_examples/crazyflie_examples/data/figure8_bezier.json"
    )
    bezier_traj.visualize(derivatives=[0], show_plot=True)
