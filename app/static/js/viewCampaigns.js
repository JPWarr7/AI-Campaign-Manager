$(document).ready(function() {
    $(".my-card").click(function() {
        var campaignId = $(this).attr("campaign-id");
        var url = "/viewCampaign/" + campaignId;
        window.location.href = url;
    });
});