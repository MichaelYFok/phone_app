$(document).ready(function () {
    document.documentElement.style.fontSize = innerWidth / 10 + "px"

    //     http://127.0.0.1:8000/market/
    var url = location.href;
    var spanIdStr = url.split("/")[3];
    //修改图片
    var $span = $(document.getElementById(spanIdStr));
    $span.css("background", "url(/static/base/img/"+spanIdStr+"1.png)");
    $span.css("background-size", "0.6rem");
});