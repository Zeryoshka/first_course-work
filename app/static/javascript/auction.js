function send_bet(event) {
    var min_cost = Number($('.min_cost').text());
    var max_cost = Number($('.max_cost').text());
    var cur_bet = Number($('#bet_form').serializeArray()[0]['value']);
    if (cur_bet < min_cost || cur_bet > max_cost){
        alert('Ставка не удовлетворяет текущему условию');
        return false;
    }
    lot_id = Number($.cookie('cur_lot_id'));
    request_data = {
        lot_id: lot_id,
        price: cur_bet,
    };
    $.post('./api/make_bet', request_data).done(function(response){
        if (response.is_successful)
            alert('Ставка сделана');
        else
            alert('Ставка не сделана');
        console.log(response.message);
    })
    return false;
}

/* <div class="lot 
                    {% if lot.is_current %}
                        lot_type_current
                    {% elif lot.who_bought is none %}
                        lot_owner_nobody
                    {% elif lot.who_bought.name == user.name %}
                        lot_owner_your
                    {% elif lot.who_bought.name != user.name %}
                        lot_owner_not-you
                    {% endif %}
                "
                >
                </div> */

function create_lot(id, name, who_bought, price) {
    var lot_id = $('<div></div>', {
        class: 'lot__number',
        text: id
    });
    var lot_name = $('<div></div>', {
        class: 'lot__name',
        text: name
    });
    var lot_team = $('<div></div>', {
        class: 'lot__team',
        text: who_bought
    });
    var lot_price = $('<div></div>', {
        class: 'lot__price',
        text: price
    });
    return $('<div></div>', {
        class: 'lot',
    }).append(lot_id, lot_name, name, who_bought, price);
}

function create_cur_lot(cur_lot) {
    $('.cur_lot_id').text(cur_lot.lot_id);
    $('.current-lot__name').text(cur_lot.lot_name);
    $('.min_cost').text(cur_lot.min_cost);
    $('.max_cost').text(cur_lot.max_cost);
}

function update_page(cur_lot, lots) {
    $('.lots').empty();
    for (var i = 0; i < lots.length; ++i) {
        var price = lots[i].is_purchased? lots[i].lot_price : '0';
        var who_bought = lots[i].is_purchased? lots[i].who_bought : '-';
        var lot = create_lot(lots[i].lot_id, lots[i].lot_name, lots[i], who_bought, price);
        if (lots[i].is_current)
            lot.addClass('lot_type_current');
        else if (!lots[i].is_purchased)
            lot.addClass('lot_owner_nobody');
        else if (lots[i].who_bought == $.cookie('user_id'))
            lot.addClass('lot_owner_your');
        else
            lot.addClass('lot_owner_not-you');
        console.log(lots[i]);
        $('.lots').append(lot);
    }

    create_cur_lot(cur_lot);
}

function get_updates() {
    $.get('api/update_lots').done(function(response){
        if (response.cur_lot.lot_id == $.cookie('cur_lot_id')) {
            setTimeout(get_updates, 100);
            return;
        }
        console.log('gg:')
        console.log(response.cur_lot.lot_id)
        $.cookie('cur_lot_id', response.cur_lot.lot_id, {
            path: '/game/auction'
        });
        tik_tak(response.left_time);
        update_page(response.cur_lot, response.lots);
    });
}

function tik_tak(left_time) {
    $('.current-lot__timer').text(left_time);
    if (left_time > 0) {
        setTimeout(tik_tak, 1000, left_time - 1);
        return;
    }
    get_updates();
}

$('.form__submit').click(send_bet);
console.log($.cookie('cur_lot_id'));
tik_tak(Number($.cookie('left_time')));