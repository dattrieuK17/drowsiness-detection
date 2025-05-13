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

# Hàm lấy tọa độ mắt
def get_eye_landmarks(landmarks, w, h, indices):
    return np.array([[landmarks[i].x * w, landmarks[i].y * h] for i in indices])

# Hàm xử lý ảnh
def detect_eye_state(image):
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        print("No face detected.")
        return None

    landmarks = results.multi_face_landmarks[0].landmark

    left_eye = get_eye_landmarks(landmarks, w, h, LEFT_EYE_IDX)
    right_eye = get_eye_landmarks(landmarks, w, h, RIGHT_EYE_IDX)

    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)
    avg_ear = round((left_ear + right_ear) / 2.0, 3)

    eye_state = classify_eye_state(avg_ear)

    # Hiển thị kết quả
    cv2.putText(image, f"Eye: {eye_state} ({avg_ear:.2f})", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0) if eye_state == "Open" else (0, 0, 255), 2)

    # Vẽ các điểm landmark quanh mắt
    for pt in np.vstack((left_eye, right_eye)).astype(np.int32):
        cv2.circle(image, tuple(pt), 2, (255, 0, 0), -1)

    # cv2.imshow("Eye State Detection", image) 

    return image

def detect_eye_state_video(video_path=0):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detect_eye_state(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
# if __name__ == "__main__":
#     # open: "C:\Users\datta\Downloads\anhthe_900x1200.jpeg"
#     # close: "C:\Users\datta\Downloads\R (1).jpeg"
#     image_path = r"D:\drowsiness-detection\static\uploads\d7ca10d1-e5fb-468d-9f7c-86c4eda0fc8d_capture.jpg"  # Đường dẫn ảnh đầu vào
#     img = cv2.imread(image_path)
#     detect_eye_state(img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     # detect_eye_state_video(0)



