from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Qiliang/bart-large-cnn-samsum-ChatGPT_v3")
model = AutoModelForSeq2SeqLM.from_pretrained(
    "Qiliang/bart-large-cnn-samsum-ChatGPT_v3"
)

words = ["friday", "explain", "tell me about", "describe", "tell me"]


def generative_gpt_bart_large(user_input):
    for word in words:
        if word in user_input:
            user_input.replace(word, "what is")

    user_input = user_input.capitalize()

    input_text = f"{user_input}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, do_sample=True)

    text = tokenizer.decode(outputs[0])

    clean_text = text.replace("</s>", " ").replace("<s>", " ").replace("None", " ")

    return clean_text
