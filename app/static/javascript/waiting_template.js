

function getTemplate(time) {
    return `
        <div id='count_down_block' class='status-block__count-down-block'>
            Игра начнется через <span id='count_down'>${time}</span>
        </div>
    `;
}

var fnc = setInterval(function(){
    $.ajax({
        method: "GET",
        url: "api/check_for_waiting"
    }).done(function (response) {
        if (!response.access)
            window.location.reload();
        else {
            $('#current_players_count').text(response.current_players_count);
            if (response.timer_is_active) {
                $('.status-block').empty();
                $('.status-block').append(getTemplate(10));
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
    else
        $.get("api/check_for_waiting").done(function(response){
            if (!response.access)
                window.location.reload();
            if (response.state_closed)
                window.location.href = './preparing_for_game';
            setTimeout(tikTak, 100, left_time);
        });
}

function startCountDown(left_time) {
    // $('.status-block__message').css('display', 'none');
    // $('#count_down_block').append(template_counter_down);
    tikTak(left_time);
}