$(function () {
    var r = 255 ;
    var g = 255;
    var b = 0;
    var lum = 100;

    function draw () {
        var rr = Math.floor((r * lum) / 100);
        var gg = Math.floor((g * lum) / 100);
        var bb = Math.floor((b * lum) / 100);
        $('.bulb-top, .bulb-middle-1, .bulb-middle-2, .bulb-middle-3, .bulb-bottom, .night').css(
            {'background': 'rgb('+ rr +', '+ gg +', '+ bb +')'}
        );
    }

    lum = 255
    draw();

    
    r = 255;
    g = 0;
    b = 0;
    draw();
});
