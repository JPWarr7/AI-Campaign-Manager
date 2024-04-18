// import config from './config.js';
document.getElementById("exportButton").addEventListener("click", function() {
    var img_url = document.querySelector('img').src;
    var imgurClientID = '5331f6b5050b43c';
    var url_segments = img_url.split('/');
    var image_hash = null;
    for (var i = 0; i < url_segments.length; i++) {
        var segment = url_segments[i];
        if (segment.includes('.j')) {
            image_hash = segment.split('.')[0];
            break;
        }
    }
    fetch(`https://api.imgur.com/3/image/${image_hash}`, {
        headers: {
            Authorization: `Client-ID ${imgurClientID}`
        }
    })
    .then(response => response.json())
    .then(data => {
        var imageUrl = data.data.link;
        var urlSegments = imageUrl.split('i.');
        var segment = urlSegments[1];
        var imageHash = segment.split('.j')[0];
        console.log(imageHash);

        var downloadLink = document.createElement("a");
        downloadLink.href = 'https://' + imageHash;
        downloadLink.target = "_blank";
        downloadLink.click();

    })
    .catch(error => {
        console.error('Error fetching image from Imgur:', error);
    });
});
