from django.contrib import admin

# Register your models here.
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status", "pk"]

    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

    is_facetable = True  # Make this model facetable
    faceted_search_fields = ["title", "body"]  # Fields to be used in faceted search
    faceted_search = True  # Enable faceted search for this model
    status_list = [Post.Status.DRAFT, Post.Status.PUBLISHED]
    list_editable = ["status"]  # Allow editing of status directly in the list view
    list_per_page = 20
    list_select_related = [
        "author"
    ]  # Optimize queries by selecting related author objects


# Comment
from .models import Comment, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]

    # Make the comment model facetable
    is_facetable = True
    faceted_search_fields = [
        "name",
        "email",
        "body",
    ]  # Fields to be used in faceted search
    faceted_search = True  # Enable faceted search for this model
    list_editable = [
        "active"
    ]  # Allow editing of active status directly in the list view
    list_per_page = 20
    list_select_related = ["post"]  # Optimize queries by selecting related post objects
