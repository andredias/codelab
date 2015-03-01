'use strict';

function setActive(elem) {
    $(elem).addClass('active').siblings().removeClass('active');
}

function showSnippets(ref, option) {
    setActive(ref);
    $('article').addClass('hidden');
    $('article#' + option).removeClass('hidden');
    setMaxPage();
    return false;
}


function enableAll(ref) {
    setActive(ref);
    $('section.project').removeClass('hidden');
    setMaxPage();
}


function filterLanguage(ref) {
    setActive(ref);
    var language = $(ref).text().toLowerCase();
    $('section.project[data-language="' + language + '"]').removeClass('hidden');
    $('section.project[data-language!="' + language + '"]').addClass('hidden');
    setMaxPage();
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

var projList;

function calcPage(index) {
    var items_per_page = 5;
    if (index == 0) {
        return 1;
    }
    return Math.ceil(index / items_per_page);
};

function setMaxPage() {
    projList = $('article:not(.hidden) section.project:not(.hidden)');
    var max_page = calcPage(projList.length);
    $('.pagination').jqPagination('option', {'max_page': max_page, 'current_page': 1});
};


function paginate(page) {
    $.each(projList, function(index, elem) {
        if (calcPage(index + 1) != page) {
            $(elem).addClass('paginate-hidden');
        } else {
            $(elem).removeClass('paginate-hidden');
        }
    });
};


$(function() {
    bindDetailButtons();
    $('.pagination').jqPagination({
        paged: paginate,
        page_string: page_string
    });
    setMaxPage();
});
