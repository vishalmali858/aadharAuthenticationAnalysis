"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.views.generic import TemplateView
from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from fs import views

app_name = 'fs'

urlpatterns = [

    url(r'^$',views.home,name='hp'),
    url(r'^login/$',views.login1,name='login1'),
    url(r'^logout_user/$', views.logout_user,name='logout_user'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/send_ma/$', views.send_ma,name='send_ma'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/update_user/$', views.update_user,name='update_user'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/deactivate_user/$', views.deactivate_user,name='deactivate_user'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/delete_user/$', views.del_user,name='del_user'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/ec/$', views.ec,name='ec'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/rl/$', views.rl,name='rl'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/mp/$', views.mp,name='mp'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/up/$', views.up,name='up'),
    url(r'^(?P<rt>PR[0-9][0-9][0-9][0-9]+)/rp/$', views.rp,name='rp'),
    url(r'^(?P<value>.+?)/open_pdf/$', views.open_pdf,name='open_pdf'),
    url(r'^register/$',views.register,name='register'),
    url(r'^(?P<rt>.+?)/y_pdf/$',views.y_pdf,name='ypdf'),
    url(r'^(?P<rt>.+?)/m_pdf/$',views.m_pdf,name='mpdf'),
    url(r'^adview/$',views.al,name='admin_view'),
    url(r'^(?P<rt>.+?)/uview/$',views.ul,name='user_view'),
    #url(r'^error/$',views.err,name='err-re'),
    url(r'^forget/$',views.forget,name='forget'),
    url(r'^otp/$',views.otp,name='otp'),
    url(r'^admin/', admin.site.urls),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
