from flask import Flask, request, render_template, jsonify
import base64
import cv2
import numpy as np
import os
import uuid
from werkzeug.utils import secure_filename
from utils import detect_eye_state, detect_eye_state_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def index():
    output_img_path = None

    if request.method == 'POST':
        file = request.files.get('image')
        if not file:
            return render_template('index.html', result="Vui lòng chọn ảnh.")

        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)

        img = cv2.imread(filepath)
        if img is None:
            return render_template('index.html', result="Không thể đọc ảnh.", input_image=unique_name)
        
        result_img = detect_eye_state(img)
        if result_img is None:
            return render_template('index.html', result="Không tìm thấy khuôn mặt nào.", input_image=unique_name)

        # Save the processed image
        output_name = f"processed_{unique_name}"
        output_img_path = os.path.join(app.config['UPLOAD_FOLDER'], output_name)
        cv2.imwrite(output_img_path, result_img)

        return render_template('index.html', result='Xử lý xong', input_image=unique_name, output_image=output_name)
    return render_template('index.html')

@app.route('/realtime-detect', methods=['POST'])
def realtime_detect():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image'}), 400

    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400

    result_img = detect_eye_state(img)  # ảnh đã có landmark và label
    _, buffer = cv2.imencode('.jpg', result_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        'image': f'data:image/jpeg;base64,{img_base64}'
    })

@app.route('/video', methods=['POST'])
def video():
    file = request.files.get('video')
    if not file:
        return render_template('index.html', result="Vui lòng chọn video.")

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4()}_{filename}"
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(input_path)

    # Xác định tên và path cho video output
    output_name = f"processed_{unique_name}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_name)

    # Gọi hàm xử lý video
    detect_eye_state_video(input_path, output_path)

    return render_template('index.html', result="Xử lý video xong.", input_video=unique_name, output_video=output_name)

if __name__ == '__main__':
    app.run(debug=True)
