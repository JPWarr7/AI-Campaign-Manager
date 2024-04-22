var addCampaignLink = document.getElementById("addCampaignLink");
var addCampaignFormDiv = document.getElementById("addCampaignFormDiv");
var formBlurHandler = null;

function loadAddCampaignForm() {
    var async = new XMLHttpRequest();
    async.open("GET", "/addCampaignForm");
    async.onreadystatechange = function() {
        if (async.readyState === 4) {
            if (async.status === 200) {
                var tempDiv = document.createElement('div');
                tempDiv.innerHTML = async.responseText;

                var campaignForm = tempDiv.querySelector('form');

                addCampaignFormDiv.innerHTML = '';
                addCampaignFormDiv.appendChild(campaignForm);

                applyCampaignFormStyles();
                applyTooltips();
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
                    showEllipsis();
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
                console.error("Error fetching addCampaignForm:", async.status);
            }
        }
    };
    async.send();
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

function showEllipsis() {
    document.getElementById('ellipsis').style.display = 'flex';
  }

function removeEllipsis() {
    $('#ellipsis').hide();
}

function applyCampaignFormStyles() {
    var form = document.getElementById('addCampaignForm');
    if (form) {
        form.style.width = '100%';

        var card = form.parentElement;
        if (card) {
            card.style.backgroundColor = 'rgba(0, 0, 0, 0.4)'; 
            card.style.backdropFilter = 'blur(7px)';
            card.style.width = '40%';
        }

        var cardHeader = form.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.style.paddingBottom = '3%';

        }

        var cardBody = form.querySelector('.card-body');
        if (cardBody) {

        }

        var formControls = form.querySelectorAll('.form-control');
        formControls.forEach(function(control) {
            control.style.width = '100%'; 
            control.style.padding = '3%';
            control.style.marginBottom = '4%';
        });

        var selectElement = form.querySelector('.form-select');
        if (selectElement) {
            selectElement.style.width = '30%'; 
            selectElement.style.padding = '8px';
            selectElement.style.marginBottom = '4%';
        }

        var submitButton = form.querySelector('.btn-secondary');
        if (submitButton) {
            submitButton.style.width = '40%';

        }
    }
}

function applyTooltips() {
    $('[data-toggle="tooltip"]').tooltip({
        html:true,
    });

    $('[data-toggle="tooltip"]').on('click', function () {
        // Trigger the tooltip manually
        $(this).tooltip('show');
      });
}
