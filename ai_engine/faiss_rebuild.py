import numpy as np
import faiss
import pickle
import os

from app.models.user import User
from app import db


INDEX_PATH = "faiss_index.bin"
MAP_PATH = "id_map.pkl"


def rebuild_faiss():

    print("🔥 AUTO REBUILDING FAISS...")

    students = User.query.filter(
        User.role == "student",
        User.embedding != None
    ).all()

    if len(students) == 0:
        print("⚠ No embeddings found. Skipping rebuild.")
        return

    embeddings = []
    id_map = []

    for student in students:

        embeddings.append(np.array(student.embedding).astype("float32"))
        id_map.append(student.id)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save files
    faiss.write_index(index, INDEX_PATH)

    with open(MAP_PATH, "wb") as f:
        pickle.dump(id_map, f)

    print(f"✅ FAISS rebuilt with {len(id_map)} students.")
