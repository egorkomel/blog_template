from django.urls import path
from .views import MainView, PostViewDetail

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('<slug>/', PostViewDetail.as_view(), name='post_detail')
]