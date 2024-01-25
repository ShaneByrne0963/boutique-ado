// Updating the product sort when the select input is changed
$('#sort-selector').change(function() {
    let selector = $(this);
    let currentUrl = new URL(window.location);

    let selectedVal = selector.val();
    if (selectedVal !== 'reset') {
        let sort = selectedVal.split('_')[0];
        let direction = selectedVal.split('_')[1];

        currentUrl.searchParams.set('sort', sort);
        currentUrl.searchParams.set('direction', direction);
    }
    else {
        currentUrl.searchParams.delete('sort');
        currentUrl.searchParams.delete('direction');
    }
    window.location.replace(currentUrl);
});

// Button to scroll to the top of the page
$('.btt-link').click(function(e) {
    window.scrollTo(0, 0);
});