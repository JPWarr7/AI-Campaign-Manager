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


function applyTooltips() {
    $('[data-toggle="tooltip"]').tooltip({
        html:true,
    });

    $('[data-toggle="tooltip"]').on('click', function () {
        // Trigger the tooltip manually
        $(this).tooltip('show');
      });
}
