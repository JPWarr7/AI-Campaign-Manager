import config from './config.js';

window.fbAsyncInit = function() {
    FB.init({
        appId      : config.facebookAppID,
        cookie     : true,
        xfbml      : true,
        version    : config.facebookAPIVersion
    });

    FB.AppEvents.logPageView();

    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            console.log('Logged in.');
        } else {
            console.log('Not logged in.');
        }
    });

    document.getElementById('loginBtn').addEventListener('click', function() {
        FB.login(function(response) {
            if (response.authResponse) {
                console.log('Access token:', response.authResponse.accessToken);
            } else {
                console.log('User cancelled login or did not fully authorize.');
            }
        });
    });
};

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
