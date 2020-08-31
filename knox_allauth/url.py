from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import KnoxLoginView, KnoxRegisterView, FacebookLogin

urlpatterns = [ 
	path('auth/login/', KnoxLoginView.as_view()),
	path('auth/register/', KnoxRegisterView.as_view()),
	path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
	path('auth/', include('dj_rest_auth.urls')),
	path('account/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
