/**
 * Created by baiby on 16/3/17.
 */
var totalChunk = 0;
var uploadKey = '';
var dataLen = 4096000;
var ext = '';
var fileId = '';
var maxSize = 1024000000;
var uploader = WebUploader.create({
    // swf文件路径
    swf: '/lib/webuploader/Uploader.swf',
    // 文件接收服务端。
    server: fsUrl,
    pick: '#picker',
    dnd: '#file-box',
    accept: {
        title: 'App',
        //extensions:"ipa,apk"
    },
    fileNumLimit: 1,
    //fileSizeLimit: maxSize,
    //fileSingleSizeLimit: maxSize,
    chunked: true,
    chunkSize: dataLen,
    chunkRetry: 10,
    fileVal: 'uploadFile',
    auto: true
});

uploader.on('uploadBeforeSend', function (block, data, headers) {

    fileId = data.id;
    uploadKey = md5(data.lastModifiedDate + data.id + data.size)
    var dataOffset = block.chunk * dataLen;
    var dataTotal = data.size;
    var chunkSize = (dataTotal - dataOffset) > dataLen ? dataLen : (dataTotal - dataOffset);
    var currChunkNum = block.chunk + 1;
    var opt_data = {
        uid: uid,
        op: "Ctfile.upload",
        md5sig: "1",
        shortUrlFlag: "1",
        analyzeAppFlag: "1",
        tag: "testinPortal",
        suffix: ext,
        dataLen: chunkSize,
        dataOffset: dataOffset,
        currChunkNum: currChunkNum,
        isAll: 0
    }
    opt_data.dataTotal = dataTotal;
    opt_data.uploadKey = uploadKey;
    delete data.id;
    delete data.name;
    delete data.type;
    delete data.lastModifiedDate;
    delete data.size;
    delete data.chunks;
    delete data.chunk;

    $.extend(data, {
        'UPLOAD-JSON': JSON.stringify(opt_data)
    });
    totalChunk = block.chunks;
});

// 当有文件被添加进队列的时候
uploader.on('fileQueued', function (file) {
    var extension = 'apk,ipa';
    var exp=new RegExp(',');
    if (extension.indexOf(file.ext.toLocaleLowerCase()) == -1)
    {
        $('#register_ajax').show();
        $('.text_content').text('文件格式有误，请上传以.apk或.ipa结尾的安装包文件');
        $('.resdk').hide();
        cancelUpload();
        return false;
    }

    if (file.size >=maxSize) {
        $('#register_ajax').show();
        $('.text_content').text('文件大小超出限制，最大支持1GB');
        $('.resdk').hide();
        cancelUpload();
        return false;
    }

    if (''!=needed_ext) {
        if('apk' == needed_ext && needed_ext != file.ext){
            $('#register_ajax').show();
            $('.resdk').hide();
            $('.text_content').text('您选择的服务仅支持安卓，请使用一个apk包');
            cancelUpload();
            return false;
        }
        if('ipa' == needed_ext && needed_ext != file.ext){
            $('#register_ajax').show();
            $('.resdk').hide();
            $('.text_content').text('您选择的服务仅支持iOS，请使用一个ipa包');
            cancelUpload();
            return false;
        }

    }

    $('#waitUploadDiv').hide();
    $('#sendUploadDiv').show().html('<h1>应用正在上传中，请不要关闭浏览器</h1> <div class="out-box"><div class="bar-box"></div>' +
        '<div class="box-relatv" id="progress-bar"><div class="motobike"><img src="../../images/motobike.gif" alt=""/></div>' +
        '<span></span></div></div><div class="bar-apk">' + file.name + '<br/><span id="progress_num">0%</span>/' + (file.size / 1000000).toFixed(2) + 'MB <a href="javascript:cancelUpload()">取消上传</a> </div>');
});
// 文件上传过程中创建进度条实时显示。
uploader.on('uploadProgress', function (file, percentage) {
    var progress_num = (percentage * 95).toFixed(2) + '%';
    $('#progress-bar').css('width', progress_num);
    $('#progress_num').html(progress_num);
});
uploader.on('uploadError', function (file, obj) {
    $('#sendUploadDiv').html('ERROR---' + obj);
});
uploader.on('uploadSuccess', function (file, obj) {

    $('#progress-bar').css('width', '97%');
    $('#progress_num').html('97%');
    $('#sendUploadDiv h1').html('上传成功,正在解析...');
    var opt_data = {
        uid: uid,
        op: "Ctfile.upload",
        tag: "testinPortal",
        md5sig: "1",
        shortUrlFlag: "1",
        analyzeAppFlag: "1",
        suffix: file.ext,
        isAll: 1,
        totalChunk: totalChunk,
        dataTotal: file.size,
        uploadKey: uploadKey

    }
    var formData = new FormData();
    formData.append("UPLOAD-JSON", JSON.stringify(opt_data));
    $.ajax({
        url: fsUrl,
        type: 'POST',
        data: formData,
        dataType: 'json',
        cache: false,
        processData: false,
        contentType: false,
        success: function (re) {
            if (0 == re.code) {
                $('#sendUploadDiv h1').html('解析完成,保存中...');
                $('#progress-bar').css('width', '99%');
                $('#progress_num').html('99%');
                var reJson = encodeURIComponent(JSON.stringify(re));
                $.ajax({
                    url: '/file/save-info',
                    type: 'POST',
                    data: {
                        info: reJson,
                        sid : sid,
                        tid : tid,
                        type : type,
                        sdk_app_key : sdk_app_key
                    },
                    dataType: 'json',
                    success: function (rep) {
                        if (rep.success) {
                            $('#progress-bar').css('width', '100%');
                            window.location.href = rep.data + reject_url;
                        }else{
                            $('#register_ajax').show();
                            $('.text_content').text(rep.data);
                            $('#sendUploadDiv h1').html(rep.data);
                            cancelUpload();
                            return false;
                        }
                    },
                    error: function () {
                        $('#sendUploadDiv h1').html('您的应用信息保存失败了,请重试或联系客服帮助您完成.');
                    }
                });

            } else {
                $('#sendUploadDiv h1').html(re.msg);
            }
        },
        error: function () {
            $('#sendUploadDiv h1').html('解析失败,请重试!');
        }
    });

});

function cancelUpload() {
    uploader.stop(true);
    uploader.removeFile(fileId);
    fileId = '';
    uploadKey = '';
    $('#waitUploadDiv').show();
    $('#sendUploadDiv').hide().html('');
}