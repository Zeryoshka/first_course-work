function send_bid(event) {
    var min_cost = Number($('.cur-lot__min-price').text());
    var max_cost = Number($('.cur-lot__max-price').text());
    var cur_bid = Number($('#bid__form').serializeArray()[0]['value']);
    if (cur_bid < min_cost || cur_bid > max_cost){
        write_message('Ставка не удовлетворяет текущему условию');
        return false;
    }
    lot_id = Number($.cookie('cur_lot_id'));
    request_data = {
        lot_id: lot_id,
        price: cur_bid,
    };
    $.post('./api/make_bid', request_data).done(function(response){
        if (response.is_successful)
            write_message('Ставка сделана');
        else
            write_message('Ставка не сделана');
        console.log(response.message);
    })
    return false;
}

function write_message(message) {
    // $('.message-block').text(message)
    // alert(message)
}

function create_lot(lot_type, name, who_bought, price) {
    var lot_name = $('<p></p>', {
        class: 'lot__name',
        text: name
    });

    var img = $('<img>', {
        class: 'lot__icon-in',
        src: lot_type == 'consumer'? '/static/auction-page/img/home_icon.png': 
         '/static/auction-page/img/ses_icon.png'
    });
    var lot_icon = (
        $('<div></div>', {
        class: 'lot__icon',
        }).append(img)
    );

    var lot_team = $('<p></p>', {
        class: 'lot__team',
        text: who_bought
    });

    var lot_price = $('<p></p>', {
        class: 'lot__price',
        text: price
    });
    return $('<div></div>', {
        class: 'lot',
    }).append(lot_name, lot_icon, lot_team, lot_price);
}

function create_cur_lot(cur_lot) {
    $('.cur-lot__name').text(cur_lot.lot_name);
    $('.cur-lot__min-price').text(cur_lot.min_cost);
    $('.cur-lot__max-price').text(cur_lot.max_cost);
    $('.cur-lot__auction-type-img').removeClass(
        "cur-lot__auction-type-img__type_dutch cur-lot__auction-type-img__type_english"
    );
    if (cur_lot.auction_type == 'dutch')
        $('.cur-lot__auction-type-img').addClass("cur-lot__auction-type-img__type_dutch")
    else
        $('.cur-lot__auction-type-img').addClass("cur-lot__auction-type-img__type_english")
}

function update_page(cur_lot, lots) {
    $('.lots__container').empty();
    for (var i = 0; i < lots.length; ++i) {
        var price = lots[i].is_purchased? lots[i].purchase_cost : '0';
        console.log(lots[i].is_purchased);
        var who_bought = lots[i].is_purchased? lots[i].who_bought_name : '-';
        var lot = create_lot(lots[i].lot_type, lots[i].lot_name, who_bought, price);
        console.log(who_bought);
        if (lots[i].is_current)
            lot.addClass('lot_lot-type_cur-lot');
        else if (!lots[i].is_purchased)
            ;
        else if (lots[i].who_bought_id == $.cookie('user_id'))
            lot.addClass('lot_lot-type_your-lot');
        else
            lot.addClass('lot_lot-type_not-your-lot');
        $('.lots__container').append(lot);
    }

    create_cur_lot(cur_lot);
}

function get_updates() {
    $.get('api/update_lots').done(function(response){
        if (!response.is_auction){
            alert('Аукцион окончен');
            location.reload();
        }
        if (response.cur_lot.lot_id == $.cookie('cur_lot_id')) {
            setTimeout(get_updates, 100);
            return;
        }
        $.cookie('cur_lot_id', response.cur_lot.lot_id, {
            path: '/game/auction'
        });
        tik_tak(response.left_time);
        update_page(response.cur_lot, response.lots);
    }).fail(function(response){
        alert('Аукцион окончен');
        location.reload();
    });
}

function tik_tak(left_time) {
    $('#left_time').text(left_time);
    if (left_time > 0) {
        setTimeout(tik_tak, 1000, left_time - 1);
        return;
    }
    get_updates();
}

$('#make_bid_but').click(send_bid);
console.log($.cookie('cur_lot_id'));
tik_tak(Number($.cookie('left_time')));