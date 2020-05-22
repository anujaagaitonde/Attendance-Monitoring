// Set constraints for the video stream
var constraints = { video: { facingMode: "environment" }, audio: false };

const cameraView = document.querySelector("#camera--view"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#camera--trigger")

// Access camera and stream to camera--view
function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function (stream) {
            track = stream.getTracks()[0];
            cameraView.srcObject = stream;
        })
        .catch(function (error) {
            console.error("Oops. Something is broken.", error);
        });
}

/**
 * The function decodeImageFromBase64 expects as first parameter a base64 string from a QRCode.
 * As second parameter the callback that expects the data from the QRCode as first parameter.
 */
function decodeImageFromBase64(data, callback) {
    // set callback
    qrcode.callback = callback;
    // Start decoding
    qrcode.decode(data)
}

// Program camera trigger button to grab a frame from the stream to use as image output
cameraTrigger.onclick = function () {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/webp"); // save captured image URL
    cameraOutput.classList.add("taken");
    var imageURI = cameraOutput.src;
    decodeImageFromBase64(imageURI, function (decodedInformation) { // decode captured image from local URL
        console.log(decodedInformation);
        if (decodedInformation == "error decoding QR Code" || decodedInformation == "Failed to load the image") {
            alert(decodedInformation);
        }
        else {
            var decoded_info = decodedInformation;
            // obtain decoded information in variable and send to form value
            document.getElementById("id_auth_hash").value = decoded_info;
            // Automatically submit form once data is populated
            document.getElementById("auth_form").submit();
        }
    });
    // console.log(decodedInformation);
};

// const fileInput = document.getElementById('file-input');

// fileInput.addEventListener('change', (e) => doSomethingWithFiles(e.target.files));


// Start camera once window finished loading
window.addEventListener("load", cameraStart, false);
