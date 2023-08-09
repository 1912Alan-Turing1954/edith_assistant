# from transformers import T5Tokenizer, T5ForConditionalGeneration

# tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
# model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")


# def generate_text(user_input):
#     input_text = user_input
#     input_ids = tokenizer(input_text, return_tensors="pt").input_ids

#     # Update max_length to max_new_tokens
#     max_new_tokens = 150  # Set the desired maximum length of the generated text
#     outputs = model.generate(input_ids, max_new_tokens=max_new_tokens)
#     response = tokenizer.decode(outputs[0])
#     response = response.replace("<pad>", "").replace("</s>", "")
#     return response


# input_text = input("Enter text to generate: ")
# print(generate_text(input_text))
