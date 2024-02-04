function updateCountryField() {
    let countrySelectedField = $('#id_default_country').val();
    if (!countrySelectedField) {
        $('#id_default_country').css('color', '#aab7c4');
    }
    else {
        $('#id_default_country').css('color', '');
    }
}
$('#id_default_country').change(updateCountryField);
updateCountryField();