from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Qiliang/bart-large-cnn-samsum-ChatGPT_v3")
model = AutoModelForSeq2SeqLM.from_pretrained(
    "Qiliang/bart-large-cnn-samsum-ChatGPT_v3"
)


def generative_gpt_bart_large(user_input):
    if "friday" in user_input:
        user_input = user_input.replace("friday", "")

    if "tell me about" in user_input:
        user_input = user_input.replace("tell me about", "what is")
    if "tell me about" in user_input and "friday" in user_input:
        user_input = user_input.replace("tell me about", "what is").replace(
            "friday", ""
        )

    if "describe" in user_input:
        user_input = user_input.replace("describe", "what is")
    if "describe" in user_input and "friday" in user_input:
        user_input = user_input.replace("describe", "what is").replace("friday", "")

    user_input = user_input.capitalize()

    input_text = f"{user_input}?"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_length=142)

    text = tokenizer.decode(outputs[0])

    clean_text = text.replace("</s>", " ").replace("<s>", " ").replace("None", " ")

    return clean_text
