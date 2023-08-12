from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")


def generative_with_t5(input_text):
    input_text = input_text.lower()

    _prompt = f"Please answer to the following question and elaborate. {input_text}?"

    # tokenize the input text
    input_ids = tokenizer(_prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=1024)

    # Decode the generated translation
    decoded_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return decoded_text
