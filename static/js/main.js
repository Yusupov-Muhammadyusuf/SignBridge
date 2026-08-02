document.addEventListener('DOMContentLoaded', () => {
    const videoFeed = document.getElementById('video-feed');
    const canvasOverlay = document.getElementById('canvas-overlay');
    const outputText = document.getElementById('output-text');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const videoUpload = document.getElementById('video-upload');
    const cameraBox = document.getElementById('camera-box');

    let stream = null;
    let isProcessing = false;
    let sendInterval = null;

    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 1280, height: 720, facingMode: 'user' } 
            });
            videoFeed.srcObject = stream;
            
            statusDot.classList.add('active');
            statusText.textContent = 'System Active';
            
            startBtn.disabled = true;
            stopBtn.disabled = false;
            
            isProcessing = true;
            startFrameSending();
        } catch (err) {
            console.error("Camera Access Error:", err);
            statusText.textContent = 'Camera Access Denied';
            alert("Kameraga ruxsat berilmadi yoki kamera topilmadi.");
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            videoFeed.srcObject = null;
        }
        
        isProcessing = false;
        clearInterval(sendInterval);
        
        statusDot.classList.remove('active');
        statusText.textContent = 'System Standby';
        outputText.textContent = 'Ready to translate...';
        
        startBtn.disabled = false;
        stopBtn.disabled = true;
        
        const ctx = canvasOverlay.getContext('2d');
        ctx.clearRect(0, 0, canvasOverlay.width, canvasOverlay.height);
    }

    function startFrameSending() {
        const tempCanvas = document.createElement('canvas');
        const tempCtx = tempCanvas.getContext('2d');

        sendInterval = setInterval(async () => {
            if (!isProcessing || !videoFeed.videoWidth) return;

            tempCanvas.width = videoFeed.videoWidth;
            tempCanvas.height = videoFeed.videoHeight;
            tempCtx.drawImage(videoFeed, 0, 0, tempCanvas.width, tempCanvas.height);

            const base64Image = tempCanvas.toDataURL('image/jpeg', 0.6);

            try {
                const response = await fetch('/process_frame', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: base64Image })
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    if (data.text) {
                        outputText.textContent = data.text;
                    }

                    if (data.image) {
                        const img = new Image();
                        img.onload = () => {
                            canvasOverlay.width = tempCanvas.width;
                            canvasOverlay.height = tempCanvas.height;
                            const ctx = canvasOverlay.getContext('2d');
                            ctx.clearRect(0, 0, canvasOverlay.width, canvasOverlay.height);
                            ctx.drawImage(img, 0, 0);
                        };
                        img.src = data.image;
                    }
                }
            } catch (err) {
                console.error("Frame processing error:", err);
            }
        }, 300);
    }

    videoUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            stopCamera();
            const fileURL = URL.createObjectURL(file);
            videoFeed.srcObject = null;
            videoFeed.src = fileURL;
            videoFeed.play();
            
            statusDot.classList.add('active');
            statusText.textContent = 'Processing Video File';
            startBtn.disabled = true;
            stopBtn.disabled = false;
            
            isProcessing = true;
            startFrameSending();
        }
    });

    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            cameraBox.requestFullscreen().catch(err => console.log(err));
            cameraBox.classList.add('is-fullscreen');
        } else {
            document.exitFullscreen();
            cameraBox.classList.remove('is-fullscreen');
        }
    });

    startBtn.addEventListener('click', startCamera);
    stopBtn.addEventListener('click', stopCamera);
});