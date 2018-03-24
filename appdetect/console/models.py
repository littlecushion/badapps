#coding=utf-8
from __future__ import unicode_literals

from django.db import models
import sys

sys.path.append('D:\\appdetect\\console\\models.py')

# Create your models here.

class Apps(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    url = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True, null=True)
    appFileName = models.CharField(max_length=50,default=None)  #文件名，带后缀
    # needToDownload = models.BooleanField(default=False) #是否需要下载，True是需要下载
    isDownloaded = models.BooleanField(default=False) #是否已下载，true是已下载
    isDetect = models.BooleanField(default=False) #是否已检测，false是不需要
    result = models.BooleanField(default=False) #检测结果
    
    def __unicode__(self):
        return self.name

class Editions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default=None)
    version = models.CharField(max_length=50,default=None)
    updateTime = models.CharField(max_length=50,default=None)
    size = models.CharField(max_length=50,default=None)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)

#     def __unicode__(self):
#         return self.name

class User(models.Model):
    username = models.CharField(primary_key=True, max_length = 50)
    password = models.CharField(max_length = 50)
    email = models.EmailField()
    phone = models.IntegerField()

    def __unicode__(self):
        return self.username

# class UserApps(models.Model):
#     apps = models.ForeignKey(Apps)
#     isDetect = models.IntegerField(default=0)
#     result = models.BooleanField()
