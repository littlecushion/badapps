#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django import forms
from django.template import RequestContext
#from django.template import RequestContext,loader
from .models import *
from .forms import *
import re
import os
import codecs
import subprocess
import threading
from downloader import *

# Create your views here.
# request 包含所有 POST 和 GET 的数据

def Home(request):
   # return render(request, 'console/file.html', {'what':'Django File Upload'})

    return render(request, 'console/Home.html')

#敏感词检测
def detect(request):
    return render(request,'console/detect.html')

def handle_uploaded_text(file, filename,textDir):
    if not os.path.exists('upload/'+textDir+'/'):
        os.mkdir('upload/'+textDir+'/')

    with open('upload/'+textDir+'/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# 上传敏感词文本
def upload_word_text(request):
    if request.method == 'POST':
        handle_uploaded_text(request.FILES['file'], str(request.FILES['file']),"word_text")
        # return HttpResponseRedirect('/detect/')
        return HttpResponse("Successful")

    return HttpResponse("Failed")


# 上传待检测文本
def upload_detect_text(request):
    if request.method == 'POST':
        handle_uploaded_text(request.FILES['file'], str(request.FILES['file']),"detect_text")
        # return HttpResponseRedirect('/detect/')
        return HttpResponse("Successful")

    return HttpResponse("Failed")

# 文本检测结果
def text_detect_result(request):
    uploadPath="D:\\appdetect\\upload\\"
    wordTextPath=uploadPath+"word_text"+"\\"
    detectTextPath=uploadPath+"detect_text"+"\\"
    word_text = os.listdir(wordTextPath)
    detect_text = os.listdir(detectTextPath)

    
    with codecs.open(wordTextPath+word_text[0],'r','utf-8') as f:
        words = f.readlines()#读取全部内容

    words_dict ={}

    with codecs.open(detectTextPath+detect_text[0],'r','utf-8') as f:
        context=f.read()

    for word in words:
        # 去掉末尾空白字符
        word=word.strip()

        if word not in words_dict:
            words_dict[word]=0

        if re.findall(word,context):
            words_dict[word]+=1

    return render(request,'console/detect_result.html',{'words_dict':words_dict})


def index(request):
    try:
        appsitem = Apps.objects.all()
        context = {'appsitem':appsitem}
    except Apps.DoesNotExist:
        raise Http404("Apps does not exist")
    return render(request,'console/index.html',context)

# def apps(request):  // before the change
#     try:
#         appsitem = Apps.objects.all()
#         context = {'appsitem':appsitem}
#     except Apps.DoesNotExist:
#         raise Http404("Apps does not exist")
#     return render(request,'console/app.html',context)

def apps(request):
    #验证用户信息
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('username', False)
        filterResult = User.objects.filter(username = username)
        if (len(filterResult)==0):
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')

    try:
        apps = Apps.objects.all()
        editions = Editions.objects.all()
    except Apps.DoesNotExist:
        raise Http404("Apps does not exist")

    # editions={}
    # for app in apps:
    #     editions[app.name]=Editions.objects.filter(name=app.name)

    paginator = Paginator(apps, 1) # 分页显示 Show 1 apps per page
    try:
        page = request.GET.get('page')
    except ValueError:
        page = 1
    try:
        appsitem = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.如果页面非整数，只保留第一页
        appsitem = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        appsitem = paginator.page(paginator.num_pages)
    return render(request, 'console/app.html', {'appsitem':appsitem,'editions':editions,'username':username})

def download(request,app_id):
    app = get_object_or_404(Apps,id=app_id)
    url=get_undownloaded_url(app_id)
    filename=downloading(url)
    update_database(app_id,filename)
    print "download sucessful"
    return HttpResponse(app.name+"is downloaded...") 

class UserForm(forms.Form): 
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')
    phone = forms.IntegerField(label='手机号')

def register(request):
    if request.method == "POST":
        #获取表单信息
        username =  request.POST['username']
        filterResult = User.objects.filter(username = username)
        if (len(filterResult)>0):
            return render_to_response('/console/register.html',{"errors":"用户名已存在"})
        # else:
        password1 =  request.POST['password1']
        password2 =  request.POST['password2']
        errors = []
        if (password2 != password1):
            errors.append("两次输入的密码不一致!")
            return render(request,'/console/register.html')
        password1 = password2
        email =  request.POST['email']
        phone = request.POST['phone']
        #将表单写入数据库
        console_user = User.objects.create(username=username,password=password1,email = email, phone = phone)
        console_user.save()  
        #返回注册成功页面
        print 'ok'
        return render(request,'console/login.html')
    else:
        return render(request,'console/register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password = request.POST['password']
        userResult = User.objects.filter(username=username,password = password) #与数据库匹配
        if (len(userResult)>0):
            #比较成功，跳转apps
            print 'OK'
            response = HttpResponseRedirect('/apps/')
            #将username写入浏览器cookie,失效时间为3600
            # response.set_cookie('username',username,3600)
            request.session['IS_LOGIN'] = True
            request.session['username'] = username
            return response
        else:
            #比较失败，还在login
            return HttpResponseRedirect('/login/')
    else:
        #验证用户信息
        is_login = request.session.get('IS_LOGIN', False)
        if is_login:
            username = request.session.get('username', False)
            filterResult = User.objects.filter(username = username)
            if (len(filterResult)==0):
                return render(request,'console/login.html')
            else:
                return HttpResponseRedirect('/apps/')
        else:
            return render(request,'console/login.html')
            
        return render(request,'console/login.html')

def logout(request):
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    # response.delete_cookie('username')
    request.session['IS_LOGIN'] = False 
    request.session.delete("username")
    return HttpResponseRedirect('/login/')

def test(request,app_id):
    app = get_object_or_404(Apps,id=app_id)
    # app = Apps.objects.get(id=app_id)
    # app.downloaded = 0
    # app.save()
    # subprocess.call("python /home/lll/android-apps-crawler/downloader/downloader.py /home/lll/appdetect/db.sqlite3  /home/lll/appdetect/upload/",shell= True)
    # subprocess.call("python D:\\apptest\\appAutoTest\\test.py",shell=True)    
    subprocess.Popen("python D:\\appdetect\\console\\apptest.py "+app_id, shell=True)
    # t = threading.Thread(target=apptest(app_id), name='apptestThread')
    # t.start()
    # return HttpResponse("downlonding..."+" from "+app.url) 
    return HttpResponse(app.name+"is detecting...") 

def app_export(request,app_id):
    app = get_object_or_404(Apps,id=app_id)
    if not app.isDownloaded:
        return HttpResponse("Please download before exporting")
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    output_dir = "D:\\apptest\\appAutoTest\\downloadApk\\apps\\"
    the_file_name = app.appFileName
    response = StreamingHttpResponse(file_iterator(output_dir+the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

# def result(request,app_id):
#     app = get_object_or_404(Apps,id=app_id)
#     if not app.isDetect:
#         return HttpResponse("Please detecting "+app.name)
#     (shotname,extension) = os.path.splitext(app.appFileName) #get rid of suffix
#     textPath = "D:\\apptest\\appAutoTest\\monkeyRunner\\text\\"
#     snapshotPath = "D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"
#     # textName= shotname+".txt"
#     # print textName
#     images= os.listdir(snapshotPath+shotname)
#     texts = os.listdir(textPath+shotname)
#     print len(images)

#     words_dict ={}
#     with codecs.open("D:\\apptest\\appAutoTest\\monkeyRunner\\results\\"+"jinritoutiao_604"+"\\"+"results.txt",'r','utf-8') as f: 
#         for lines in f.readlines(): 
#             line=lines.strip('\r\n') #windows下去除换行
#             list = line.split(' ') #以空格分割
#             allWords = []
#             for word in list:
#                 allWords.append(word)

#             words_dict[allWords[0]]= allWords[1]

#     return render(request, 'console/result.html',{'app':app,'texts':texts,'images':images,'words_dict':words_dict})


def result(request,app_id):
    app = get_object_or_404(Apps,id=app_id)
    if not app.isDetect:
        return HttpResponse("Please detecting "+app.name)
    (shotname,extension) = os.path.splitext(app.appFileName) #get rid of suffix
    textPath = "D:\\apptest\\appAutoTest\\text\\"
    snapshotPath = "D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"
    textName= shotname+".txt"
    print textName
    images= os.listdir(snapshotPath+shotname)
    print len(images)
    return render(request, 'console/result.html',{'app':app,'textName':textName,'images':images})
    

def export_text(request,app_id):
    textName = request.GET['textName']
    app = get_object_or_404(Apps,id=app_id)
    (shotname,extension) = os.path.splitext(app.appFileName) #get rid of suffix
    textPath = "D:\\apptest\\appAutoTest\\monkeyRunner\\text\\"+shotname+"\\"
    #下载文件  
    def readFile(fn, buf_size=262144):#大文件下载，设定缓存大小  
        f = open(fn, "rb")  
        while True:#循环读取  
            c = f.read(buf_size)  
            if c:  
                yield c  
            else:  
                break  
        f.close()  
    response = HttpResponse(readFile(textPath+textName),content_type='APPLICATION/OCTET-STREAM')#设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
    response['Content-Disposition'] = 'attachment; filename='+textName#设定传输给客户端的文件名称  
    response['Content-Length'] = os.path.getsize(textPath+textName)#传输给客户端的文件大小  
    return response  


def export_snapshot(request,app_id):
    snapshotName = request.GET['snapshotName']
    app = get_object_or_404(Apps,id=app_id)
    (shotname,extension) = os.path.splitext(app.appFileName) #get rid of suffix
    snapshotPath = "D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"+shotname+"\\"
    print snapshotPath
    #下载文件  
    def readFile(fn, buf_size=262144):#大文件下载，设定缓存大小  
        f = open(fn, "rb")  
        while True:#循环读取  
            c = f.read(buf_size)  
            if c:  
                yield c  
            else:  
                break  
        f.close() 
    response = HttpResponse(readFile(snapshotPath+snapshotName),content_type='APPLICATION/OCTET-STREAM')#设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
    response['Content-Disposition'] = 'attachment; filename='+snapshotName#设定传输给客户端的文件名称  
    response['Content-Length'] = os.path.getsize(snapshotPath+snapshotName)#传输给客户端的文件大小  
    return response

def redetect(request,app_id):
    word = request.GET['word']
    print word
    app = get_object_or_404(Apps,id=app_id)
    (shotname,extension) = os.path.splitext(app.appFileName) #get rid of suffix
    print shotname
    subprocess.Popen("python D:\\appdetect\\console\\reDetect.py "+shotname+" "+app_id+" "+ word, shell=True)
    return HttpResponse(app.name+"is being detected by"+word)


def crawler(request):
    return render(request, 'console/crawler.html')

def files(request):
   # return render(request, 'console/file.html', {'what':'Django File Upload'})
    return render(request, 'console/file.html')

def upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        return HttpResponse("Successful")
        # return render(request, 'console/success.html')
    return HttpResponse("Failed")

def upload_file(request):
  if request.method == 'POST':
     form = UploadFileForm(request.POST, request.FILES)
     if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect('/success')
   #     return HttpResponse('upload ok!')
  else:
     print "bad"
     form = UploadFileForm()
  return render_to_response('console/upload.html', {'form': form})

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def success(request):
    return render(request,'console/success.html')

def service(request):
    return render(request,'console/service.html')

def publish(request):
    return render(request,'console/publish.html')




def apptest(appid):
    app_id = appid
    url=get_undownloaded_url(app_id)
    downloading(url)
    update_database(app_id)    

    subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\aaptOutput.py",shell=True)
    subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\startMonkeyRunner.py",shell=True)
    files = os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot')
    images= os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\'+files[0])

    img=''
    for i in range(len(images)):
      img=img+images[i]+' '
      # capture%d.png '%(i,)
    
    print img
    subprocess.call("cd D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"+files[0]+"&& FineCmd.exe "+img+"/lang Mixed /out D:\\apptest\\appAutoTest\\temp\\result.txt /quit",shell=True)
    # subprocess.call("python D:\\appdetect\\console\\re.py result.txt "+app_id,shell=True)
    reDetect("result.txt",app_id)



def reDetect(filename,appid):
    path='D:\\apptest\\appAutoTest\\temp\\'+filename
    app_id=appid
    app = get_object_or_404(Apps,id=app_id)

    with open(path,'r') as f:
        test=f.read()
    # print test
    if re.match(r'[\s\S]*头发[\s\S]*',test):
    # if re.match(r'[\s\S]*阿富汗[\s\S]*',test):  
        app.result = True
        print 'OK'
    else:          
        app.result = False
        print 'failed'

    app.isDetect=True  
    app.save()