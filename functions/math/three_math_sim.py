import sys
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import matplotlib

matplotlib.use("TkAgg")


def plot_custom_function(user_function_str):
    x = sp.symbols("x")
    y = sp.symbols("y")

    user_function_expr = sp.sympify(user_function_str)
    user_function = sp.lambdify((x, y), user_function_expr, "numpy")

    x_values = np.linspace(-10, 10, 400)
    y_values = np.linspace(-10, 10, 400)

    y_custom = user_function(x_values, y_values)

    fig = plt.figure(figsize=(16, 7))  # Adjust the figure size here

    # Adjust the width of the 2D subplot here
    ax2d = fig.add_subplot(131)

    ax3d = fig.add_subplot(122, projection="3d")

    fig.patch.set_facecolor("black")

    ax2d.plot(x_values, y_custom, color="white", linewidth=2)
    ax2d.set_xlabel("x")
    ax2d.set_ylabel("f(x)")
    ax2d.set_title("2D Plot of Function", color="white")
    ax2d.set_facecolor("black")

    ax2d.xaxis.label.set_color("white")
    ax2d.yaxis.label.set_color("white")
    ax2d.tick_params(axis="x", colors="white")
    ax2d.tick_params(axis="y", colors="white")

    X, Y = np.meshgrid(x_values, x_values)
    Z = user_function(X, Y)

    surf = ax3d.plot_surface(
        X, Y, Z, cmap="viridis", rstride=10, cstride=10, antialiased=True
    )
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Z")
    ax3d.set_title("3D Plot of Function", color="white")

    ax3d.set_facecolor("black")
    ax3d.xaxis.pane.fill = False
    ax3d.yaxis.pane.fill = False
    ax3d.zaxis.pane.fill = False
    ax3d.xaxis._axinfo["grid"]["color"] = "white"
    ax3d.yaxis._axinfo["grid"]["color"] = "white"
    ax3d.zaxis._axinfo["grid"]["color"] = "white"
    ax3d.xaxis.label.set_color("white")
    ax3d.yaxis.label.set_color("white")
    ax3d.zaxis.label.set_color("white")
    ax3d.tick_params(axis="x", colors="white")
    ax3d.tick_params(axis="y", colors="white")
    ax3d.tick_params(axis="z", colors="white")
    ax3d.view_init(elev=30, azim=45)

    plt.tight_layout()
    plt.show()


def create_simlulation_function(user_input):
    cleaned_function_description = user_input
    if cleaned_function_description:
        return plot_custom_function(cleaned_function_description)
    else:
        pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <user_function_description>")
    else:
        user_function_description = sys.argv[1]
        create_simlulation_function(user_function_description)
