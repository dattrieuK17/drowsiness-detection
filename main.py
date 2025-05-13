import cv2
import mediapipe as mp
import numpy as np

# Khởi tạo FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Chỉ số landmark cho mắt trái và mắt phải trong MediaPipe
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

# Hàm tính EAR (Eye Aspect Ratio)
def calculate_ear(eye_points):
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Hàm phân loại mắt mở/nhắm
def classify_eye_state(ear, threshold=0.25):
    return "Close" if ear < threshold else "Open"

# Hàm xử lý ảnh
def detect_eye_state(image_path):
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        print("No face detected.")
        return None

    landmarks = results.multi_face_landmarks[0].landmark

    def get_eye_landmarks(indices):
        return np.array([[landmarks[i].x * w, landmarks[i].y * h] for i in indices])

    left_eye = get_eye_landmarks(LEFT_EYE_IDX)
    right_eye = get_eye_landmarks(RIGHT_EYE_IDX)

    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)
    avg_ear = (left_ear + right_ear) / 2.0

    state = classify_eye_state(avg_ear)
    print(f"EAR: {avg_ear:.3f} → Eye State: {state}")
    return state

# Ví dụ chạy:
if __name__ == "__main__":
    image_path = r"C:\Users\datta\Downloads\R (1).jpeg"  # Đường dẫn ảnh đầu vào
    detect_eye_state(image_path)
