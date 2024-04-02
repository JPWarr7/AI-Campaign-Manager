document.getElementById("exportButton").addEventListener("click", function() {
    var img_url = document.querySelector('img').src;
    var encoded_img_url = encodeURIComponent(img_url);
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/exportImage?img_url=" + encoded_img_url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log("Export successful");
            } else {
                console.error("Export failed");
            }
        }
    };
    
    xhr.send();
});
