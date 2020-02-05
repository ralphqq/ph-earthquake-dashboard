from django.urls import include, path


urlpatterns = [
    path('bulletins/', include('bulletin.api.urls'))
]
