from django.urls import path
from . import views
# from .views import Logout

app_name="myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    #追加です
    
    path("talk_room/<int:userlist_id>/", views.talk_room, name="talk_room"),
    path("friends", views.get_return_link, name="get_return_link"),
    path('logout', views.logout_view, name="logout"),#ログアウトページへのパス
    path('change_email', views.change_email, name='change_email'),
    path('change_username/', views.change_username, name='change_username'),
    path('change_image/', views.change_image, name='change_image'),
    path('change_password/', views.change_password, name='change_password'),
    # path('changed/<int:changed_type>', views.changed, name='changed'),
    
    
]
