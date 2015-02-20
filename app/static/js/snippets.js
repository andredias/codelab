function setActive(elem) {
    $(elem).addClass('active').siblings().removeClass('active');
}

function showSnippets(ref, option) {
    setActive(ref);
    $('article').css('display', 'none');
    $('article#' + option).css('display', '');
    return false;
}


function enableAll(ref) {
    setActive(ref);
    $('section.project').css('display', '');
}

function filterLanguage(ref) {
    setActive(ref);
    var language = $(ref).text().toLowerCase();
    $('section.project[data-language="' + language + '"]').css('display', '');
    $('section.project[data-language!="' + language + '"]').css('display', 'none');
    return false;
}
