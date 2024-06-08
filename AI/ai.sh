#!/bin/bash

ask_question() {
    question="$1"
    command="ollama run llama2 '$question'"
    result=$(eval "$command" 2>&1)
    if [ $? -eq 0 ]; then
        echo "$result" | tr -d '\n'
    else
        echo "Error: $result" | tr -d '\n'
    fi
}

# Prompt the user for a question
echo -n "Ask a question: "
read question

# Call the function to ask the question
response=$(ask_question "$question")

# Print the response
echo "$response"

