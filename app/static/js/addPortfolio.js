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

                var form = tempDiv.querySelector('form');

                addPortfolioFormDiv.innerHTML = '';
                addPortfolioFormDiv.appendChild(form);
                
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
                
                form.addEventListener("submit", function(event) {
                    event.preventDefault();
                    var formData = new FormData(form);
                
                    form.action = "/addPortfolio";
                    
                    var submitXhr = new XMLHttpRequest();
                    submitXhr.open("POST", form.action);
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
