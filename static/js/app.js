const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const imageInput = document.getElementById('image');
const toggle = document.getElementById('toggle');

let stream = null;
let isCameraOn = false;

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(s => {
            stream = s;
            video.srcObject = stream;
            isCameraOn = true;
            toggle.textContent = "Tắt Camera";
            toggle.classList.remove("btn-success");
            toggle.classList.add("btn-danger");
        })
        .catch(err => {
            console.error("Không thể truy cập camera", err);
            alert("Không thể truy cập camera!");
        });
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    video.srcObject = null;
    isCameraOn = false;
    toggle.textContent = "Bật Camera";
    toggle.classList.remove("btn-danger");
    toggle.classList.add("btn-success");
}

// Toggle camera on/off
toggle.addEventListener('click', () => {
    if (isCameraOn) {
        stopCamera();
    } else {
        startCamera();
    }
});

// Capture image and attach to form input
snap.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        imageInput.files = dataTransfer.files;
    }, "image/jpeg");
});

// Start camera on page load
startCamera();

const realtimeBtn = document.getElementById('realtime');
const canvasResult = document.getElementById('canvas-result');
let realtimeInterval = null;

realtimeBtn.addEventListener('click', () => {
    if (realtimeInterval) {
        clearInterval(realtimeInterval);
        realtimeInterval = null;
        realtimeBtn.textContent = "Bắt đầu Real-time";
    } else {
        realtimeInterval = setInterval(() => {
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob(blob => {
                const formData = new FormData();
                formData.append("image", blob, "frame.jpg");

                fetch("/realtime-detect", {
                    method: "POST",
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    if (data.image) {
                        const img = new Image();
                        img.onload = () => {
                            const resultCtx = canvasResult.getContext('2d');
                            resultCtx.clearRect(0, 0, canvasResult.width, canvasResult.height);
                            resultCtx.drawImage(img, 0, 0, canvasResult.width, canvasResult.height);
                        };
                        img.src = data.image;
                    }
                })
                .catch(err => console.error("Lỗi khi gửi ảnh real-time:", err));
            }, "image/jpeg");
        }, 500);

        realtimeBtn.textContent = "Dừng Real-time";
    }
});
