from transformers import DataCollatorForLanguageModeling, TrainingArguments, Trainer
from datasets import Dataset

import batching
import llm


print("Loading tokenizer and model...")
tokenizer, model = llm.load()


print("Batching messages...")
batches = batching.batch_messages(tokenizer)
print("Loaded", len(batches), "batches!")


print("Tokenizing dataset...")
dataset = Dataset.from_dict({'text': batches})

def tokenize_function(examples):
    res = tokenizer(examples["text"], padding='max_length', truncation=True)
    return res

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset.set_format('torch', columns=['input_ids'])


print("Training! Press CTRL-C to exit")
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False,
)

while 1:
    training_args = TrainingArguments(
        output_dir='./results',
        per_device_train_batch_size=3,
        num_train_epochs=1,
        weight_decay=0.01
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_dataset,
    )

    trainer.train()

    trainer.save_model()
