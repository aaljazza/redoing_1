"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from restaurant import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/list/', views.list, name='list'),
    path('restaurants/detail/<int:restaurant_id>/', views.detail, name='detail'),
    path('create/', views.restaurant_create, name='create'),
    path('restaurants/<int:restaurant_id>/update/', views.restaurant_update, name='update'),
    path('restaurants/<int:restaurant_id>/delete/', views.restaurant_delete, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('restaurants/<int:restaurant_id>/item/', views.item_create, name='create-item'),
    path('no-access/', views.no_access, name='no-access'),
    path('ajax_like/<int:restaurant_id>/', views.ajax_like, name="like_button"),
    path('accounts/', include('allauth.urls')),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)