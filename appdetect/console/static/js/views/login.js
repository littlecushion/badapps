$(document).ready(function(){
	$('#loginId').click(function(){
		// 取值
		var userName = $('#username').val();
		var password = $('#password').val();
	
		if(userName == "wututu" && password == "1234"){
			window.location.href="../crawler";
		}else{
			alert("用户名密码不对！")
		}
	});
});
