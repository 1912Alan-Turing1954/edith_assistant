import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import json

matplotlib.use("TkAgg")

with open("./data/intents.json") as f:
    intents = json.load(f)


def extract_function_from_input(input_str):
    input_str = input_str.replace("{string}", "")

    for intent in intents["intents"]:
        if intent["tag"] == "simulate_interference":
            for pattern in intent["patterns"]:
                if pattern in input_str:
                    input_str = input_str.replace(pattern, "").strip()

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
        "equals": "==",
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


def create_static_3d_plot(func):
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)

    fig = plt.figure(figsize=(10, 8), facecolor="black")
    ax = fig.add_subplot(111, projection="3d")

    surface = ax.plot_surface(
        X,
        Y,
        Z,
        cmap="viridis",
        edgecolor="none",
        antialiased=True,
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Function Static Plot")

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

    plt.show()


def create_simlulation_function(user_input):
    extracted_function = extract_function_from_input(user_input)

    def extracted_function_python(x, y):
        return eval(extracted_function)

    create_static_3d_plot(extracted_function_python)
