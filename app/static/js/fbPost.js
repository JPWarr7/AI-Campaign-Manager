import config from './config.js';

function shareToFacebook(imageUrl) {
    var campaignText = document.querySelector('.ad-text').textContent.trim();
    console.log('Campaign text:', campaignText);


    FB.init({
        appId: config.facebookAppID,
        version: config.facebookAPIVersion 
    });

    FB.ui({
        method: 'share',
        href: imageUrl,
        quote: campaignText,
    }, function(response) {
        if (response && !response.error_message) {
            console.log('Post shared successfully:', response);
        } else {
            console.error('Error sharing post:', response.error_message);
        }
    });
}

document.getElementById("shareButton").addEventListener("click", function() {
    var imageUrl = document.getElementById("campaignImage").src;

    shareToFacebook(imageUrl);
});

function copyToClipboard(text) {

    var tempInput = document.createElement("input");
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    var popup = document.createElement("div");
    popup.textContent = "Text copied to clipboard!";
    popup.style.position = "fixed";
    popup.style.bottom = "20px";
    popup.style.left = "50%";
    popup.style.transform = "translateX(-50%)";
    popup.style.padding = "10px 20px";
    popup.style.background = "#333";
    popup.style.color = "#fff";
    popup.style.borderRadius = "5px";
    popup.style.zIndex = "9999";
    popup.style.opacity = "0";
    popup.style.transition = "opacity 0.3s ease-in-out";
    document.body.appendChild(popup);

    setTimeout(function() {
        popup.style.opacity = "1";
    }, 100);

    setTimeout(function() {
        popup.style.opacity = "0";
        setTimeout(function() {
            document.body.removeChild(popup);
        }, 300);
    }, 2000);
}


document.getElementById("copyButton").addEventListener("click", function() {
    var campaignText = document.querySelector('.ad-text').textContent.trim();
    console.log('Campaign text:', campaignText);
    
    copyToClipboard(campaignText);
});

