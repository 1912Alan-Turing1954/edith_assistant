import nltk
from nltk.tokenize import word_tokenize
from sympy import sympify

nltk.download('punkt')

def extract_expression(text):
    # Tokenize the text and identify the mathematical expression
    tokens = word_tokenize(text)
    expression = ""
    for i in range(len(tokens)):
        if tokens[i] == "is" and i + 1 < len(tokens):
            expression = " ".join(tokens[i + 1:])
            break
        elif tokens[i] == "what" and i + 2 < len(tokens) and tokens[i + 1] == "is":
            expression = " ".join(tokens[i + 2:])
            break
        else:
            expression = " ".join(tokens)
    return expression

def solve_math_expression(expression):
    try:
        # Evaluate the mathematical expression
        result = sympify(expression)
        return result
    except:
        return None

def main():
    print("Welcome to the Math Equation Solver!")
    while True:
        user_input = input("Enter your math question or equation (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        expression = extract_expression(user_input)
        if expression:
            answer = solve_math_expression(expression)
            if answer is not None:
                print(f"Answer: {answer}")
            else:
                print("Invalid math expression.")
        else:
            print("Unable to identify the math expression.")

if __name__ == "__main__":
    main()
