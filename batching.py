import os
import json

import messages
import util

DB_PATH = "data/message-db.json"
BATCH_PATH = "data/message-batches.json"

def batch_messages(tokenizer):
    if os.path.isfile(BATCH_PATH) and os.path.getmtime(BATCH_PATH) > os.path.getmtime(DB_PATH):
        with open(BATCH_PATH, "r") as f:
            return json.load(f)

    msg_db, _ = messages.load()

    batches = []
    curr_batch = []

    for line in msg_db:
        curr_batch.append(line)

        curr_rendered = messages.render_messages(curr_batch)

        amnt_tokens = len(tokenizer(curr_rendered, max_length=2*tokenizer.model_max_length, truncation=True).tokens())

        if amnt_tokens > tokenizer.model_max_length:
            batches.append(messages.render_messages(curr_batch))
            
            curr_batch = []
    
    util.write_to_path(BATCH_PATH, json.dumps(batches))

    return batches