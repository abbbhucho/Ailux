#!/bin/bash
ls -lh ../src/data/commands.json
ls -lh ../src/data/desc_embeddings.npy
ls -lh ../src/models/faiss.index

# quick load test:
python - <<'PY'
import json, faiss, numpy as np, pathlib
print("cmds:", len(json.load(open("../src/data/commands.json"))))
print("emb:", np.load("../src/data/desc_embeddings.npy").shape)
print("faiss:", isinstance(faiss.read_index("../src/models/faiss.index"), faiss.Index))
PY
