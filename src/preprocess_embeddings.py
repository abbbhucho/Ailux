# src/preprocess_embeddings.py
from pathlib import Path
import argparse, json
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle, scipy.sparse as sp
import faiss

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

parser = argparse.ArgumentParser(description="Build TF-IDF, embeddings, and FAISS index")
parser.add_argument("--rebuild", action="store_true", help="Rebuild from scratch")
parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="ST model")
parser.add_argument("--data", type=str, default=str(DATA_DIR / "commands.json"), help="task->cmd json")
parser.add_argument("--faiss", type=str, default=str(MODELS_DIR / "faiss.index"), help="FAISS index path")
args = parser.parse_args()

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# 1) Load dataset (expects [{"task": "...", "command": "..."}])
with open(args.data, "r", encoding="utf-8") as f:
    rows = json.load(f)
descriptions = [r.get("task","").strip() for r in rows]
commands = [r.get("command","").strip() for r in rows]

# Persist canonical files used at runtime
with open(DATA_DIR / "commands.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

# 2) TF-IDF (lexical first stage)
print("Building TF-IDF…")
vectorizer = TfidfVectorizer(ngram_range=(1,3), min_df=1)
X = vectorizer.fit_transform(descriptions)
pickle.dump(vectorizer, open(MODELS_DIR / "tfidf.pkl", "wb"))
sp.save_npz(MODELS_DIR / "tfidf_X.npz", X)

# 3) Embeddings (semantic second stage) + unit norm
print(f"Encoding {len(descriptions)} descriptions with {args.model} …")
model = SentenceTransformer(args.model)
emb = model.encode(descriptions, convert_to_numpy=True, batch_size=256, show_progress_bar=True)
emb = normalize(emb, axis=1)              # unit-length
np.save(DATA_DIR / "desc_embeddings.npy", emb.astype("float32"))

# 4) FAISS (IndexFlatIP on normalized vectors => cosine)
print("Building FAISS index…")
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb.astype("float32"))
faiss_path = Path(args.faiss)
faiss_path.parent.mkdir(parents=True, exist_ok=True)
faiss.write_index(index, str(faiss_path))
print(f"Done. Wrote:\n- {DATA_DIR/'desc_embeddings.npy'}\n- {MODELS_DIR/'tfidf.pkl'}\n- {MODELS_DIR/'tfidf_X.npz'}\n- {faiss_path}")