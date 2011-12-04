(function($, win){

function formatMoney(num) {
    var jingdu = 2;
    return parseFloat(num.toFixed(jingdu));
}



// class
function OrderTable(options) {
    this.options = $.extend({}, {
        tableId : '#order-f-g',
        addRowElem: '#o-f-g-addRow',
        removeRowElem: '#o-f-g-removeRow',
        totlePriceElem: '#o-f-g-totlePrice',
        flashTableElem: '#o-f-g-flash'
    }, options);
}

$.extend(OrderTable.prototype, {
    onPriceChangeListeners: [],
    addOnPriceChangeListener: function(fn) {
        if (fn instanceof Function) {
            this.onPriceChangeListeners.push(fn);
        }
    },
    noticeOnPriceChangeListeners: function(msg) {
        for (i in this.onPriceChangeListeners) {
            var fn = this.onPriceChangeListeners[i];
            if (fn instanceof Function) {
                fn.call(this, msg);
            }
        }
    },

    init: function(options) {
        this.options = $.extend({}, this.options, options);
        this.addListens();
        return this;
    },

    addListens: function() {
        var self = this, o = this.options;
        $(o.tableId + " input[type=text]").change(function(){
            self.flashRow(this);
        });
        $(o.flashTableElem).click(function(){
            self.flashTable();
            return false;
        });
        $(o.removeRowElem).click(function() {
            $(o.tableId + " tr:last").remove();
            return false;
        });
        $(o.addRowElem).click(function() {
            var tableId = o.tableId,
                $table = $(tableId);

            if (!$table.is(':visible')) {
                $table.show();
                return false;
            }

            var $row = $(tableId + " tr:last").clone(true);
            $row.find('input').val("");
            //$row.find('.order-f-g-rubEdgeCost, .order-f-g-area, .order-f-g-price').text('-');
            $row.appendTo($(tableId));
            return false;
        });
    },

    // @Override
    flashRow: function(inputElem) {
        //console.log(inputElem);
        this.onFlash();
        var $row = $(inputElem).parent().parent(),
            $rubEdgeCost = $row.find('.o-f-g-rubEdgeCost'),
            $price = $row.find('.o-f-g-price'),
            $area = $row.find('.o-f-g-area'),
            width = parseInt($row.find('.o-f-g-width').val()),
            height = parseInt($row.find('.o-f-g-height').val()),
            rubEdge = $row.find('.o-f-g-rubEdge').val(),
            rate = parseFloat($row.find('.o-f-g-rate').val()),
            quantity = parseInt($row.find('.o-f-g-quantity').val()),
            extraCost = parseFloat($row.find('.o-f-g-extraCost').val()),
            uPrice = parseFloat($row.find('.o-f-g-uPrice').val());

       if (rate < 1.0) { rate = 1.2; }

       var rubEdgeCost = (width * rubEdge[0] + height * rubEdge[1]) * quantity * 0.001,
            area = width * height / 1000000,
            price = area * quantity * uPrice * rate;

        // for NaN
        rubEdgeCost = (!isNaN(rubEdgeCost)) ? rubEdgeCost : 0;
        extraCost = (!isNaN(extraCost)) ? extraCost : 0;
        area = (!isNaN(area)) ? area : 0;
        price = (!isNaN(price)) ? price : 0;

        $rubEdgeCost.text(formatMoney(rubEdgeCost));
        $area.text(formatMoney(area));
        $price.text(formatMoney(price + rubEdgeCost + extraCost));

        this.onPriceChange();
        this.onFlashEnd();
    },

    flashTable: function() {
        var self = this, o = this.options;
        $(o.tableId + ' .o-f-g-uPrice').each(function(){
            self.flashRow(this);
        });
    },

    //TODO: change to g notice
    onFlash: function() {
        console.log("flash...");
    },
    onFlashEnd: function() {
        console.log("finish.");
    },

    onPriceChange: function() {
        $(this.options.totlePriceElem).text(formatMoney(this.getTotlePrice()));
        this.noticeOnPriceChangeListeners();
        console.log("on price change: " + this.getTotlePrice());
    },

    getTotlePrice: function() {
        var totle = 0;
        $(this.options.tableId + ' .o-f-g-price').each(function(){
            var price = parseFloat($(this).text());
            price = (!isNaN(price)) ? price : 0;
            totle += price;
        });
        return totle;
    }

});

// class InstallTable extends OrderTable
function InstallTable(options) {
    OrderTable.apply(this, arguments);
}
InstallTable.prototype = new OrderTable();
$.extend(InstallTable.prototype, {
    flashRow: function(inputElem) {
        this.onFlash();
        var $row = $(inputElem).parent().parent(),
            $price = $row.find('.o-f-g-price'),
            quantity = this.getQuantity($row, '.o-f-g-quantity'),
            uPrice = parseFloat($row.find('.o-f-g-uPrice').val()),
            price = quantity * uPrice;

        // for NaN
        price = (!isNaN(price)) ? price : 0;
        $price.text(formatMoney(price));

        this.onPriceChange();
        this.onFlashEnd();
    },
    getQuantity: function(row, elem) {
        var $elem = row.find(elem);
        if ($elem[0].nodeName.toUpperCase() == 'INPUT') {
            return $elem.val();
        } else {
            return $elem.text();
        }
    },
});

var Order = {
    options: {
        priceElem: '#order-totle-price',
        tables: [],
    },
    init: function(options) {
        this.options = $.extend({}, this.options, options);
        this.addPriceListener();
    },

    addPriceListener: function() {
        var self = this, o = this.options;
        for (i in o.tables) {
            var table = o.tables[i];
            table.addOnPriceChangeListener(function(){
                self.setOrderPrice();
            });
        }
    },
    setOrderPrice: function() {
        var o = this.options, price = 0;
        for (i in o.tables) {
            var table = o.tables[i], 
                p = parseFloat($(table.options.totlePriceElem).text());
            p = (!isNaN(p)) ? p : 0; 
            price += p;
        }

        $(o.priceElem).text(formatMoney(price));
    },
};


$(window).load(function(){
    console.log("start");

    var glassTable = new OrderTable({
        tableId : '#order-f-g',
        addRowElem: '#o-f-g-addRow',
        removeRowElem: '#o-f-g-removeRow',
        totlePriceElem: '#o-f-g-totlePrice',
        flashTableElem: '#o-f-g-flash'
    }).init();

    var installTable = new InstallTable({
        tableId : '#order-f-i',
        addRowElem: '#o-f-i-addRow',
        removeRowElem: '#o-f-i-removeRow',
        totlePriceElem: '#o-f-i-totlePrice',
        flashTableElem: '#o-f-i-flash'
    }).init();

    var partTable = new InstallTable({
        tableId : '#order-f-p',
        addRowElem: '#o-f-p-addRow',
        removeRowElem: '#o-f-p-removeRow',
        totlePriceElem: '#o-f-p-totlePrice',
        flashTableElem: '#o-f-p-flash'
    }).init();


    Order.init({
        tables: [installTable, glassTable, partTable]
    });

    /*
    installTable.addOnPriceChangeListener(function(){
        Order.setOrderPrice();
    });
    */

});

})(jQuery, window);
