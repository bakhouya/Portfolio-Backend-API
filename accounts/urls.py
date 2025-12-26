# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path
from .views import (CustomLoginView, AdminUserView, AdminProfileView, PortfolioView)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
# ======================================================================================




# ======================================================================================
# Urls app accounts & auth 
# ======================================================================================
urlpatterns = [
    # Custom Url auth Login
    path('auth/login/', CustomLoginView.as_view(), name='Custom_auth'),
    # default auth Login
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # GET & UPDATE data user and Profile
    path('ad/accounts/user/', AdminUserView.as_view(), name='User'),
    path('ad/accounts/profile/', AdminProfileView.as_view(), name='Profile'),
    # get data user and profile 
    path('accounts/user/data/', PortfolioView.as_view(), name='User_data'),



]
# ======================================================================================
