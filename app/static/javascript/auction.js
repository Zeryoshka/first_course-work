function send_bet(event) {
    var min_cost = Number($('.min_cost').text());
    var max_cost = Number($('.max_cost').text());
    var cur_bet = Number($('#bet_form').serializeArray()[0]['value']);
    if (cur_bet < min_cost || cur_bet > max_cost){
        alert('Ставка не удовлетворяет текущему условию');
        return false;
    }
    lot_id = Number($('.cur_lot_id').text());
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

function get_updates() {
    $.get('api/update_lots').done(function(response){
        console.log(response);
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
tik_tak(Number($.cookie('left_time')));