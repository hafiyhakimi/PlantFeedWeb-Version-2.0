from member import views
from sharing import views
from group import views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from oauth2_provider.views import AuthorizationView
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index ),
    path('', include('member.urls')),
    path('sharing/', include('sharing.urls')),
    path('group/', include('group.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('basket/', include('basket.urls')),
    path('payment/', include('payment.urls')),
    path('orders/', include('orders.urls')),
    path('topic/', include('topic.urls')),
    # path('sso/', include('sso.provider.urls')),
    path('authorization/', views.custom_oauth_authorization, name='custom_oauth_authorization'),
    path('plantlink/login/', views.login_view, name='plantlinklogin'),
    path('token-exchange/', views.token_exchange_view, name='token_exchange'),
    path('authorize/successful', views.authorize, name='authorize'),
    path('authorization/deny', views.deny, name='deny'),
    path('api/user-data/', views.user_data_api, name='user_data_api'),
]
