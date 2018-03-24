
function timeUptopBar(obj){
    var obj = $('.top-alert');
    obj.fadeOut(1500);
    return false;
}

function alertNavtopBar(msg,alerttype){
    var obj = $('.top-alert');
    var btn = $('.top-alert button')
    obj.removeClass('alert-success alert-warning alert-danger');

    obj.addClass('alert-'+alerttype);
    $('#navbar-msg').html(msg);
    obj.fadeIn(1500);
   
    setTimeout(function(){
        timeUptopBar();
    },4000);
    
    btn.click(function(){
        timeUptopBar(obj);
    });  
}


function alertNavtopBarSuccess(msg){
    alertNavtopBar(msg,'success');
}

function alertNavtopBarFail(msg){
    alertNavtopBar(msg,'danger');
}

function alertNavtopBarDanger(msg){
    alertNavtopBar(msg,'danger');
}

function alertNavtopBarWarning(msg){
    alertNavtopBar(msg,'warning');
}

//上传时，错误提示不自动消失
function alertNavtopBarDangerStatic(msg,alerttype){
	var obj = $('.top-alert');
    var btn = $('.top-alert button')
    obj.removeClass('alert-success alert-warning alert-danger');
    obj.addClass('alert-'+alerttype);
    $('#navbar-msg').html(msg);

    obj.animate({height:'toggle'},'slow');
    btn.click(function(){
        timeUptopBar(obj);
    });  
}