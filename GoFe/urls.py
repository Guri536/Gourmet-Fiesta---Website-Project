"""
URL configuration for GoFe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign', views.sign, name='sign'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('cont-signup', views.cont_sign, name='cont'),
    path('test', views.test, name='test'),
    path('add', views.add, name='add'),
    path('rec', views.rec, name='rec'),
    path('search', views.search, name='search'),
    path('search_res', views.search_res, name="s_r"),
    path('cs', views.csoon, name='cs'),
    path('about', views.ab_us, name='ab'),
    path('privacy-policy', views.pr_po, name='pr')
]
