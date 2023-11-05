// // results.js
// document.addEventListener("DOMContentLoaded", function() {
//     // Your JavaScript code here
//     function changePage(page) {
//         window.location.href = `${page}`;
//     }
    
//     if (mode == "1") { 
//         const storedImage = localStorage.getItem('uploadedImageData');
//         if (storedImage) {
//             // Find the image element with the class 'uploadedImage' and set its src attribute
//             const uploadedImage = document.querySelector('.uploadedImage');
//             if (uploadedImage) {
//                 uploadedImage.src = storedImage;
//             }
//         }
//     }
//     else if (mode == "2") {
//         document.addEventListener("DOMContentLoaded", function() {
//             // Your JavaScript code here
//             const textData = decodeURIComponent("{{ labels.name }}");
//             // Fetch image from Unsplash API
//             console.log(textData);
//             fetch(`https://api.unsplash.com/search/photos?query="${textData}"&client_id=BxwX4irH_sxS33ZGXT9ZFCuYP4O0BCbK_KMCyKGVdUo`)
//                 .then(response => response.json())
//                 .then(data => {
//                     const uploadedImage = document.querySelector('.uploadedImage');
//                     if (uploadedImage && data.results.length > 0) {
//                         // Generate a random index
//                         const randomIndex = Math.floor(Math.random() * data.results.length);
//                         uploadedImage.src = data.results[randomIndex].urls.small;
//                     }
//                 })
//                 .catch(error => console.error('Error:', error));
//         });
//     }
// });