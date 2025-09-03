
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.show, name="show"),
    path('gmail/',views.gmail,name="gmail"),
    path('map/',views.map,name="map")
    ]
