import sys
from matplotlib.widgets import Button
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from mpl_toolkits.mplot3d import Axes3D

# Use a high-tech style for the plots
plt.style.use("dark_background")


def plot_custom_function(user_function_str):
    x = sp.symbols("x")
    y = sp.symbols("y")

    user_function_expr = sp.sympify(user_function_str)
    user_function = sp.lambdify((x, y), user_function_expr, "numpy")

    x_values = np.linspace(-10, 10, 400)
    y_values = np.linspace(-10, 10, 400)

    y_custom = user_function(x_values, y_values)

    fig = plt.figure(figsize=(17, 8))

    # Adjust the width of the 2D subplot here
    ax2d = fig.add_subplot(131)

    ax3d = fig.add_subplot(122, projection="3d")

    ax2d.plot(
        x_values, y_custom, color="cyan", linewidth=2, linestyle="--"
    )  # Dashed line for 2D
    ax2d.set_xlabel("x", color="white")
    ax2d.set_ylabel("f(x)", color="white")
    ax2d.set_title("2D Plot of Function", color="cyan")

    # Add transparent grid lines to the 2D plot
    ax2d.grid(True, linestyle="--", linewidth=0.5, color="white", alpha=0.5)

    X, Y = np.meshgrid(x_values, y_values)
    Z = user_function(X, Y)

    surf = ax3d.plot_surface(
        X,
        Y,
        Z,
        cmap="viridis",
        rstride=10,
        cstride=10,
        antialiased=True,
        alpha=0.7,  # Adjust colormap and alpha
    )
    ax3d.set_xlabel("X", color="white")
    ax3d.set_ylabel("Z", color="white")
    ax3d.set_zlabel("Y", color="white")
    ax3d.set_title("3D Plot of Function", color="cyan")

    def on_scroll(event):
        x_center, y_center = event.xdata, event.ydata

        if event.button == "up":
            scale_factor = 1.1
        elif event.button == "down":
            scale_factor = 1 / 1.1
        else:
            scale_factor = 1.0

        if event.inaxes == ax2d:
            ax2d.set_xlim(
                x_center - (x_center - ax2d.get_xlim()[0]) * scale_factor,
                x_center + (ax2d.get_xlim()[1] - x_center) * scale_factor,
            )
            ax2d.set_ylim(
                y_center - (y_center - ax2d.get_ylim()[0]) * scale_factor,
                y_center + (ax2d.get_ylim()[1] - y_center) * scale_factor,
            )
        elif event.inaxes == ax3d:
            ax3d.set_xlim(
                x_center - (x_center - ax3d.get_xlim()[0]) * scale_factor,
                x_center + (ax3d.get_xlim()[1] - x_center) * scale_factor,
            )
            ax3d.set_ylim(
                y_center - (y_center - ax3d.get_ylim()[0]) * scale_factor,
                y_center + (ax3d.get_ylim()[1] - y_center) * scale_factor,
            )
        plt.draw()

    fig.canvas.mpl_connect("scroll_event", on_scroll)

    # Make the 3D plot movable
    ax3d.mouse_init()

    plt.tight_layout()
    plt.show()


def create_simulation_function(user_input):
    cleaned_function_description = user_input
    if cleaned_function_description:
        return plot_custom_function(cleaned_function_description)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <user_function_description>")
    else:
        user_function_description = sys.argv[1]
        create_simulation_function(user_function_description)


create_simulation_function(indefinite_integral)
