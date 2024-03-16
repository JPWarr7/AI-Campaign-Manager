$(document).ready(function() {
    $(".my-card").click(function() {
        var campaignId = $(this).attr("campaign-id");
        if (campaignId == 'add') {
            var url = "/addCampaign";
        } else {
            var url = "/viewCampaign/" + campaignId;
        };
        window.location.href = url;

    });
});