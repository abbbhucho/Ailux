from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import json, os
import faiss
import argparse

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

with open(DATA_DIR / "examples_100000_with_safe.json") as f:
    examples = json.load(f)

descriptions = [e["task"] for e in examples]
commands = [e["command"] for e in examples]

print("Encoding 100k descriptions... (one-time)")
embeddings = model.encode(descriptions, convert_to_tensor=True)

# Save to disk

os.makedirs(DATA_DIR, exist_ok=True)
np.save(DATA_DIR / "desc_embeddings.npy", embeddings.cpu().numpy())

with open(DATA_DIR / "commands.json", "w") as f:
    json.dump(commands, f)



###
# FAISS for Ultra-Fast Search // FAISS (Facebook AI Similarity Search)
###

# Load embeddings as float32 (required for FAISS)
embeddings = np.load(DATA_DIR / "desc_embeddings.npy").astype("float32")
d = embeddings.shape[1]  # embedding dimension

# Build a basic L2 index
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Save FAISS index
MODELS_DIR = BASE_DIR / "models"
parser = argparse.ArgumentParser(description="Precompute sentence embeddings and FAISS index.")
parser.add_argument("--rebuild", action="store_true",
                    help="Rebuild embeddings from scratch")
parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2",
                    help="SentenceTransformer model to use")
parser.add_argument("--data", type=str, default=str(DATA_DIR / "commands.json"),
                    help="Path to JSON data file")
parser.add_argument("--faiss", type=str, default=str(MODELS_DIR / "faiss.index"),
                    help="Path to save FAISS index")
# parser.add_argument("--faiss", default=str(MODELS_DIR / "faiss.index"),
#                     help="Path to save FAISS index")
args = parser.parse_args()


faiss_path = Path(args.faiss)
faiss_path.parent.mkdir(parents=True, exist_ok=True)  # make sure dir exists

# out_faiss = Path(args.faiss)
# out_faiss.parent.mkdir(parents=True, exist_ok=True)  # make sure folder exists
faiss.write_index(index, str(faiss_path))
print(f"FAISS index saved to : {faiss_path}")

print("Preprocessing complete. now use main.py for faster control")
