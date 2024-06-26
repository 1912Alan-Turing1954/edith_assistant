# # import torch
# # from transformers import pipeline, set_seed

# # # Set seed for reproducibility
# # set_seed(42)

# # # Example usage:
# # messages = [
# #     {
# #         "role": "system",
# #         "content": "",
# #     },
# #     {"role": "user", "content": ""},
# # ]


# # def generate_responses(
# #     messages,
# #     model_name="Qwen/Qwen2-7B-Instruct",
# #     max_new_tokens=50,
# #     temperature=0.7,
# #     top_k=50,
# #     top_p=0.9,
# #     repetition_penalty=1.0,
# # ):
# #     """
# #     Generates responses to a list of messages using a specified model.

# #     Args:
# #         messages (list): A list of dictionaries where each dictionary contains keys 'role' and 'content'.
# #         model_name (str): The name of the model to use for text generation. Default is "Qwen/Qwen2-7B-Instruct".
# #         max_new_tokens (int): The maximum number of tokens to generate for each response. Default is 50.
# #         device (int or str): The GPU device to run the model on. Use -1 for CPU, 0 or 'cuda:0' for GPU. Default is 0.

# #     Returns:
# #         list: A list of generated responses.
# #     """
# #     pipe = pipeline("text-generation", model=model_name)
# #     # pipe = pipeline(
# #     #     "text-generation",
# #     #     model="microsoft/Phi-3-mini-4k-instruct",
# #     #     trust_remote_code=True,
# #     #     device=device,
# #     # )
# #     responses = pipe(
# #         messages,
# #         max_new_tokens=max_new_tokens,
# #         temperature=temperature,
# #         top_k=top_k,
# #         top_p=top_p,
# #         repetition_penalty=repetition_penalty,
# #     )
# #     return [response["generated_text"] for response in responses]


# # def edith_ai(input_text):
# #     with open("Data/boot_personality_prompt.txt", "r") as f:
# #         prompt = f.read()
# #         print(prompt)

# #     messages[1]["content"] = ""
# #     messages[0]["content"] += prompt
# #     messages[1]["content"] += input_text

# #     responses = generate_responses(messages)
# #     for response in responses:
# #         print(response)

# #     # Debugging statement
# #     print("User input:", input_text)

# #     return response[2]["content"]


# # if __name__ == "__main__":
# #     # Determine device availability
# #     # device = 0 if torch.cuda.is_available() else 1  # Use GPU if available, else CPU

# #     while True:
# #         user_input = input("input: ")
# #         edith_ai(user_input)
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Model and tokenizer initialization
# model_id = "/"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(model_id)

# # Check if CUDA is available and move model to GPU if possible
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Example input messages
# messages = [
#     {
#         "role": "user",
#         "content": "I'm feeling really down today. Nothing seems to be going right.",
#     },
# ]

# batch_size = 1  # Reduce batch size
# input_ids = tokenizer.encode(
#     messages[0]["content"],
#     return_tensors="pt",
#     max_length=512,
#     truncation=True,
#     add_special_tokens=True,
# ).to(device)

# outputs = model.generate(
#     input_ids,
#     max_length=256,
#     pad_token_id=tokenizer.eos_token_id,
#     do_sample=True,
#     temperature=0.9,
#     top_p=0.9,
#     batch_size=batch_size,  # Specify reduced batch size
# )


# # Decode and print the generated response
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print("Generated response:", response)

import torch
from transformers import LlamaTokenizer, LlamaForCausalLM

## v2 models
model_path = "openlm-research/open_llama_7b_v2"
# model_path = 'openlm-research/open_llama_7b_v2'

## v1 models
# model_path = 'openlm-research/open_llama_3b'
# model_path = 'openlm-research/open_llama_7b'
# model_path = 'openlm-research/open_llama_13b'

# Initialize LLAMA tokenizer and model
tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(model_path)

prompt = "What is the largest animal?\n"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

generation_output = model.generate(input_ids=input_ids, max_new_tokens=32)
print(tokenizer.decode(generation_output[0]))
