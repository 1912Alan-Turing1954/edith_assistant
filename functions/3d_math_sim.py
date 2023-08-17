import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def extract_function_from_input(input_str):
    input_str = input_str.replace("simulate the function of", "")

    replacements = {
        "x squared": "x**2",
        "x square": "x**2",
        "x cubed": "x**3",
        "x cube": "x**3",
        "x to the power of 2": "x**2",
        "x to the power of 3": "x**3",
        "sine of x": "np.sin(x)",
        "cosine of x": "np.cos(x)",
        "tangent of x": "np.tan(x)",
        "square root of x": "np.sqrt(x)",
        "absolute value of x": "np.abs(x)",
        "logarithm base 10 of x": "np.log10(x)",
        "natural logarithm of x": "np.log(x)",
        "exponential of x": "np.exp(x)",
        "inverse sine of x": "np.arcsin(x)",
        "inverse cosine of x": "np.arccos(x)",
        "inverse tangent of x": "np.arctan(x)",
        "addition": "+",
        "subtraction": "-",
        "multiplication": "*",
        "division": "/",
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided by": "/",
        "greater than": ">",
        "less than": "<",
        "equal to": "==",
        "not equal to": "!=",
        "y squared": "y**2",
        "y square": "y**2",
        "y cubed": "y**3",
        "y cube": "y**3",
        "y to the power of 2": "y**2",
        "y to the power of 3": "y**3",
        "sine of y": "np.sin(y)",
        "cosine of y": "np.cos(y)",
        "tangent of y": "np.tan(y)",
        "square root of y": "np.sqrt(y)",
        "absolute value of y": "np.abs(y)",
        "logarithm base 10 of y": "np.log10(y)",
        "natural logarithm of y": "np.log(y)",
        "exponential of y": "np.exp(y)",
        "inverse sine of y": "np.arcsin(y)",
        "inverse cosine of y": "np.arccos(y)",
        "inverse tangent of y": "np.arctan(y)",
    }

    for keyword, replacement in replacements.items():
        input_str = input_str.replace(keyword, replacement)

    return input_str


def create_3d_rotation_animation(func, num_frames=120, rotation_speed=0.1):
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)

    fig = plt.figure(figsize=(10, 8), facecolor="black")
    ax = fig.add_subplot(111, projection="3d")

    for i in range(num_frames):
        ax.cla()
        t = (i * rotation_speed) % 360
        X_rotated = X * np.cos(np.radians(t)) - Y * np.sin(np.radians(t))
        Y_rotated = X * np.sin(np.radians(t)) + Y * np.cos(np.radians(t))
        Z_rotated = func(X_rotated, Y_rotated)

        surface = ax.plot_surface(
            X_rotated,
            Y_rotated,
            Z_rotated,
            cmap="viridis",
            edgecolor="none",
            antialiased=True,
        )

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("3D Function Slow Rotation")

        ax.grid(False)
        ax.w_xaxis.pane.fill = False
        ax.w_yaxis.pane.fill = False
        ax.w_zaxis.pane.fill = False

        ax.set_facecolor("black")

        ax.xaxis._axinfo["grid"]["color"] = "white"
        ax.yaxis._axinfo["grid"]["color"] = "white"
        ax.zaxis._axinfo["grid"]["color"] = "white"

        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.zaxis.label.set_color("white")

        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.tick_params(axis="z", colors="white")

        ax.view_init(elev=30, azim=45)

        plt.pause(0.01)

    plt.show()


# Ask user for the input and extract the function from it
user_input = input(
    "Enter a description of the function (e.g., 'simulate the function of x squared'): "
)
extracted_function = extract_function_from_input(user_input)
print("Extracted function:", extracted_function)


# Convert the extracted function text to a Python function
def extracted_function_python(x, y):
    return eval(extracted_function)


# Call the animation function with the extracted function
create_3d_rotation_animation(
    func=extracted_function_python, num_frames=120, rotation_speed=0.1
)
