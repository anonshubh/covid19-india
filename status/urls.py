from django.urls import path
from . import views

urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('about/',views.about,name='about'),
    path('yesterday/',views.yesterday_data,name='yesterday'),

    #API ENDPOINTS
    path('api/yesterday/',views.yesterday_api,name='api-yesterday'),
]