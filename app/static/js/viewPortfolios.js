$(document).ready(function() {
    $(".my-card").click(function() {
        var portfolioId = $(this).attr("portfolio-id");
        var url = "/viewPortfolio/" + portfolioId;
        window.location.href = url;
    });
});
