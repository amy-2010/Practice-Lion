from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
	path('search/<str:keyword>/', views.search, name='search'),
]