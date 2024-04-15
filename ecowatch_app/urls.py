from django.urls import path
from . import views

urlpatterns = [
    path('map',views.map_view,name='map_view'),
    path('', views.waste_site_list, name='waste_site_list'),
    path('upload-and-tag/',views.upload_and_tag, name='upload_and_tag'),
]
