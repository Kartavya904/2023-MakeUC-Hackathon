// const fileUpload = document.getElementById('file-upload');
// const textInput = document.getElementById('text-input');
// const submitButton = document.getElementById('submit-button');
// const fileNameDisplay = document.getElementById('file-name');
// const uploadedImage = document.getElementById('uploaded-image');

// function submitForm() {
//     // Check if either an image is uploaded or text is provided
//     if (fileUpload.files.length > 0) {
//         const file = fileUpload.files[0];
//         const reader = new FileReader();
//         reader.onload = function() {
//             const fileData = reader.result;
//             localStorage.setItem('uploadedImageData', fileData);
//             // Show the uploaded image
//             uploadedImage.src = fileData;
//             uploadedImage.style.display = 'block';
//             // Redirect to a new page and pass the image data as a parameter
//             console.log(fileData);
//             //window.location.href = `result.html?imageData=${encodeURIComponent(fileData)}`;
//         };
//         reader.readAsDataURL(file);
//     } else if (textInput.value.trim() !== '') {
//         // Redirect to a new page and pass the text as a parameter
//         const textData = encodeURIComponent(textInput.value.trim());
//         window.location.href = `result.html?textData=${textData}`;
//     } else {
//         alert('Please upload an image or enter text.');
//     }
// }

// // Enable the submit button when either input changes
// fileUpload.addEventListener('change', updateSubmitButton);
// textInput.addEventListener('input', updateSubmitButton);

// function updateSubmitButton() {
//     if (fileUpload.files.length > 0 || (textInput.value.trim() !== '' && textInput.value.length > 2)) {
//         submitButton.style.display = 'block';
//         if (fileUpload.files.length > 0) {
//             submitButton.value = "Process Image"
//             const fileName = fileUpload.files[0].name;
//             fileNameDisplay.innerHTML = `<span class="cancel-button" onclick="cancelFileUpload()">X</span> File Name: ${fileName}`;
//         } else {
//             submitButton.value = "Process Text"
//             fileNameDisplay.textContent = '';
//         }
//     } else {
//         submitButton.style.display = 'none';
//         fileNameDisplay.textContent = '';
//     }
// }

// // Function to cancel file upload and clear the file input
// function cancelFileUpload() {
//     fileUpload.value = ''; // Clear the file input
//     fileNameDisplay.textContent = ''; // Clear the file name display
//     submitButton.style.display = 'none'; // Hide the submit button
//     uploadedImage.style.display = 'none'; // Hide the uploaded image
// }