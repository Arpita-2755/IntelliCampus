from deepface import DeepFace
import cv2


def verify_face(known_image_path):

    '''video = cv2.VideoCapture(0)'''

    print("Starting camera...")

    while True:

        '''ret, frame = video.read()'''

        '''cv2.imshow("AI Attendance - Press Q to Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):

            temp_img = "temp_capture.jpg"
            cv2.imwrite(temp_img, frame)

            break

    video.release()
    cv2.destroyAllWindows()'''

    try:

        result = DeepFace.verify(
            img1_path=known_image_path,
            img2_path=temp_img,
            enforce_detection=False
        )

        return result["verified"]

    except Exception as e:
        print("Verification error:", e)
        return False
