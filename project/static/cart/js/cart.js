$(document).ready(function () {
   $(".ischose").bind("click", function () {
       gid = $(this).attr("gid");
       pid = $(this).attr("pid");
       //购物车id
       cartid = $(this).attr("cartid");

       $.get("/carts/", {"gid":gid,"pid":pid,"num":0}, function (data, status) {
            if (data.error == 0){
                infoStr = "";
                if (data.isChose){
                    infoStr = "√";
                }
                $(document.getElementById("chose"+cartid)).html(infoStr)
            }
        });
   });


    //下订单
    $("#ok").bind("click", function () {

        $.get("/order/", function (data, status) {
            if (data.error == 0){
                location.href = "/cart/"
            }
        });
    });
});