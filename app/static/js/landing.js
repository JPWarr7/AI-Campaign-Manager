function applyTooltips() {
    $('[data-toggle="tooltip"]').tooltip({
        html:true,
    });

    $('[data-toggle="tooltip"]').on('click', function () {
        // Trigger the tooltip manually
        $(this).tooltip('show');
      });
}

applyTooltips();