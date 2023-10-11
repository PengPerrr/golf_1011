from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('upload_wy',views.upload_wy,name='upload_wy'),
    path('upload_pmc',views.upload_pmc,name='upload_pmc'),
    path('get_state_pmc',views.get_state_pmc,name='get_state_pmc'),
    path('get_state_wy',views.get_state_wy,name='get_state_wy'),
    path('rm_state_wy',views.rm_state_wy,name='rm_state_wy'),
    path('',views.refresh_page,name='refresh_page'),
]

"""
urlpatterns = [
    path("", views.index, name="index"),
    path('upload_wy/',views.upload_wy,name='upload_wy'),
    path('upload_pmc/',views.upload_pmc,name='upload_pmc'),
    path('refresh/',views.refresh_page,name='refresh_page'),
]
"""