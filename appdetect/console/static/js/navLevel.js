/**
 * Created by zhaoyongzhen on 16/2/1.
 */
$(function(){
    var btnSet = $(".set-hd");
    var testList = $(".nav-test-list");
    btnSet.on("mouseover",function(){
        btnSet.parent(".nav-lev-top").hide();
        testList.show();
    })
    testList.on("mouseleave",function(){
        btnSet.parent(".nav-lev-top").show();
        testList.hide();
    })
})
