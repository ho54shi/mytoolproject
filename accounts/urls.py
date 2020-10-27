from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('testindex/', views.index, name='test_index'),
  
]