from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")


def generative_with_t5(input_text):
    input_text = input_text.lower()

    if "friday" in input_text.lower():
        input_text = input_text.replace("friday", "")

    _prompt = f"Please answer the following question in detail. {input_text}?"
    _prompt_yes_no = f"Answer the following yes/no question. {input_text}?"

    def type_(input_text):
        if (
            input_text.startswith("do")
            or input_text.startswith("does")
            or input_text.startswith("is")
        ):
            return _prompt_yes_no
        else:
            return _prompt

    # tokenize the input text
    input_ids = tokenizer(type_(input_text), return_tensors="pt").input_ids
    outputs = model.generate(
        input_ids,
        do_sample=True,
        max_new_tokens=200,
        min_length=50,
        temperature=0.7,
        top_k=0,
        no_repeat_ngram_size=4,  # Avoid repeating the same bigram
    )

    # Decode the generated translation
    decoded_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    clean_text = decoded_text.capitalize().replace("br>", "").replace("br>", "").strip()

    return clean_text
