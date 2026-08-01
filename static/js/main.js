const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const outputText = document.getElementById('output-text');
const videoFeed = document.getElementById('video-feed');
const cameraBox = document.getElementById('camera-box');
const fullscreenBtn = document.getElementById('fullscreen-btn');
const fullscreenIcon = document.getElementById('fullscreen-icon');

let videoStream = null;

startBtn.addEventListener('click', async () => {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: { ideal: 1280 }, height: { ideal: 720 } } 
        });
        videoFeed.srcObject = videoStream;

        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusDot.classList.add('active');
        statusText.innerText = 'Listening...';
        outputText.innerText = 'Awaiting gestures...';

    } catch (err) {
        alert("Kameraga ulanishda xatolik yuz berdi: " + err.message);
        console.error("Camera access error:", err);
    }
});

stopBtn.addEventListener('click', () => {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        videoFeed.srcObject = null;
    }

    startBtn.disabled = false;
    stopBtn.disabled = true;
    statusDot.classList.remove('active');
    statusText.innerText = 'System Standby';
    outputText.innerText = 'Translation stopped';
});

fullscreenBtn.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        cameraBox.requestFullscreen().catch(err => {
            alert(`Error entering fullscreen: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
});

document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement) {
        cameraBox.classList.add('is-fullscreen');
        fullscreenIcon.className = 'bi bi-fullscreen-exit';
    } else {
        cameraBox.classList.remove('is-fullscreen');
        fullscreenIcon.className = 'bi bi-fullscreen';
    }
});