"""
AI Shell Helper retrieval module
- Prefers FAISS index for fast search
- Falls back to cosine similarity over precomputed numpy embeddings
- Loads SentenceTransformer once and reuses it
"""

import os
import json
import numpy as np

from sentence_transformers import SentenceTransformer

# Optional torch imports only if we need cosine fallback
import torch
from sentence_transformers import util

# Optional FAISS (only used if index file is present)
try:
    import faiss  # type: ignore
    _FAISS_AVAILABLE = True
except Exception:
    _FAISS_AVAILABLE = False

# ---------- Paths ----------
DATA_DIR = "src/data"
MODELS_DIR = "src/models"
COMMANDS_PATH = os.path.join(DATA_DIR, "commands.json")
EMB_PATH = os.path.join(DATA_DIR, "desc_embeddings.npy")
FAISS_PATH = os.path.join(MODELS_DIR, "faiss_index.faiss")

# ---------- Load model once ----------
# You can switch models here if you want to compare
_MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(_MODEL_NAME)

# ---------- Load commands ----------
if not os.path.isfile(COMMANDS_PATH):
    raise FileNotFoundError(
        f"commands.json not found at {COMMANDS_PATH}. "
        "Run preprocess_embeddings.py first to generate it."
    )

with open(COMMANDS_PATH, "r") as f:
    _commands = json.load(f)

# ---------- Choose backend (FAISS > cosine fallback) ----------
_use_faiss = _FAISS_AVAILABLE and os.path.isfile(FAISS_PATH)
_index = None
_desc_embeddings_t = None  # torch tensor for cosine fallback

if _use_faiss:
    # Load FAISS index
    _index = faiss.read_index(FAISS_PATH)
    print(f"Using FAISS index: {_MODEL_NAME} @ {FAISS_PATH}")
else:
    # Fallback: load precomputed embeddings and use cosine similarity
    if not os.path.isfile(EMB_PATH):
        raise FileNotFoundError(
            f"desc_embeddings.npy not found at {EMB_PATH}. "
            "Either build FAISS index or save embeddings via preprocess_embeddings.py."
        )
    _desc_embeddings_np = np.load(EMB_PATH).astype("float32")
    # Move to torch tensor once (CPU is fine; we only do a matrix similarity)
    _desc_embeddings_t = torch.from_numpy(_desc_embeddings_np)
    print(f"Using cosine similarity fallback: {_MODEL_NAME} with {EMB_PATH}")

# ---------- Public API ----------
def get_shell_command(user_input: str) -> str:
    """
    Encode the query and retrieve the best matching command.
    Prefers FAISS if available; otherwise uses cosine similarity over precomputed embeddings.
    """
    if not user_input or not user_input.strip():
        return ""

    if _use_faiss and _index is not None:
        # FAISS path (assumes index built on float32 embeddings; L2 metric by default)
        vec = _model.encode([user_input])[0].astype("float32").reshape(1, -1)
        D, I = _index.search(vec, k=1)
        best_idx = int(I[0][0])
        # Safety for empty index
        if best_idx < 0 or best_idx >= len(_commands):
            return ""
        return _commands[best_idx]

    # Cosine fallback
    query_emb = _model.encode([user_input], convert_to_tensor=True)
    # util.pytorch_cos_sim returns [1, N]; take row 0
    scores = util.pytorch_cos_sim(query_emb, _desc_embeddings_t)[0]
    best_idx = int(torch.argmax(scores).item())
    if best_idx < 0 or best_idx >= len(_commands):
        return ""
    return _commands[best_idx]