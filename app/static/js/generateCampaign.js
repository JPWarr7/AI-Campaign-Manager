const responseAreaSummary = document.getElementById('summary');
const responseAreaAdText = document.getElementById('ad_text');
const responseAreaImageContainer = document.getElementById('image_container');

const summaryDiv = document.getElementById('regenerateSummarization');
const adTextDiv = document.getElementById('regenerateAdvertisement');
const imageDiv = document.getElementById('regenerateImage');

var urlParams = new URLSearchParams(window.location.search);
var campaignId = urlParams.get('new_campaign_id');
var callType = urlParams.get('call_type');

let final_summary;
let final_ad_text;
let final_img_prompt;
let final_image_url;
let final_parent_id;

const evtSource = new EventSource(`/createCampaign/${campaignId}/${callType}`);

evtSource.onmessage = function(event) {
    if (event.data === 'end-of-stream') {
        evtSource.close();
        $('#regenerateSummarization').show();
        $('#regenerateAdvertisement').show();
        $('#regenerateImage').show();
        $('#saveCampaign').show();

    }
};

evtSource.addEventListener('summary', function(event) {
    setTimeout(function() {
        responseAreaSummary.innerHTML += event.data;
    }, 100);
});

evtSource.addEventListener('ad_text', function(event) {
    setTimeout(function() {
        responseAreaAdText.innerHTML += event.data;
    }, 100);
});

evtSource.addEventListener('img_url', function(event) {
    const imageUrl = event.data;
    const imgElement = document.createElement('img');
    imgElement.id = 'generated_image';
    imgElement.src = imageUrl;
    imgElement.style.width = '100%';
    responseAreaImageContainer.appendChild(imgElement);
});

evtSource.addEventListener('campaign_id', function(event) {
    campaignId = event.data;
});

evtSource.addEventListener('final_summary', function(event) {
    final_summary = event.data;
});

evtSource.addEventListener('final_ad_text', function(event) {
    final_ad_text = event.data;
});

evtSource.addEventListener('final_img_prompt', function(event) {
    final_img_prompt = event.data;
});

evtSource.addEventListener('final_img_url', function(event) {
    final_img_url = event.data;
});

evtSource.addEventListener('final_parent_id', function(event) {
    final_parent_id = event.data;
});

function regenerateImage() {
    const imgElement = document.getElementById('generated_image');
    const img_url = imgElement.src;
    const img_feedback = document.getElementById('regenerateImageInput')
    const regenerateParameters = {
        img_url: img_url,
        feedback: img_feedback.value
    };

    $('#regenerateImage').hide();
    $('#saveCampaign').hide();
    img_feedback.value = '';

    const progressBar = document.createElement('div');
    progressBar.classList.add('progress-container');
    const progressInner = document.createElement('div');
    progressInner.classList.add('progress-bar');
    progressBar.appendChild(progressInner);
    responseAreaImageContainer.appendChild(progressBar); 

    fetch('/regenerateImage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(regenerateParameters)
    })

    .then(response => response.json())
    .then(data => {
        const imageUrl = data.new_image_url;
        const imgElement = document.getElementById('generated_image');
        imgElement.src = imageUrl;
        console.log('POST request successful', data);

    })
    .catch(error => {
        console.error('Error regenerating image:', error);
    })
    .finally(() => {
        responseAreaImageContainer.removeChild(progressBar);
        $('#regenerateImage').show();
        $('#saveCampaign').show();
    });
}

function regenerateSummarization() {
    const summarization = encodeURIComponent(responseAreaSummary.textContent);
    const feedback = encodeURIComponent(document.getElementById('regenerateSummarizationInput').value);
    const evtSource = new EventSource(`/regenerateSummarization?summarization=${summarization}&feedback=${feedback}`);
    
    $('#regenerateSummarization').hide();
    $('#saveCampaign').hide();
    responseAreaSummary.innerHTML = '';

    evtSource.onmessage = function(event) {
        if (event.data === 'end-of-stream') {
            evtSource.close();
            $('#regenerateSummarization').show();
            $('#saveCampaign').show();
        }
    };

    evtSource.addEventListener('summary', function(event) {
        setTimeout(function() {
            responseAreaSummary.innerHTML += event.data;
        }, 100);
    });
}

function regenerateAdvertisement() {
    const ad_text = encodeURIComponent(responseAreaAdText.textContent);
    const username = document.getElementById('username');
    const feedback = encodeURIComponent(document.getElementById('regenerateAdvertisementInput').value);
    const evtSource = new EventSource(`/regenerateAdvertisement?ad_text=${ad_text}&feedback=${feedback}`);
    
    $('#regenerateAdvertisement').hide();
    $('#saveCampaign').hide();
    responseAreaAdText.innerHTML = '';

    evtSource.onmessage = function(event) {
        if (event.data === 'end-of-stream') {
            evtSource.close();
            $('#regenerateAdvertisement').show();
            $('#saveCampaign').show();
        }
    };

    evtSource.addEventListener('ad_text', function(event) {
        setTimeout(function() {
            responseAreaAdText.innerHTML += event.data;
        }, 50);
    });
}

function saveCampaign() {
    const imgElement = document.getElementById('generated_image')
    const finalizedParameters = {
        new_campaign_id: campaignId,
        call_type: callType,
        summary: responseAreaSummary.textContent,
        ad_text: responseAreaAdText.textContent,
        img_prompt: final_img_prompt,
        image_url: imgElement.src,
        parent_id: final_parent_id
    };

    fetch('/processCampaign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(finalizedParameters)
    })
    .then(response => response.json())
    .then(data => {
        console.log('POST request successful', data);
        window.location.href = `/viewCampaign/${campaignId}`;
    })
    .catch(error => {
        console.error('Error making POST request', error);
    });
}
