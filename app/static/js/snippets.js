function setActive(elem) {
    $(elem).addClass('active').siblings().removeClass('active');
}

function showSnippets(ref, option) {
    setActive(ref);
    $('article').addClass('hidden');
    $('article#' + option).removeClass('hidden');
    return false;
}


function enableAll(ref) {
    setActive(ref);
    $('section.project').removeClass('hidden');
}


function filterLanguage(ref) {
    setActive(ref);
    var language = $(ref).text().toLowerCase();
    $('section.project[data-language="' + language + '"]').removeClass('hidden');
    $('section.project[data-language!="' + language + '"]').addClass('hidden');
    return false;
}


function getVisitedProjects(ref, option) {
    $.get('/visited', {'option': option}, function(data) {
        $('#' + option).html(data);
        showSnippets(ref, option);
        bindDetailButtons();
        flask_moment_render_all();
    });
}


function showDetail() {
    var parent = $(this).parents('section.project')[0];
    $(parent).removeClass('detail-hidden');
}


function hideDetail() {
    var parent = $(this).parents('section.project')[0];
    $(parent).addClass('detail-hidden');
}


function bindDetailButtons() {
    $('i.icon-zoom-in').on('click', showDetail);
    $('i.icon-zoom-out').on('click', hideDetail);
}


$(function() {
    bindDetailButtons();
});
