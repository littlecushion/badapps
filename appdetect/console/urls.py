from django.conf.urls import url

from . import views

urlpatterns = [
 #   url(r'^$', views.index, name='index'),
    url(r'^file/',views.files, name='file'),
    url(r'^crawler/',views.crawler, name='crawler'),
    url(r'^success/',views.success,name='success'),
    url(r'^upload/', views.upload,name='upload'),
    url(r'^apps/', views.apps,name='apps'),
    # url(r'^apps/?page=(?P[0-9]+)/$', views.apps,name='apps'),
    url(r'^service/', views.service,name='service'),
    url(r'^publish/', views.publish,name='publish'),
    url(r'^download/(?P<app_id>[0-9]+)/$', views.download,name='download'),
    url(r'^test/(?P<app_id>[0-9]+)/$', views.test,name='test'),
    url(r'^app_export/(?P<app_id>[0-9]+)/$', views.app_export,name='app_export'),
    url(r'^result/(?P<app_id>[0-9]+)/$', views.result,name='result'),
    url(r'^result/(?P<app_id>[0-9]+)/export/snapshot', views.export_snapshot,name='snapshot'),
    url(r'^result/(?P<app_id>[0-9]+)/export/text', views.export_text,name='text'),
    url(r'^login/', views.login,name='login'),
    url(r'^register/', views.register,name='register'),
    url(r'^logout/', views.logout,name='logout'),
    url(r'^Home/', views.Home,name='Home'),
    url(r'^detect/', views.detect,name='detect'),
    url(r'^upload_word_text/', views.upload_word_text,name='upload_word_text'),
    url(r'^upload_detect_text/', views.upload_detect_text,name='upload_detect_text'),
    url(r'^text_detect_result/', views.text_detect_result,name='text_detect_result'),
]
