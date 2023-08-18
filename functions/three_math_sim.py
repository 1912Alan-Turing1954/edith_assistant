import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import matplotlib
from word2number import w2n

matplotlib.use("TkAgg")

patterns = [
    "simulate the function of",
    "simulate the function",
    "simulate function",
    "simulate",
    "plot the function of",
    "plot the function",
    "display the function",
]


def convert_textual_numbers(input_str):
    words = input_str.lower().split()  # Split input into words
    numerical_words = []

    for word in words:
        try:
            num = w2n.word_to_num(word)
            numerical_words.append(str(num))
        except ValueError:
            numerical_words.append(word)  # Keep non-convertible words as they are

    processed_input = " ".join(numerical_words)
    return processed_input.strip()


print(convert_textual_numbers("one plus one"))


def extract_function_from_input(input_str):
    for pattern in patterns:
        if pattern in input_str:
            input_str = input_str.replace(pattern, "")
        else:
            input_str = input_str

    replacements = {
        "cosine of x": "cos(x)",
        "sine of x": "sin(x)",
        "tangent of x": "tan(x)",
        "square root of x": "sqrt(x)",
        "logarithm base 10 of x": "log10(x)",
        "natural logarithm of x": "log(x)",
        "exponential of x": "exp(x)",
        "absolute value of x": "abs(x)",
        "cosine of y": "cos(y)",
        "sine of y": "sin(y)",
        "tangent of y": "tan(y)",
        "square root of y": "sqrt(y)",
        "logarithm base 10 of y": "log10(y)",
        "natural logarithm of y": "log(y)",
        "exponential of y": "exp(y)",
        "absolute value of y": "abs(y)",
        "x squared": "x**2",
        "x cubed": "x**3",
        "y squared": "y**2",
        "y cubed": "y**3",
        "equals": "==",
        "equal to": "==",
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided by": "/",
        "greater than": ">",
        "less than": "<",
        "not equal to": "!=",
    }
    for keyword, replacement in replacements.items():
        input_str = input_str.replace(keyword, replacement)
    return input_str.strip()


def plot_custom_function(user_function_str):
    x = sp.symbols("x")
    y = sp.symbols("y")

    user_function_expr = sp.sympify(user_function_str)
    user_function = sp.lambdify((x, y), user_function_expr, "numpy")

    x_values = np.linspace(-10, 10, 400)
    y_values = np.linspace(-10, 10, 400)

    y_custom = user_function(x_values, y_values)

    fig = plt.figure(figsize=(18, 8))
    ax2d = fig.add_subplot(121)
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
    cleaned_function_description = extract_function_from_input(user_input)
    cleaned_function_description = convert_textual_numbers(cleaned_function_description)
    if cleaned_function_description:
        return plot_custom_function(cleaned_function_description)
    else:
        pass


create_simlulation_function("simulate function sine of x plus one")
