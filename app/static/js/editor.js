'use strict';

// ref: http://tympanus.net/codrops/2012/10/04/custom-drop-down-list-styling/
function DropDown(editor, elem) {
    this.editor = editor;
    this.dd = elem;
    this.opts = this.dd.find('ul.dropdown > li');
    this.initEvents();
}

DropDown.prototype = {
    initEvents : function() {
        var obj = this;

        obj.dd.on('click', function(event) {
            var activate = !$(this).hasClass('active');
            $('.menu').removeClass('active');
            if (activate) {
                $(this).addClass('active');
            }
            return false;
        });

        obj.opts.on('click', function(event) {
            obj.dd.removeClass('active');
        });
    }
}

function DropDownLanguage(editor, elem) {
    this.editor = editor;
    this.dd = elem;
    this.placeholder = this.dd.children('span');
    this.opts = this.dd.find('ul.dropdown > li');
    this.val = '';
    this.index = -1;
    this.initEvents();
}


DropDownLanguage.prototype = {
    initEvents : function() {
        var obj = this;

        obj.dd.on('click', function(event) {
            var activate = !$(this).hasClass('active');
            $('.menu').removeClass('active');
            if (activate) {
                $(this).addClass('active');
            }
            return false;
        });

        obj.opts.on('click', function(event) {
            var opt = $(this);
            obj.val = opt.text();
            obj.index = opt.index();
            obj.placeholder.text(obj.val);
            var mode = opt.data('ace-mode') || obj.val;
            obj.editor.getSession().setMode('ace/mode/' + mode);
            obj.dd.removeClass('active');
            return false;
        });

        obj.opts.filter(function(){
            return $(this).text() === obj.placeholder.text()
        }).click();
    },
    getValue : function() {
        return this.val;
    },
    getIndex : function() {
        return this.index;
    }
}

// see: http://codepen.io/jacmaes/pen/miBKI
function Terminals(elem) {
    this.terminals = elem;
    this.init();
}

Terminals.prototype = {
    init: function() {
        this.terminals.find('> dd:not(:first)').hide();
        this.terminals.find('> dt:first-child').addClass('active');
        this.terminals.find('> dt').on('click', this._tabClick);
        this.terminals.find('dt:nth-child(3)').click();  // output tab, segunda aba
    },

    clear: function() {
        var abas = this.terminals.find('dt:not(:first-child)');
        abas.next().remove();
        abas.remove();
        this.terminals.find('dt').click();
    },

    addTab: function(tabName, content) {
        var dt = $('<dt />').text(tabName).on('click', this._tabClick);
        var dd = $('<dd />').append(content);
        this.terminals.append(dt).append(dd);
        return dt;
    },

    _tabClick: function(event) {
        $(this).parent().find('> dd').hide();
        $(this).next().show().prev().addClass('active').siblings().removeClass('active');
        return false;
    }
}
