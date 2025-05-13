from flask import Flask, request, render_template
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

@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
