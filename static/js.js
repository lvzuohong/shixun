var uname_flag=false;
var upwd_flag = false;

function  checkName() {

    //获取网页当中输入框里的内容
    uname  =  document.getElementById("uid").value;
    //通过value获取输入框中的值
    //alert(uname.value)
    //alert(uname)
    //用户名格式进行校验  var reg=/^[0-9]{8}$/;   /*定义验证表达式*/  return reg.test(str);     /*进行验证*/
    var reg=/^[A-Za-z0-9]{8,}$/;
    var result = reg.test(uname);
    //alert(result)
    span = document.getElementById("usid");
    if (result==true){
        //将用户名发送到服务器端，校验用户名是否存在
        //http://127.0.0.1:5000/checkName?uname='xiaoming'
        //1.发送的请求和用户名   2.接收后端传递过来的数据
       $.getJSON("checkUName?name="+uname,function(res) {

            result = ""+res;
           if(result=="true"){

               span.innerHTML="<font color='red'>名字已经存在</font>";
               uname_flag = false;
           }else{
                alert("2");
               span.innerHTML="<font color='green'>可以注册</font>";
               uname_flag = true;
           }
       })

    }else{
        span.innerHTML="<font color='red'>用户名格式不正确</font>";
        uname_flag = false;
    }
}
function  checkPwd(){
    pwd = document.getElementById("pid").value;
    var reg=/^[A-Za-z0-9]{6,}$/;
    var result = reg.test(pwd);
    //alert("密码长度至少是6位")
    span = document.getElementById("sid");
    if (result==true){
        span.innerHTML="<font color='green'>密码格式正确</font>";
        upwd_flag=true;
    }else{
        span.innerHTML="<font color='red'>密码长度至少是6位</font>";
        upwd_flag=false;
    }

}

function checkAll() {
    if(uname_flag==true & upwd_flag==true){
        alert("true")
        return true;
    }else{
        alert("false")
        return false;
    }
}
