var addCampaignLink = document.getElementById("addCampaignLink");
var addCampaignFormDiv = document.getElementById("addCampaignFormDiv");
var formBlurHandler = null;

function loadAddCampaignForm() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/addCampaignForm");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var tempDiv = document.createElement('div');
                tempDiv.innerHTML = xhr.responseText;

                var campaignForm = tempDiv.querySelector('form');

                addCampaignFormDiv.innerHTML = '';
                addCampaignFormDiv.appendChild(campaignForm);
                
                addCampaignFormDiv.style.display = "block";
                blurContent();

                if (formBlurHandler) {
                    document.body.removeEventListener("click", formBlurHandler);
                }

                formBlurHandler = function(event) {
                    if (!addCampaignFormDiv.contains(event.target)) {
                        addCampaignFormDiv.style.display = "none";
                        removeBlur();
                        document.body.removeEventListener("click", formBlurHandler);
                    }
                };
                document.body.addEventListener("click", formBlurHandler);

                campaignForm.addEventListener("submit", function(event) {
                    event.preventDefault();
                    var formData = new FormData(campaignForm);
                
                    var submitXhr = new XMLHttpRequest();
                    submitXhr.open("POST", campaignForm.action);
                    submitXhr.onreadystatechange = function() {
                        if (submitXhr.readyState === 4) {
                            if (submitXhr.status === 200) {
                                window.location.href = submitXhr.responseURL;
                            }
                        }
                    };
                
                    submitXhr.send(formData);
                });
            } else {
                console.error("Error fetching addCampaignForm:", xhr.status);
            }
        }
    };
    xhr.send();
}

addCampaignLink.addEventListener("click", function(event) {
    event.preventDefault();
    loadAddCampaignForm();
});

function blurContent() {
    $('#blur-container').show();
}

function removeBlur() {
    $('#blur-container').hide();
}
