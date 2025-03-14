
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path('user_profile/<str:username>', views.user_profile, name='user_profile'),
    path('increment_likes/<int:post_id>/', views.increment_likes, name='increment_likes'),
    path('decrement_likes/<int:post_id>/', views.decrement_likes, name='decrement_likes'),
    path('follow/<str:username>/',views.follow, name='follow')
]
