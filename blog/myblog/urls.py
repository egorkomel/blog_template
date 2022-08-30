from django.urls import path
from .views import MainView, PostViewDetail, SignUpView, SignInView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/', PostViewDetail.as_view(), name='post_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
]