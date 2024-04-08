$(document).ready(function() {
    $(".my-card").click(function() {
        var campaignId = $(this).attr("campaign-id");
        if (campaignId === 'add') {
            loadAddCampaignForm();
        } else {
            var url = "/viewCampaign/" + campaignId;
            window.location.href = url;
        }
    });
});
