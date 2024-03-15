function populateTable(searchTerm) {
  $('#results-table tbody').empty();

  var hasPortfolios = false;
  var hasCampaigns = false;
  $('#results-table tbody').append('<tr class="table-divider">');
  $('#results-table tbody').append('<tr><td colspan="2"><b>Portfolios</b></td></tr>');

  user_portfolios.forEach(function(portfolio) {
      if (portfolio[0].toLowerCase().includes(searchTerm.toLowerCase())) {
          var portfolioId = portfolio[2].toString();
          var portfolioLink = '/viewPortfolio/' + portfolioId;
          var portfolioHtml = '<a href="' + portfolioLink + '">' + portfolio[0] + '</a>';
          $('#results-table tbody').append('<tr><td>' + portfolioHtml + '</td><td class="text-right" style="text-align: right;">' + portfolio[1] + '</td></tr>');
          hasPortfolios = true;
      }
  });

  if (hasPortfolios) {
    $('#results-table tbody').append('<tr class="table-divider" style="height:0.5%;">');

  }

  $('#results-table tbody').append('<tr><td colspan="2"><b>Campaigns</b></td></tr>');

  user_campaigns.forEach(function(campaign) {
      if (campaign[0].toLowerCase().includes(searchTerm.toLowerCase())) {
          var campaignId = campaign[8].toString();
          var campaignLink = '/viewCampaign/' + campaignId;
          var campaignHtml = '<a href="' + campaignLink + '">' + campaign[0] + '</a>';
          $('#results-table tbody').append('<tr><td>' + campaignHtml + '</td><td class="text-right" style="text-align: right;">' + campaign[1] + '</td></tr>');
          hasCampaigns = true;
      }
  });

  if (hasPortfolios || hasCampaigns) {
    $('#results-container').show();  
    $('#results-table').show();
  }
}

function blurContent() {
$('#blur-container').show();
}

function removeBlur() {
$('#blur-container').hide();
}

$(document).ready(function() {
$('#search-input').keyup(function() {
    var searchTerm = $(this).val().trim();
    if (searchTerm !== '') {
        populateTable(searchTerm);
        blurContent();
    } else {
        $('#results-table').hide();
        $('#results-container').hide();
        removeBlur();
    }
});
});