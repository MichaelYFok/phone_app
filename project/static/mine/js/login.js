$(document).ready(function () {
   $("#smsBtn").bind("click", function () {
       //告诉后台发送验证码
       data = {"mobile":$("#phone").val()};
      $.ajax({
          url:"/verifycode/",
          data:data,
          type:"get",
          dataType:"json",
          success:function (data, status) {
              console.log(data, status);
              alert(data.data);
          }
      })
   }) ;
});