var addPortfolioLink = document.getElementById("addPortfolioLink");
var addPortfolioFormDiv = document.getElementById("addPortfolioFormDiv");
var formBlurHandler = null;

addPortfolioLink.addEventListener("click", function(event) {
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/addPortfolioForm");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var tempDiv = document.createElement('div');
                tempDiv.innerHTML = xhr.responseText;

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
                    
                    form.submit();
                });
            } else {
                console.error("Error fetching addPortfolioForm:", xhr.status);
            }
        }
    };
    xhr.send();
});

function blurContent() {
    $('#blur-container').show();
}

function removeBlur() {
    $('#blur-container').hide();
}
