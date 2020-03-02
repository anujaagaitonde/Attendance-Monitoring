// Read file input (just for testing - remove later)

const input = document.querySelector('input');
const preview = document.querySelector('.preview');

input.addEventListener('change', updateImageDisplay);

// Declare valid file types
const fileTypes = [
    'image/jpeg',
    'image/pjepg',
    'image/png'
];

// Return whether input file is a valid file type
function validFileType(file) {
    return fileTypes.includes(file.type);
}

// Return formatted file size (in Bytes, kB, MB)
function returnFileSize(number) {
    if (number < 1024) {
        return number + 'bytes';
    }
    else if (number >= 1024 && number < 1048576) {
        return (number / 1024).toFixed(1) + 'KB';
    }
    else if (number >= 1048576) {
        return (number / 1048576).toFixed(1) + 'MB';
    }
}

// Display uploaded image along with file name and size, or display error warning
function updateImageDisplay() {
    // Empty previous contents of the preview <div>
    while (preview.firstChild) {
        preview.removeChild(preview.firstChild);
    }

    // Grab the FileList object that contains the information on all the selected files, store in variable called curFiles
    const curFiles = input.files;

    // check to see if no files were selected, and if so print a message into the preview <div> stating that no files were selected
    if (curFiles.length === 0) {
        const para = document.createElement('p');
        para.textContent = 'No images currently selected for upload';
        preview.appendChild(para);
    }
    // If files have been selected, print information about each one in the preview <div>
    else {
        const list = document.createElement('ol');
        preview.appendChild(list);

        for (const file of curFiles) {
            const listItem = document.createElement('li');
            const para = document.createElement('p');

            // check whether files uploaded are of the correct type
            if (validFileType(file)) {
                para.textContent = `File name ${file.name}, file size ${returnFileSize(file.size)}.`;
                const image = document.createElement('img');
                // Create a thumbnail preview of the image
                image.src = URL.createObjectURL(file);

                // Decode QR code
                var imageURI = image.src;

                // Decode captured image from local URL
                decodeImageFromBase64(imageURI, function (decodedInformation) {
                    console.log(decodedInformation);
                    if (decodedInformation == "error decoding QR Code" || decodedInformation == "Failed to load the image") {
                        alert(decodedInformation);
                    }
                    else {
                        window.location.href = decodedInformation; // redirect to QR code URL
                    }
                });
                listItem.appendChild(para);
                listItem.appendChild(image);
            }
            else {
                para.textContent = `File name ${file.name}: Not a valid file type. Update your selection.`;
                listItem.appendChild(para);
            }
            list.appendChild(listItem);
        }
    }
}