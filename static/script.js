async function captureScreen() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
        const video = document.createElement("video");
        video.srcObject = stream;
        video.play();

        video.onloadedmetadata = async () => {
            const canvas = document.getElementById("canvas");
            const ctx = canvas.getContext("2d");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Stop screen capture
            stream.getTracks().forEach(track => track.stop());

            // Convert canvas to Base64
            const imageData = canvas.toDataURL();

            // Send to backend for OCR
            fetch("/process_image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ image: imageData })
            })
            .then(response => response.json())
            .then(data => alert("Text Extracted: " + JSON.stringify(data)))
            .catch(error => console.error("Error:", error));
        };
    } catch (error) {
        alert("Screen capture failed: " + error);
    }
}
