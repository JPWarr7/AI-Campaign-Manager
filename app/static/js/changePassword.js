var changePasswordLink = document.getElementById("changePasswordLink");
var changePasswordFormDiv = document.getElementById("changePasswordFormDiv");
var formBlurHandler = null;

function loadChangePasswordForm() {
    var async = new XMLHttpRequest();
    async.open("GET", "/changePasswordForm");
    async.onreadystatechange = function() {
        if (async.readyState === 4) {
            if (async.status === 200) {
                var tempDiv = document.createElement('div');
                tempDiv.innerHTML = async.responseText;

                var passwordForm = tempDiv.querySelector('form');

                changePasswordFormDiv.innerHTML = '';
                changePasswordFormDiv.appendChild(passwordForm);

                applyPasswordFormStyles();
                applyTooltips();
                
                changePasswordFormDiv.style.display = "block";
                blurContent();

                if (formBlurHandler) {
                    document.body.removeEventListener("click", formBlurHandler);
                }

                formBlurHandler = function(event) {
                    if (!changePasswordFormDiv.contains(event.target)) {
                        changePasswordFormDiv.style.display = "none";
                        removeBlur();
                        document.body.removeEventListener("click", formBlurHandler);
                    }
                };
                document.body.addEventListener("click", formBlurHandler);

                passwordForm.addEventListener("submit", function(event) {
                    event.preventDefault();
                    var formData = new FormData(passwordForm);
                    showEllipsis();
                    var submitXhr = new XMLHttpRequest();
                    submitXhr.open("POST", passwordForm.action);
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
                console.error("Error fetching changePasswordForm:", async.status);
            }
        }
    };
    async.send();
}

changePasswordLink.addEventListener("click", function(event) {
    event.preventDefault();
    loadChangePasswordForm();
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

function applyPasswordFormStyles() {
    var form = document.getElementById('changePasswordForm');
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
