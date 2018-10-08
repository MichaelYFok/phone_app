$(document).ready(function () {
    //黄色小方块
    var url = location.href;
    var spanIdStr = "yellow" + url.split("/")[4];
    var $span = $(document.getElementById(spanIdStr));
    $span.addClass("yellowSlide");

    //点击分类和排序
    $("#typeBtn").bind("click", function () {
        $("#typediv").toggle();
        $("#sortdiv").hide();
    });
    $("#sortBtn").bind("click", function () {
        $("#sortdiv").toggle();
        $("#typediv").hide();
    });
    $("#typediv").bind("click",hideFunc);
    $("#sortdiv").bind("click",hideFunc);
    function hideFunc() {
        $(this).hide()
    }

    //子组添加背景颜色
    var span2IdStr = "bg" + location.href.split("/")[5];
    var $span2 = $(document.getElementById(span2IdStr));
    $span2.addClass("spanbg");


    
    
    function changeCart() {
         //组id   商品id
        gid = $(this).attr("gid");
        pid = $(this).attr("pid");
        num = $(this).attr("num");

        $.get("/carts/", {"gid":gid,"pid":pid,"num":num}, function (data, status) {
            if (data.error == 0){
                $(document.getElementById("num"+pid)).html(data.num)
            } else if (data.error == 1) {
                location.href = "/login/?from=market&gid="+gid+"&cid="+url.split("/")[5]+"&sid="+url.split("/")[6]
            }
        });
    }
    //修改购物车
    $(".addBtn").bind("click", changeCart);
    $(".subBtn").bind("click", changeCart);
});