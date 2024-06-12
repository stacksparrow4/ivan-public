import os

from transformers import AutoTokenizer, AutoModelForCausalLM

from constants import MODEL_NAME

def load():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    if os.path.isfile("results/model.safetensors"):
        return tokenizer, AutoModelForCausalLM.from_pretrained("./results")

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    return tokenizer, model