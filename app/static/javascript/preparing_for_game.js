function renderPage(left_time) {
    if (left_time > 0) {
        var seconds = String(left_time % 60);
        var minutes = String((left_time - seconds) / 60);
        if (seconds.length < 2)
            seconds = '0' + seconds;
        if (seconds.length < 1)
            seconds = '0' + seconds;
        if (minutes.length < 2)
            minutes = '0' + minutes;
        if (minutes.length < 1)
            minutes = '0' + minutes;
        $('#left-time').text(minutes + ':' + seconds);
        console.log(minutes + ':' + seconds);
        setTimeout(renderPage, 1000, left_time - 1);
    }
    else
        window.location.href = './auction';
}