from django.urls import include, path


urlpatterns = [
    path('bulletin/', include('bulletin.api.urls'))
]
