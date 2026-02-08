import os
import faiss
import numpy as np
import pickle

INDEX_PATH = "faiss_index.bin"
MAP_PATH = "faiss_map.pkl"
DIMENSION = 128


def load_index():

    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)

    index = faiss.IndexFlatL2(DIMENSION)
    faiss.write_index(index, INDEX_PATH)

    return index


def load_map():

    if os.path.exists(MAP_PATH):
        with open(MAP_PATH, "rb") as f:
            return pickle.load(f)

    return []


def save_map(mapping):

    with open(MAP_PATH, "wb") as f:
        pickle.dump(mapping, f)


def add_embedding(embedding, user_id):

    index = load_index()
    mapping = load_map()

    vector = np.array(embedding).astype("float32")
    vector = vector / np.linalg.norm(vector)
    index.add(vector.reshape(1, -1))

    mapping.append(user_id)

    faiss.write_index(index, INDEX_PATH)
    save_map(mapping)


def search_embedding(embedding, k=1):

    index = load_index()
    mapping = load_map()

    # ⭐ NORMALIZE QUERY VECTOR (CRITICAL)
    vector = np.array(embedding).astype("float32")
    vector = vector / np.linalg.norm(vector)

    vector = vector.reshape(1, -1)

    distances, indices = index.search(vector, k)

    idx = indices[0][0]
    distance = distances[0][0]

    print("FAISS DISTANCE:", distance)
    print("FAISS INDEX:", idx)

    if idx < len(mapping):
        return mapping[idx], distance
    else:
        return None, None
