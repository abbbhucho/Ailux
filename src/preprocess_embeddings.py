from sentence_transformers import SentenceTransformer
import numpy as np
import json, os
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("src/data/examples_100000_with_safe.json") as f:
    examples = json.load(f)

descriptions = [e["task"] for e in examples]
commands = [e["command"] for e in examples]

print("Encoding 100k descriptions... (one-time)")
embeddings = model.encode(descriptions, convert_to_tensor=True)

# Save to disk
os.makedirs("src/data", exist_ok=True)
np.save("src/data/desc_embeddings.npy", embeddings.cpu().numpy())

with open("src/data/commands.json", "w") as f:
    json.dump(commands, f)



###
# FAISS for Ultra-Fast Search // FAISS (Facebook AI Similarity Search)
###

# Load embeddings as float32 (required for FAISS)
embeddings = np.load("src/data/desc_embeddings.npy").astype("float32")
d = embeddings.shape[1]  # embedding dimension

# Build a basic L2 index
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "src/models/faiss_index.faiss")
print("FAISS index built and saved!")

print("Preprocessing complete. now use main.py for faster control")
