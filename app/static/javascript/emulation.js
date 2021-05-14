function create_result(num, name, money) {
    var num_block = $('<div></div>', {
        class: 'user-result__num',
        text: num + ')'
    });
    var name_block = $('<div></div>', {
        class: 'user-result__name',
        text: name
    });
    var money_block = $('<div></div>', {
        class: 'user-result__money',
        text: money
    });

    return $('<div></div>', {
        class: 'other-result__item user-result',
    }).append(num_block, name_block, money_block);
}

function update_page(cur_result, my_result, cur_step) {
    $('.my-result__money').text(my_result);
    $('.main-data__other-results').empty();
    $('#cur_step').text(cur_step);
    for (let i = 0; i < cur_result.length; i++) {
        result = cur_result[i];
        $('.main-data__other-results').append(create_result(i+1, result[0], result[1]))
    }
}


function main() {
    $.get('api/update_result').done(function(response) {
        cur_result = response.cur_result;
        my_result = response.my_result;
        cur_step = response.cur_step;
        update_page(cur_result, my_result, cur_step);
        if (cur_step != response.steps_count)
            setTimeout(main, response.left_time);
    })
}

setTimeout(main, Number($.cookie('left_time')));
console.log(Number($.cookie('left_time')));