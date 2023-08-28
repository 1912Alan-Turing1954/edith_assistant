# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")


# def generative_with_t5(input_text):
#     input_text = input_text.lower()

#     if "friday" in input_text.lower():
#         input_text = input_text.replace("friday", "")

#     _prompt = f"Please answer the following question in detail. {input_text}?"
#     _prompt_yes_no = f"Answer the following yes/no question. {input_text}?"

#     def type_(input_text):
#         if input_text.startswith("do"):
#             return _prompt_yes_no
#         else:
#             return _prompt

#     # tokenize the input text
#     input_ids = tokenizer(type_(input_text), return_tensors="pt").input_ids
#     outputs = model.generate(input_ids, max_length=1024, do_sample=False)

#     # Decode the generated translation
#     decoded_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     return decoded_text


# print(generative_with_t5("what is plasma"))

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-xl"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Save the model and tokenizer to a local directory
model.save_pretrained("./model/flan-t5-xl")
tokenizer.save_pretrained("./model/flan-t5-xl")
