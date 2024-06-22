from django.conf import settings
from django.conf.urls.static import static
#=========================================
from django.urls import path, include
from . import views

urlpatterns = [
    #=======================    DEFAULT WEB     ====================================
    path('', views.LoginPage, name = 'LoginPage'),
    
    #=======================    REGISTRATION     ====================================
    path('register', views.register, name = "register"),
    
    #=======================    HOMEPAGE     ====================================
    path('home', views.home, name = 'homepage'),
    
    #=======================    RESPONSIBLE FOR PROFILE     ====================================
    path('profile/<str:username>', views.profile, name = 'profile'),
    
    #=======================    TESTING WEBSITE    ====================================
    # path('tryy', views.tryy, name = 'tryy'),
    
    #=======================    AUTHENTICATIIONS     ====================================
    path('register/success/', views.register_success, name='register_success'),
    path('login/success/', views.login_success, name='login_success'),
    
    #=======================    FUNCTIONS    ====================================
    path('like/', views.like_unlike_post, name='like_unlike_post'), 
    path('friendrequests', views.friendreq, name = 'friendreq'),
    
    #=======================    LOGOUT     ====================================
    path('Log_out', views.Log_out, name = 'Log_out'),
    path('logout/success/', views.Logout_success, name='Logout_success'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
