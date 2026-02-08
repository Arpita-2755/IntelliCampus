import cv2
import numpy as np
from deepface import DeepFace

from ai_engine.faiss_manager import search_embedding


def process_class_image(image_path, threshold=1.0):

    """
    Returns:
        present_student_ids -> set()
    """

    present_students = set()

    # Load image
    img = cv2.imread(image_path)

    if img is None:
        print("Image not loaded.")
        return present_students

    # Detect faces + embeddings
    try:

        representations = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            detector_backend="retinaface",
            enforce_detection=True
        )

    except Exception as e:
        print("Face detection error:", e)
        return present_students


    for face in representations:

        embedding = np.array(face["embedding"]).astype("float32")
        # ⭐ NORMALIZE (VERY IMPORTANT)
        embedding = embedding / np.linalg.norm(embedding)
        # FAISS search
        student_id, distance = search_embedding(embedding)

        if student_id is not None and distance < threshold:

            print(f"MATCH FOUND → ID: {student_id} | Distance: {distance}")

            present_students.add(student_id)

        else:

            print("Unknown face detected.")


    return present_students
