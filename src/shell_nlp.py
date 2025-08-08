from sentence_transformers import SentenceTransformer, util
import json
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2') # replaced by paraphrase-MiniLM-L6-v2 (as its good, but tuned mostly for paraphrase) instead this one is better for diverse search queries

# Load precomputed data
desc_embeddings = np.load("src/data/desc_embeddings.npy")
desc_embeddings = util.tensor(desc_embeddings)  # Convert to tensor

with open("src/data/commands.json") as f:
    commands = json.load(f)

# def load_examples(filepath="examples_100000_with_safe.json"):
#     with open(filepath, "r") as f:
#         return json.load(f)

# examples = load_examples()
# commands = [e["command"] for e in examples]
# descriptions = [e["description"] for e in examples]

def get_shell_command(user_input: str):
    query_embedding = model.encode([user_input], convert_to_tensor=True)
    
    cos_scores = util.pytorch_cos_sim(query_embedding, desc_embeddings)[0]
    best_idx = cos_scores.argmax()
    
    return commands[best_idx]
    # description_embeddings = model.encode(descriptions, convert_to_tensor=True)
    
    # scores = util.pytorch_cos_sim(query_embedding, description_embeddings)
    # best_match_idx = scores.argmax()
    # return examples[best_match_idx]["command"]