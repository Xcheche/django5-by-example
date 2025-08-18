from django.urls import path
from uuid import UUID

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    # path("<int:id>/", views.post_detail, name="post_detail"),
    # path("<uuid:id>/", views.post_detail, name="post_detail"),
    #Detail
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    #share post
    path("share/<uuid:post_id>/", views.share_post, name="share_post"),

]
