import random

import llm
import messages

_, user_db = messages.load()

tokenizer, model = llm.load()


def complete(prompt):
    model_inputs = tokenizer([prompt], return_tensors="pt")

    generated_ids = model.generate(**model_inputs, max_new_tokens=100, do_sample=True)

    decoded_data = tokenizer.batch_decode(generated_ids)[0]

    return decoded_data

def generate_chat():
    return complete(random.choice(user_db.names()) + ": ")

if __name__ == '__main__':
    print(generate_chat())
