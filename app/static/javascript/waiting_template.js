var fnc = setInterval(function(){
    $.ajax({
        method: "GET",
        url: "api/check_for_waiting"
    }).done(function (response) {
            if (response.accses)
                window.location.reload()
            else {
                $('#current_players_count').text(response.current_players_count);
                $('#need_players_count').text(response.need_players_count);
                if (response.timer_is_active) {
                    $('#header_text').text('Игра скоро начнется');
                    clearInterval(fnc);
                    startCountDown(response.left_time);
                }
            }
    })
}, 400);

function tikTak(left_time) {
        $('#count_down').text(left_time);
        if (left_time > 0) {
            setTimeout(tikTak, 1000, left_time - 1);
        }
        else {
            window.location.href = '/preparing_for_game';
        }
}

function startCountDown(left_time) {
    $('#count_down_block').css('display', 'block');
    tikTak(left_time);
}