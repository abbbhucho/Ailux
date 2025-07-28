from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def load_examples(filepath="examples_100000_with_safe.json"):
    with open(filepath, "r") as f:
        return json.load(f)

examples = load_examples()
commands = [e["command"] for e in examples]
descriptions = [e["description"] for e in examples]

def get_shell_command(user_input):
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    description_embeddings = model.encode(descriptions, convert_to_tensor=True)
    
    scores = util.pytorch_cos_sim(query_embedding, description_embeddings)
    best_match_idx = scores.argmax()
    return examples[best_match_idx]["command"]