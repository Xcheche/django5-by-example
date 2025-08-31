from django.urls import path

from .feeds import LatestPostsFeed
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.post_list, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    # share post
    path("share/<int:post_id>/", views.share_post, name="share_post"),
    # comment
    path("comment/<int:post_id>/", views.post_comment, name="post_comment"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    # Feed
    path("feed/", LatestPostsFeed(), name="post_feed"),
    # Search
    path("search/", views.post_search, name="post_search"),
]
