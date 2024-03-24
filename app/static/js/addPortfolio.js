var addPortfolioLink = document.getElementById("addPortfolioLink");
var addPortfolioFormDiv = document.getElementById("addPortfolioFormDiv");
var formBlurHandler = null;

function loadAddPortfolioForm() {
    var async = new XMLHttpRequest();
    async.open("GET", "/addPortfolioForm");
    async.onreadystatechange = function() {
        if (async.readyState === 4) {
            if (async.status === 200) {
                var tempDiv = document.createElement('div');
                tempDiv.innerHTML = async.responseText;

                var portfolioForm = tempDiv.querySelector('form');

                addPortfolioFormDiv.innerHTML = '';
                addPortfolioFormDiv.appendChild(portfolioForm);

                applyPortfolioFormStyles();
                
                addPortfolioFormDiv.style.display = "block";
                blurContent();

                if (formBlurHandler) {
                    document.body.removeEventListener("click", formBlurHandler);
                }

                formBlurHandler = function(event) {
                    if (!addPortfolioFormDiv.contains(event.target)) {
                        addPortfolioFormDiv.style.display = "none";
                        removeBlur();
                        document.body.removeEventListener("click", formBlurHandler);
                        formBlurHandler = null;
                    }
                };
                document.body.addEventListener("click", formBlurHandler);
                
                portfolioForm.addEventListener("submit", function(event) {
                    event.preventDefault();
                    var formData = new FormData(portfolioForm);
                
                    portfolioForm.action = "/addPortfolio";
                    
                    var submitXhr = new XMLHttpRequest();
                    submitXhr.open("POST", portfolioForm.action);
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
                console.error("Error fetching addPortfolioForm:", async.status);
            }
        }
    };
    async.send();
}

addPortfolioLink.addEventListener("click", function(event) {
    event.preventDefault();
    loadAddPortfolioForm();
});

function blurContent() {
    $('#blur-container').show();
}

function removeBlur() {
    $('#blur-container').hide();
}

function applyPortfolioFormStyles() {
    var form = document.getElementById('addPortfolioForm');
    if (form) {

        form.style.width = '100%';

        var card = form.parentElement;
        if (card) {
            console.log('card exists')
            card.style.backgroundColor = 'rgba(0, 0, 0, 0.4)';
            card.style.backdropFilter = 'blur(7px)';
            card.style.width = '40%'
        }

        // Adjust card header padding
        var cardHeader = form.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.style.paddingBottom = '3%';
        }

        // Adjust form control styles
        var formControls = form.querySelectorAll('.form-control');
        formControls.forEach(function(control) {
            control.style.width = '100%'; 
            control.style.padding = '3%';
            control.style.marginBottom = '4%';
            control.style.resize = 'none';
        });

        var formControlFile = form.querySelector('.form-control-file');
        if (formControlFile) {
            formControlFile.style.width = '100%'; 
            formControlFile.style.padding = '3%'; 
            formControlFile.style.marginBottom = '4%';
        }

        // Adjust submit button styles
        var submitButton = form.querySelector('.btn-secondary');
        if (submitButton) {
            submitButton.style.width = '40%';
        }
    }
}
