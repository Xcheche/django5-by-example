from django.urls import path
from uuid import UUID 

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.post_list, name="post_list"),
    # path("<int:id>/", views.post_detail, name="post_detail"),
    path("<uuid:id>/", views.post_detail, name="post_detail"),
]
