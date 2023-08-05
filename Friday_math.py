import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")

# Dictionary to map word representation to numerical values and operators
word_to_num = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
    "thirty": "30",
    "forty": "40",
    "fifty": "50",
    "sixty": "60",
    "seventy": "70",
    "eighty": "80",
    "ninety": "90",
    "hundred": "100",
    "thousand": "1000",
    "million": "1000000",
}

word_to_operator = {
    "plus": "+",
    "add": "+",
    "sum": "+",
    "and": "+",
    "minus": "-",
    "subtract": "-",
    "difference": "-",
    "times": "*",
    "multiply": "*",
    "multiplied": "*",
    "product": "*",
    "divided": "/",
    "divide": "/",
    "quotient": "/",
}


def replace_words_with_values(text):
    # Tokenize the text and replace words with numerical values and operators
    tokens = word_tokenize(text.lower())
    expression = ""
    for token in tokens:
        if token in word_to_num:
            expression += word_to_num[token] + " "
        elif token in word_to_operator:
            expression += word_to_operator[token] + " "
    return expression.strip()


def solve_math_expression(expression):
    try:
        # Safely evaluate the mathematical expression using 'eval'
        result = eval(expression)
        return result
    except:
        return None


def main():
    user_input = input("Enter your word math expression (type 'exit' to quit): ")

    expression = replace_words_with_values(user_input)
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
