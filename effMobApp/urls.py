from django.urls import path
from . import views
from .usersAction.login import user_login, profile_page
from .usersAction.signup import signup
from .usersAction.access.adminAccess import adminPage
from .usersAction.access.operAccess import operatorPage
from .usersAction.access.userAccess import userPage
from .usersAction.updateUserData import editProfile, updateProfileData
from .usersAction.logout import logout_view
from .usersAction.deleteProfile import deleteProfile
from .API.internalApi import get_users_data, update_user_role
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from effMobApp.API.externalApi import external_get_users, external_update_role

urlpatterns = [
    # основные страницы
    path('', views.index, name='index'),
    path('error/', views.error, name='error'),  
    path('signup/', signup, name='signup'),
    path('user_login/', user_login, name='user_login'),

    # профиль пользователя
    path('profile/<int:id>/logout/', logout_view, name='logout'), 

    path('profile/<int:id>/', profile_page, name='profile_page'),
   
    path('profile/<int:id>/operatorPage/', operatorPage, name='operatorPage'), 
    path('profile/<int:id>/userPage/', userPage, name='userPage'), 
    path('profile/<int:id>/editProfile/', editProfile, name='editProfile'), 
    path('profile/<int:id>/deleteProfile/', deleteProfile, name='deleteProfile'), 
    path('profile/<int:id>/editProfile/updateProfileData/', updateProfileData, name='updateProfileData'),

    path('profile/<int:id>/adminPage/', adminPage, name='adminPage'), 
    path('profile/<int:id>/adminPage/api/users/', get_users_data, name='get_users_data'),
    path('profile/<int:id>/adminPage/api/update_role/', update_user_role, name='update_user_role'),

    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # внешние API
    path('external/users/', external_get_users, name='external_get_users'),
    path('external/update_role/', external_update_role, name='external_update_role'),

    path('external/demo/', views.external_api_demo, name='external_api_demo'),
]